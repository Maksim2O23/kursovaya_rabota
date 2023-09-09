import pytest
import tempfile
import json
import os
from main import (
    filter_executed_operations,
    sort_operations_by_date,
    mask_credit_card,
    mask_account,
    format_operation,
    mask_card_number,
    mask_account_number,
    read_operations_from_json,
)

@pytest.fixture
def test_data():
    return [{'id': 1, 'state': 'EXECUTED'}, {'id': 2, 'state': 'PENDING'}, {'id': 3}]

def test_filter_executed_operations(test_data):
    # Тестируем функцию фильтрации выполненных операций
    executed_operations = filter_executed_operations(test_data)
    assert len(executed_operations) == 1
    assert executed_operations[0]['id'] == 1

def test_sort_operations_by_date():
    # Создаем тестовые данные
    test_data = [{'date': '2022-01-01'}, {'date': '2021-12-31'}, {'date': '2022-02-01'}]

    # Тестируем функцию сортировки операций по дате
    sorted_operations = sort_operations_by_date(test_data)
    assert sorted_operations[0]['date'] == '2022-02-01'
    assert sorted_operations[-1]['date'] == '2021-12-31'

def test_mask_credit_card():
    # Тестируем функцию маскирования номера карты
    card_number = '1234567890123456'
    masked_card = mask_credit_card(card_number)
    assert masked_card == '****** 3456'

def test_mask_account():
    # Тестируем функцию маскирования номера счета
    account_number = '1234567890'
    masked_account = mask_account(account_number)
    assert masked_account == '**7890'

def test_mask_card_number():
    # Тестируем функцию маскирования номера карты
    card_number = '1234567890123456'
    masked_card = mask_card_number(card_number)
    assert masked_card == '****** 3456'

    # Тестируем случай, когда номер карты None
    card_number = None
    masked_card = mask_card_number(card_number)
    assert masked_card is None

def test_mask_account_number():
    # Тестируем функцию маскирования номера счета
    account_number = '1234567890123456'
    masked_account = mask_account_number(account_number)
    assert masked_account == '**3456'

    # Тестируем случай, когда номер счета None
    account_number = None
    masked_account = mask_account_number(account_number)
    assert masked_account is None

def test_format_operation():
    # Создаем тестовую операцию
    operation = {
        'date': '2022-01-01',
        'description': 'Test Operation',
        'from': '1234567890123456',
        'to': '9876543210987654',
        'operationAmount': {'amount': 100, 'currency': {'name': 'USD'}},
    }

    # Тестируем функцию форматирования операции
    formatted_operation = format_operation(operation)
    assert '2022-01-01 Test Operation' in formatted_operation
    assert '100 USD' in formatted_operation

def test_read_operations_from_json():
    # Создаем временный JSON-файл с данными
    temp_json_data = [
        {
            'date': '2022-01-01',
            'description': 'Test Operation',
            'from': '1234567890123456',
            'to': '9876543210987654',
            'operationAmount': {'amount': 100, 'currency': {'name': 'USD'}},
        },
        {
            'date': '2022-01-02',
            'description': 'Another Test Operation',
            'from': '9876543210987654',
            'to': '1234567890123456',
            'operationAmount': {'amount': 50, 'currency': {'name': 'EUR'}},
        }
    ]

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as json_file:
        json.dump(temp_json_data, json_file)

    # Вызываем функцию чтения данных из временного JSON-файла
    operations_data = read_operations_from_json(json_file.name)

    # Удаляем временный JSON-файл
    os.remove(json_file.name)





