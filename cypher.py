# cypher.py
from typing import List, Dict
from constants import cypher_maps, decypher_maps, end_of_line_symbol, Mode


def cypher(split_container:List[str], message: List[int], number_of_bits: int = 1,
           eol_symbol:str = None, mode:Mode = Mode.REGULAR_SPACES) -> List[str]:
    """
    Шифрует текст посредством вставки пробелов
    """
    if mode is Mode.REGULAR_SPACES and number_of_bits > 1:
        raise ValueError("Метод обыкновенных пробелов поддерживает только один шифруемый символ на предложение.")

    cypher_map = cypher_maps[mode]

    if eol_symbol is None:
        eol_symbol = end_of_line_symbol

    result: List[str] = []

    i, j = 0, 0
    while i < len(split_container):
        sentence = split_container[i]

        for _ in range(number_of_bits):
            if j < len(message):
                bit = message[j]
                if bit not in cypher_map.keys():
                    raise ValueError(f"Некорректный бит: {bit}")

                sentence += cypher_map[bit]  # шифрующий символ
                j += 1

        sentence += eol_symbol
        result.append(sentence)
        i += 1


    return result


def decypher(spaces: List[str], number_of_bits: int = 1, mode:Mode = Mode.REGULAR_SPACES) -> List[int]:
    """
    Извлекает биты сообщения по количеству пробелов
    """
    if mode is Mode.REGULAR_SPACES and number_of_bits > 1:
        raise ValueError("Метод обыкновенных пробелов поддерживает только один шифруемый символ на предложение.")

    decypher_map = decypher_maps[mode]

    message: List[int] = []
    for space_sequence in spaces:

        if mode is Mode.REGULAR_SPACES:
            if space_sequence not in decypher_map.keys():  # прекращаем обработку, если встретили неизвестный символ
                raise ValueError(f"Некорректный символ: {space_sequence}")
            message.append(decypher_map[space_sequence])

        elif mode is Mode.NON_BREAKING_SPACES:
#            if len(space_sequence) != number_of_bits:
#                raise ValueError("Указанное количество шифруемых символов на строку не совпадает с фактическим.")
            for space in space_sequence:
                if space not in decypher_map.keys():  # прекращаем обработку, если встретили неизвестный символ
                    raise ValueError(f"Некорректный символ: {space}")
                message.append(decypher_map[space])

    return message
