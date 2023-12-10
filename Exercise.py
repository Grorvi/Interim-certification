"""
Задача № 1:

Возьмите любые 1-3 задания из прошлых домашних заданий. Добавьте к ним логирование ошибок и полезной информации. Также реализуйте возможность запуска из командной строки с передачей параметров.

Логирование работы и запуск из командной строки функций из задачи № 4 про банкомат (из семинара № 4 "Функции"): Задача № 4: Возьмите задачу о банкомате из семинара 2. Разбейте её на отдельные операции — функции. Дополнительно сохраняйте все операции поступления и снятия средств в список.


"""

import argparse
import logging
import sys

MULTIPLICITY = 50
TAX_RATE = 0.015
TAX_MIN_LIMIT = 30
TAX_MAX_LIMIT = 600
EXPECTED_OPERATION = 3
EXPECTED_OPERATION_RATE = 0.03
WEALTH_LIMIT = 5_000_000
WEALTH_LIMIT_RATE = 0.1

operations_list = [] 

logging.basicConfig(filename='log.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s', encoding='utf-8')


def log_error(error_msg):
    logging.error(error_msg)


def log_info(info_msg):
    logging.info(info_msg)


def deposit(balance, amount, operations_count, operations_list):
    try:
        if balance > WEALTH_LIMIT:
            wealth_tax = balance * WEALTH_LIMIT_RATE
            balance -= wealth_tax
            log_info(f"Ваш баланс превышает сумму в 5 млн, удержан налог на богатство 10%. Текущий баланс: {balance} у.е.")
            print(f"Ваш баланс превышает сумму в 5 млн, удержан налог на богатство 10%. Текущий баланс: {balance} у.е.")

        if amount % MULTIPLICITY != 0:
            print(f"Депозит должен быть пополнен на сумму, кратную 50 у.е. Пополнение не выполнено!")
            print(f"Текущий баланс: {balance} у.е.")
            log_error("Депозит должен быть пополнен на сумму, кратную 50 у.е. Пополнение не выполнено!")
            log_info(f"Текущий баланс: {balance} у.е.")
            return balance, operations_count, operations_list

        if operations_count % EXPECTED_OPERATION == 0:
            balance += amount
            balance += balance * EXPECTED_OPERATION_RATE
            print(f"Вы совершили третью операцию. Ваш баланс пополняется на {EXPECTED_OPERATION_RATE * 100} %, что составляет {balance * EXPECTED_OPERATION_RATE} у.е.")
            log_info(f"Вы совершили третью операцию. Ваш баланс пополняется на {EXPECTED_OPERATION_RATE * 100} %, что составляет {balance * EXPECTED_OPERATION_RATE} у.е.")
        else:
            balance += amount

        operations_count += 1
        print(f"Депозит пополнен на {amount} у.е. Текущий баланс: {balance} у.е.")
        log_info(f"Депозит пополнен на {amount} у.е. Текущий баланс: {balance} у.е.")
        operations_list.append(f"Депозит пополнен на {amount} у.е.")
        return balance, operations_count, operations_list
    except Exception as e:
        log_error(f"Ошибка в работе функции deposit(): {str(e)}")

def withdraw(balance, amount, operations_count, operations_list):
    try:
        if balance > WEALTH_LIMIT:
            wealth_tax = balance * WEALTH_LIMIT_RATE
            balance -= wealth_tax
            print(f"Ваш баланс превышает сумму в 5 млн, удержан налог на богатство 10%. Текущий баланс: {balance} у.е.")
            log_info(f"Ваш баланс превышает сумму в 5 млн, удержан налог на богатство 10%. Текущий баланс: {balance} у.е.")

        if amount % MULTIPLICITY != 0:
            print(f"Списание с депозита должено быть на сумму, кратную 50 у.е. Списание не выполнено!")
            print(f"Текущий баланс: {balance} у.е.")
            log_error("Списание с депозита должено быть на сумму, кратную 50 у.е. Списание не выполнено!")
            log_info(f"Текущий баланс: {balance} у.е.")
            return balance, operations_count, operations_list

        if balance < amount:
            print(f"Недостаточно средств на счете. Списание не выполнено!")
            log_error("Недостаточно средств на счете. Списание не выполнено!")
            return balance, operations_count, operations_list

        withdrawal_fee = max(min(amount * TAX_RATE, TAX_MAX_LIMIT), TAX_MIN_LIMIT)
        print(f"Удержана комиссия в размере {withdrawal_fee} у.е.")
        log_info(f"Удержана комиссия в размере {withdrawal_fee} у.е.")
        balance -= amount + withdrawal_fee

        if operations_count % EXPECTED_OPERATION == 0:
            balance += balance * EXPECTED_OPERATION_RATE
            print(f"Вы совершили третью операцию. Ваш баланс пополняется на {EXPECTED_OPERATION_RATE * 100} %, что составляет {balance * EXPECTED_OPERATION_RATE} у.е.")
            log_info(f"Вы совершили третью операцию. Ваш баланс пополняется на {EXPECTED_OPERATION_RATE * 100} %, что составляет {balance * EXPECTED_OPERATION_RATE} у.е.")

        operations_count += 1
        print(f"К выдачи {amount} у.е. Текущий баланс: {balance} у.е.")
        log_info(f"К выдачи {amount} у.е. Текущий баланс: {balance} у.е.")
        operations_list.append(f"Со счета списано: {amount} у.е.")
        return balance, operations_count, operations_list
    except Exception as e:
        log_error(f"Ошибка в функции withdraw(): {str(e)}")

