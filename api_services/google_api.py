import os.path
from urllib import parse

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


def get_first_sheet_name(spreadsheet_id, service):

    sheets = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
    ).execute()

    for sheet in sheets['sheets']:
        if sheet['properties']['sheetId'] == 0:
            return sheet['properties']['title']
    return None


def get_all_rows(first_sheet_name, spreadsheet_id, service):

    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=first_sheet_name
    ).execute()

    values = result.get('values', [])
    column_titles, rows = values[0], values[1:]

    return [dict(zip(column_titles, row)) for row in rows]


def modify_cell(cell):
    pass


def color_cell(cell):
    pass


def select_posts_to_publish(rows):

    posts_to_publish = []

    for row in rows:
        for row_title, row_value in row.items():
            if row_title == 'Статус' and row_value == 'Обработан':
                continue

        dt_format = '%d.%m.%Y %H:%M'
        pub_time = datetime.strptime(f'{row["Дата"]} {row["Время"]}', dt_format)
        if pub_time < datetime.now():
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


def get_publishing_text(doc_url):

    creds = get_credentials()
    document_id = get_doc_id_from_url(doc_url)
    service = get_document_service(creds)
    document = service.documents().get(documentId=document_id).execute()
    doc_text = select_text_from_doc(document)

    return doc_text


def get_unpublished_posts(spreadsheet_id):

    creds = get_credentials()
    service = get_spreadsheet_service(creds)
    first_sheet_name = get_first_sheet_name(spreadsheet_id, service)
    all_rows = get_all_rows(first_sheet_name, spreadsheet_id, service)
    posts_to_publish = select_posts_to_publish(all_rows)

    return posts_to_publish