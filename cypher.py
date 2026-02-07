# cypher.py
from typing import List, Dict
from constants import cypher_map_const, decypher_map_const, end_marker_const


def cypher(split_container:List[str], message: List[int], end_marker: str = None,
           cypher_map:Dict[int, str] = None) -> List[str]:
    """
    Шифрует текст посредством вставки одиночных/двойных пробелов
    """
    if cypher_map is None:
        cypher_map = cypher_map_const

    if end_marker is None:
        end_marker = end_marker_const

    result: List[str] = []

    for i, sentence in enumerate(split_container):
        if sentence == end_marker:
            if i + 2 < len(split_container):
                result.append(split_container[i + 1])
                result.append(end_marker)
                result.extend(split_container[i + 2])
            else:
                raise ValueError("Текущее сообщение не поместится в контейнер.")

        result.append(sentence)

        if i < len(message):
            bit = message[i]
            if bit not in cypher_map.keys():
                raise ValueError(f"Некорректный бит: {bit}")

            result.append(cypher_map[bit])
        else:
            # если биты закончились — обычный одиночный пробел
            result.append(" ")

    return result


def decypher(spaces: List[str], end_marker:str = None, decypher_map:Dict[str, int] = None) -> List[int]:
    """
    Извлекает биты сообщения по количеству пробелов
    """
    if decypher_map is None:
        decypher_map = decypher_map_const

    if end_marker is None:
        end_marker = end_marker_const

    message: List[int] = []
    for space in spaces:
        if space == end_marker:
            break

        if space not in decypher_map.keys():
            break

        message.append(decypher_map[space])

    return message

