import re


def change_symmetric_quotes(text):

    stack = [0]
    modified_text = ''
    for char in text:
        if char in ('"', "'", '`'):
            if char == stack[-1]:
                stack.pop()
                modified_text += '»'
            else:
                modified_text += '«'
                stack.append(char)
        else:
            modified_text += char

    return modified_text


def beautify_text(text):

    text = re.sub(' {2,}', ' ', text)  # remove redundant spaces
    text = re.sub('-', '–', text)  # replace 'minus' to 'dash'
    text = re.sub('“|‘', '«', text)
    text = re.sub('”|’', '»', text)
    text = change_symmetric_quotes(text)

    return text
