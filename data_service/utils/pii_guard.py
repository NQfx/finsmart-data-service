import re
import phonenumbers
import stdnum.ru
from natasha import NewsNERTagger

def detect_pii(text: str) -> str:
    pass

def luhn(string: str) -> bool:
    digits = string.replace(" ", "")

    if not digits or not digits.isdigit():
        return False

    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d

    return total % 10 == 0

def mod97(string: str) -> bool:
    if not isinstance(string, str):
        return False

    iban = re.sub(r"\s+", "", string).upper()

    if len(iban) < 4 or not re.fullmatch(r"[A-Z0-9]+", iban):
        return False

    rearranged = iban[4:] + iban[:4]
    remainder = 0

    for ch in rearranged:
        if ch.isdigit():
            value = int(ch)
            remainder = (remainder * 10 + value) % 97
        else:
            value = ord(ch) - ord("A") + 10
            remainder = (remainder * 100 + value) % 97

    return remainder == 1

def is_ogrn(string: str) -> bool:
    pass

def is_inn(string: str) -> bool:
    pass



def getNERobjects(text: str) -> [str]:
    """Использует модель NewsNERTagger из проекта Natasha для 
    поиска имен, организаций и адресов в тексте"""
    tagger = NewsNERTagger()
    pass