def check_balance(balance, operations_list):
    try:
        if balance > WEALTH_LIMIT:
            wealth_tax = balance * WEALTH_LIMIT_RATE
            balance -= wealth_tax
            print(f"Ваш баланс превышает сумму в 5 млн, удержан налог на богатство 10%. Текущий баланс: {balance} у.е.")
            log_info(f"Ваш баланс превышает сумму в 5 млн, удержан налог на богатство 10%. Текущий баланс: {balance} у.е.")
        print(f"Текущий баланс: {balance} у.е.")
        print(f"История поступления и снятия средств со счета: {operations_list}")
        log_info(f"Текущий баланс: {balance} у.е.")
        log_info(f"История поступления и снятия средств со счета: {operations_list}")
    except Exception as e:
        log_error(f"Ошибка в работе функции check_balance(): {str(e)}")

def print_parameters():
    print(f"Кратность операции: {MULTIPLICITY}")
    print(f"Процентная ставка: {TAX_RATE}")
    print(f"Минимальная сумма: {TAX_MIN_LIMIT}")
    print(f"Максимальная сумма: {TAX_MAX_LIMIT}")
    print(f"Номер операции на начисление: {EXPECTED_OPERATION}")
    print(f"Процентная ставка на операцию: {EXPECTED_OPERATION_RATE}")
    print(f"Лимит богатства: {WEALTH_LIMIT}")
    print(f"Процентная ставка на богатство: {WEALTH_LIMIT_RATE}")

def parse_args():
    parser = argparse.ArgumentParser(description='ATM Script with Logging')
    parser.add_argument('--MULTIPLICITY', type=int, default=MULTIPLICITY, help='Сумма пополнения и снятия кратны 50 у.е.')
    parser.add_argument('--TAX_RATE', type=float, default=TAX_RATE, help='Процент за снятие')
    parser.add_argument('--TAX_MIN_LIMIT', type=int, default=TAX_MIN_LIMIT, help='Минимальная сумма для снятия')
    parser.add_argument('--TAX_MAX_LIMIT', type=int, default=TAX_MAX_LIMIT, help='Максимальная сумма для снятия')
    parser.add_argument('--EXPECTED_OPERATION', type=int, default=EXPECTED_OPERATION, help='Номер операции, после которой начисляются проценты')
    parser.add_argument('--EXPECTED_OPERATION_RATE', type=float, default=EXPECTED_OPERATION_RATE, help='Процентная ставка для операции, после которой начисляются проценты')
    parser.add_argument('--WEALTH_LIMIT', type=int, default=WEALTH_LIMIT, help='Сумма, после которой начисляется налог на богатство')
    parser.add_argument('--WEALTH_LIMIT_RATE', type=float, default=WEALTH_LIMIT_RATE, help='Процентная ставка на богатство')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    MULTIPLICITY = args.MULTIPLICITY
    TAX_RATE = args.TAX_RATE
    TAX_MIN_LIMIT = args.TAX_MIN_LIMIT
    TAX_MAX_LIMIT = args.TAX_MAX_LIMIT
    EXPECTED_OPERATION = args.EXPECTED_OPERATION
    EXPECTED_OPERATION_RATE = args.EXPECTED_OPERATION_RATE
    WEALTH_LIMIT = args.WEALTH_LIMIT
    WEALTH_LIMIT_RATE = args.WEALTH_LIMIT_RATE

balance = 0
operations_count = 1
    
while True:
    print("\nВыберите действие:")
    print("1. Пополнение депозита")
    print("2. Списание (снятие) средств")
    print("3. Проверка баланса")
    print("4. Проверка параметров работы банкомата")
    print("5. Выход")
        
    choice = input()
        
    if choice == "1":
        print(f"Текущий баланс: {balance} у.е.")
        amount = int(input("Введите сумму пополнения: "))
        balance, operations_count, operations_list = deposit(balance, amount, operations_count, operations_list)
    elif choice == "2":
        print(f"Текущий баланс: {balance} у.е.")
        amount = int(input("Введите сумму списания: "))
        balance, operations_count, operations_list = withdraw(balance, amount, operations_count, operations_list)
    elif choice == "3":
        check_balance(balance, operations_list)
    elif choice == "4":
        print_parameters()
    elif choice == "5":
        print("Благодарим Вас за использование нашего банкомата. Ваш сеанс работы завершен.")
        exit()
    else:
        print("Введен неправильный номер действия! Пожалуйста, сделайте правильный выбор.")