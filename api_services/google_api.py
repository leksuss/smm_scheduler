import os.path
from urllib import parse
import validators

from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/documents.readonly',
]
FALTURE_RGB_CELL_COLOR = {'red': 254, 'green': 196, 'blue': 189}
SUCCESS_RGB_CELL_COLOR = {'red': 208, 'green': 230, 'blue': 201}


def get_credentials():

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_spreadsheet_service(creds):

    service = build('sheets', 'v4', credentials=creds)
    return service


def get_document_service(creds):

    service = build('docs', 'v1', credentials=creds)
    return service


def get_first_sheet_name(sheet_id, service):

    sheets = service.spreadsheets().get(
        spreadsheetId=sheet_id,
    ).execute()

    for sheet in sheets['sheets']:
        if sheet['properties']['sheetId'] == 0:
            return sheet['properties']['title']
    return None


def get_all_rows(first_sheet_name, sheet_id, service):

    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=sheet_id,
        range=first_sheet_name
    ).execute()

    values = result.get('values', [])
    column_titles, rows = values[0], values[1:]

    rows_with_titles = []
    for row in rows:
        row_with_titles = dict(zip(column_titles, map(str.strip, row)))
        rows_with_titles.append(row_with_titles)

    return rows_with_titles


def update_value_cell_body_request(cell_value, cell_coord, sheet_id=0):

    if validators.url(cell_value):
        user_entered_value = {
            "formulaValue": f'=ГИПЕРССЫЛКА("{cell_value}"; "ссылка")',
        }
    else:
        user_entered_value = {
            "stringValue": cell_value,
        }

    return {
        "updateCells": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": cell_coord['row'],
                "endRowIndex": cell_coord['row'] + 1,
                "startColumnIndex": cell_coord['col'],
                "endColumnIndex": cell_coord['col'] + 1,
            },
            "rows": [{
                "values": [{
                    "userEnteredValue": user_entered_value,
                }]
            }],
            "fields": "userEnteredValue",
        }
    }


def colorize_cell_body_request(rgb_color, cell_coord, sheet_id=0):
    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": cell_coord['row'],
                "endRowIndex": cell_coord['row'] + 1,
                "startColumnIndex": cell_coord['col'],
                "endColumnIndex": cell_coord['col'] + 1,
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                        "red": rgb_color['red'] / 255,
                        "green": rgb_color['green'] / 255,
                        "blue": rgb_color['blue'] / 255,
                    }
                }
            },
            "fields": "userEnteredFormat.backgroundColor"
        }
    }


def update_post_status_to_cell(cell_value, cell_coord, sheet_id, service):

    google_api_body_requests = []
    cell_color = FALTURE_RGB_CELL_COLOR

    if cell_value:
        google_api_body_requests.append(
            update_value_cell_body_request(cell_value, cell_coord)
        )
        cell_color = SUCCESS_RGB_CELL_COLOR

    google_api_body_requests.append(
        colorize_cell_body_request(cell_color, cell_coord),
    )

    request = service.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={'requests': google_api_body_requests}
    )
    request.execute()

    return None


def update_post_row(social_media_names, row, sheet_id, service):

    for social_media_name in social_media_names:
        if row[social_media_name] != '':
            cell_coord = {
                'col': tuple(row).index(social_media_name),
                'row': row['id'],
            }

            update_post_status_to_cell(
                row[social_media_name], cell_coord, sheet_id, service
            )
    cell_coord = {
        'col': tuple(row).index('id'),
        'row': row['id'],
    }
    update_post_status_to_cell(
        'Обработан', cell_coord, sheet_id, service
    )


def select_posts_to_publish(rows):

    posts_to_publish = []
    for i, row in enumerate(rows, 1):
        if row.get('Статус') == 'Обработан':
            continue

        pub_time = datetime.strptime(
            f'{row["Дата"]} {row["Время"]}', '%d.%m.%Y %H:%M'
        )

        if pub_time < datetime.now():
            row['id'] = i
            posts_to_publish.append(row)

    return posts_to_publish


def get_doc_id_from_url(doc_url):

    parsed_url_parts = parse.urlparse(doc_url)
    return parsed_url_parts.path.split('/')[3]


def select_text_from_doc(document):

    doc_text = ''
    doc_elements = document.get('body').get('content')
    for doc_element in doc_elements:
        if 'paragraph' in doc_element:
            paragraph_elements = doc_element.get('paragraph').get('elements')
            for paragraph_element in paragraph_elements:
                text_run = paragraph_element.get('textRun')
                if text_run:
                    doc_text += text_run.get('content')

    return doc_text


def get_publishing_text(doc_url, service):

    document_id = get_doc_id_from_url(doc_url)
    document = service.documents().get(documentId=document_id).execute()
    doc_text = select_text_from_doc(document)

    return doc_text


def get_unpublished_posts(sheet_id, service):

    first_sheet_name = get_first_sheet_name(sheet_id, service)
    all_rows = get_all_rows(first_sheet_name, sheet_id, service)
    posts_to_publish = select_posts_to_publish(all_rows)

    return posts_to_publish
