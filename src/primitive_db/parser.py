# !/usr/bin/env python3
"""Парсеры сложных функций."""

import shlex
import re


def parse_set_where(tokens: list[str]) -> dict:
    """
    Парсит условие SET/WHERE
    в формате col = value.
    """
    if len(tokens) < 3 or tokens[1] != "=":
        print("Некорректный синтаксис SET.")
        return {}
    col, _, val = tokens
    val = val.strip('"') if val.startswith('"') and val.endswith('"') else val
    return {col: val}


def parse_where_condition(tokens: list[str]) -> tuple:
    """
    Парсит условие WHERE с поддержкой различных операторов:
    =, !=, >, <

    Возвращает кортеж (column, operator, value)
    """
    condition_str = " ".join(tokens)

    pattern = r'(.+?)\s*(=|!=|>|<)\s*(.+)'
    match = re.match(pattern, condition_str.strip())

    if not match:
        raise ValueError(f"Некорректное условие WHERE: {condition_str}")

    column = match.group(1).strip()
    operator = match.group(2).strip()
    value = match.group(3).strip()

    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    elif value.startswith("'") and value.endswith("'"):
        value = value[1:-1]

    return column, operator, value


def parse_insert(values_str: str) -> list:
    """
    Разбирает строку вида '(value1, value2, ...)'
    и возвращает список значений.
    Учтены кавычки для строк с пробелами и запятыми.
    """
    values_str = values_str.strip()
    if values_str.startswith("(") and values_str.endswith(")"):
        values_str = values_str[1:-1]

    raw_values = shlex.split(values_str)
    values = [tok.rstrip(',') for tok in raw_values if tok != ","]
    return values
