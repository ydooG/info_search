import re

from task3.helpers import InvertedIndex

operation_mapping = {
    'OR': '|',
    'AND':  '&',
    'NOT': 'result_set -',
    '(': '(',
    ')': ')'
}


def is_operator(string) -> bool:
    return string in ['AND', 'OR', 'NOT', '(', ')']


def is_cyrillic(string) -> bool:
    """
    Checks if given word is russian
    :param string:
    :return:
    """
    return all([bool(re.search('[а-яА-Я]', letter)) for letter in string])


def is_operand(string) -> bool:
    return not is_operator(string) and is_cyrillic(string)


def prettify_set(result_set) -> str:
    result = ''
    for page_num in result_set:
        result += f'{page_num}\n'
    return result + f'-----------\nВсего: {len(result_set)}\n'


def dispatch_query(inv_index, query) -> set:
    """
    :param inv_index: inverted index
    :param query: query string
    :return: set of page numbers
    """
    result_set = set()
    for pages in inv_index.values():
        result_set.update(pages)
    args = query.split(' ')
    equation = ''
    for arg in args:
        if is_operand(arg):
            equation += f'inv_index["{arg}"] '
        elif is_operator(arg):
            equation += f'{operation_mapping[arg]} '
        else:
            raise ValueError(f'Неверный запрос "{arg}"')
    return eval(equation)


def main():
    info_text = 'Поддерживаемые операции: AND OR NOT ( ).\nПосле каждого слова/операции нужно ставить пробел.\n' \
                'Чтобы завершить работу, введите "STOP"\n'
    print(info_text)
    stop = False
    inv_index = InvertedIndex()
    while not stop:
        query = input('Введите запрос:\n')
        if query == 'STOP':
            stop = True
        else:
            try:
                print(prettify_set(dispatch_query(inv_index, query)))
            except ValueError as e:
                print(str(e))
            except SyntaxError:
                print('Неверный запрос')


if __name__ == '__main__':
    main()
