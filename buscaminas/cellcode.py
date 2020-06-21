
COVERED = '.'
FLAG = 'F'
QUESTION = '?'
MINE = '*'
BLANK = ' '


def count(number):
    return number if number > 0 else BLANK


def decode_count(code):
    if code == BLANK:
        return 0
    return int(code)
