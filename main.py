import json


def read_operations_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Убираем дубликаты операций на основе их текстового представления
    unique_operations = []
    unique_operation_strings = set()

    for operation in data:
        operation_string = json.dumps(operation, sort_keys=True)
        if operation_string not in unique_operation_strings:
            unique_operation_strings.add(operation_string)
            unique_operations.append(operation)

    return unique_operations


def filter_executed_operations(operations):
    return [op for op in operations if 'state' in op and op['state'] == 'EXECUTED']


def sort_operations_by_date(operations):
    return sorted(operations, key=lambda x: x['date'], reverse=True)


def mask_card_number(card_number):
    # Маскирование номера карты (показываем первые 6 цифр и последние 4)
    if card_number is None:
        return None  # Возвращаем None, если номер карты не определен
    return f"{'*' * 6} {card_number[-4:]}"

def mask_account_number(account_number):
    # Маскирование номера счета (показываем только последние 4 цифры)
    if account_number is None:
        return None  # Возвращаем None, если номер счета не определен
    return f"**{account_number[-4:]}"


def format_operation(operation):
    # Извлекаем необходимые данные из операции
    date = operation['date']
    description = operation['description']
    from_account = operation.get('from', 'None')
    to_account = operation.get('to', 'None')
    amount = operation['operationAmount']['amount']
    currency = operation['operationAmount']['currency']['name']

    # Маскирование номера карты
    from_account = mask_credit_card(from_account)
    # Маскирование номера счета
    to_account = mask_account(to_account)

    # Форматируем и выводим операцию
    formatted_operation = f"{date} {description}\n{from_account} -> {to_account}\n{amount} {currency}\n"
    return formatted_operation.replace('**', '******')



def mask_credit_card(card_number):
    # Маскирование номера карты (показываем первые 6 цифр и последние 4)
    if card_number is None:
        return 'None'
    return f"{'*' * 6} {card_number[-4:]}"


def mask_account(account_number):
    # Маскирование номера счета (показываем только последние 4 цифры)
    if account_number is None:
        return 'None'
    return f"**{account_number[-4:]}"


def main():
    # Чтение данных из JSON-файла
    operations_data = read_operations_from_json('operations.json')

    # Фильтрация выполненных операций
    executed_operations = filter_executed_operations(operations_data)

    # Сортировка выполненных операций по дате в убывающем порядке
    sorted_operations = sort_operations_by_date(executed_operations)[:5]

    # Убираем дубликаты операций
    unique_operations = []

    # Пройдем по отсортированным операциям и добавим их в unique_operations, если они не были добавлены ранее
    for operation in sorted_operations:
        if operation not in unique_operations:
            unique_operations.append(operation)

    # Выводим только первые 5 уникальных операций
    for operation in unique_operations[:5]:
        formatted = format_operation(operation)
        print(formatted)


if __name__ == "__main__":
    main()