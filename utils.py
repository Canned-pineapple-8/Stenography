# utils.py
from typing import List, Tuple, NamedTuple
from constants import end_of_sentence_symbols, end_marker_const


def trim_spaces(text: str, markers: Tuple[str, ...] = end_of_sentence_symbols) -> List[str]:
    """
    Предобработка контейнера:
    - разбивает текст на предложения
    - удаляет лишние пробелы после знаков конца предложения
    - возвращает список предложений (каждое с завершающим знаком)
    """
    sentences: List[str] = []
    current = []
    i = 0

    while i < len(text):
        ch = text[i]
        current.append(ch)

        if ch in markers:
            sentences.append(''.join(current))
            current = []

            i += 1
            # пропускаем все пробелы после конца предложения
            while i < len(text) and text[i].isspace():
                i += 1
            continue

        i += 1

    if current:
        sentences.append(''.join(current))

    return sentences


def extract_spaces(text: str, markers: Tuple[str, ...] = end_of_sentence_symbols) -> List[str]:
    """
    Извлекает пробелы после каждого конца предложения.
    Используется при дешифровании.
    """
    spaces: List[str] = []
    i = 0

    while i < len(text):
        if text[i] in markers:
            i += 1
            buf = []

            while i < len(text) and text[i].isspace():
                buf.append(text[i])
                i += 1

            spaces.append(''.join(buf))
        else:
            i += 1

    return spaces


def put_end_marker(message_len: int, sentences: List[str], end_marker:str = None) -> List[str]:
    """
    Вставляет маркер конца сообщения в список предложений
    """
    if message_len < 0:
        raise ValueError("Длина сообщения должна быть неотрицательной")

    if len(sentences) < message_len + 1:
        raise ValueError("Контейнер слишком мал для размещения сообщения")

    if end_marker is None:
        end_marker = end_marker_const

    return sentences[:message_len] + [end_marker] + sentences[message_len:]


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
    container_capacity = max(len(sentences) - 1, 0)

    message_bits = text_to_bits(secret_text)
    message_length = len(message_bits)

    return LengthCheckResult(
        container_capacity=container_capacity,
        message_length=message_length,
        fits=message_length <= container_capacity
    )