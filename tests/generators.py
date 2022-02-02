import random
from string import ascii_lowercase, digits


def random_string(length: int) -> str:
    """
    Генерирует строку случайных символов заданной длины
    Args:
        length (int): Длина генерируемой строки

    Returns:
        str: Сгенерированная строка
    """
    return ''.join(random.choice(ascii_lowercase) for _ in range(length))


def random_int(length: int) -> int:
    """
    Генерирует случайную целочисленную цифру заданной длины
    Args:
        length (int): Длина генерируемой цифры

    Returns:
        str: Сгенерированная цифра
    """
    return int(''.join(random.choice(digits) for _ in range(length)))


