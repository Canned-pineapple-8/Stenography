# utils.py
from typing import List, Tuple, NamedTuple
from constants import end_of_line_symbol, space_symbols


def trim_spaces(text: str, markers: Tuple[str, ...] = end_of_line_symbol) -> List[str]:
    """
    Предобработка контейнера:
    - разбивает текст на строки
    - удаляет лишние пробелы в конце строк
    - возвращает список строк (без символов переноса строки)
    """
    sentences: List[str] = []
    current = []
    i = 0

    while i < len(text):
        ch = text[i]
        current.append(ch)

        if ch in markers:
            current.pop()
            next_symbol = i
            i -= 1
            while current and i < len(text) and text[i].isspace():
                current.pop()
                i -= 1
            sentences.append(''.join(current))
            current = []
            i = next_symbol

        i += 1

    if current:
        sentences.append(''.join(current))

    return sentences


def extract_spaces(text: str, markers: Tuple[str, ...] = end_of_line_symbol) -> List[str]:
    """
    Извлекает пробелы после каждого конца предложения.
    Используется при дешифровании.
    """
    spaces: List[str] = []
    i = 0

    while i < len(text):
        if text[i] in markers:
            buf = []
            next_symbol = i + 1
            i -= 1
            while i >= 0 and text[i] in space_symbols:
                buf.append(text[i])
                i -= 1
            i = next_symbol

            if buf:
                spaces.append(''.join(buf[::-1]))
        else:
            i += 1

    return spaces


def text_to_bits(text: str, encoding: str = "utf-8") -> List[int]:
    """
    Кодирует текст в список бит (0/1)
    """
    bits: List[int] = []
    for byte in text.encode(encoding):
        bits.extend(int(bit) for bit in f"{byte:08b}")
    return bits


def bits_to_text(bits: List[int], encoding: str = "utf-8") -> str:
    """
    Декодирует список бит обратно в строку
    """
    if len(bits) % 8 != 0:
        raise ValueError("Количество бит должно быть кратно 8")

    data = bytes(
        int(''.join(map(str, bits[i:i + 8])), 2)
        for i in range(0, len(bits), 8)
    )

    return data.decode(encoding)


class LengthCheckResult(NamedTuple):
    container_capacity: int
    message_length: int
    fits: bool


def check_len(container_text: str, secret_text: str) -> LengthCheckResult:
    """
    Проверяет, помещается ли сообщение в контейнер
    """
    sentences = trim_spaces(container_text)
    container_capacity = len(sentences)

    message_bits = text_to_bits(secret_text)
    message_length = len(message_bits)

    return LengthCheckResult(
        container_capacity=max(container_capacity, 0),
        message_length=message_length,
        fits=message_length <= container_capacity
    )