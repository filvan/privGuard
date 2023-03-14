import re
from src.examples.program.Libretaxi.locales.english import *
def run(str_text):


    if len(str_text) > 300:
        return (validation_text_too_long + len(str_text))
    if len(str_text) < 20:
        return validation_text_too_short + len(str_text)
    charsToMatch = ("🚗","👋","🚘")
    if not str_text.startsWith(charsToMatch):
        return validation_prefix
    if str_text.__contains__("@"):
        return validation_no_at

    lowerText = str_text.lower()
    if lowerText.__contains__("fuck") | lowerText.__contains__("хуй")| lowerText.__contains__('пизда') | lowerText.__contains__('блядь'):
        return validation_no_offensive_language

    if lowerText.__contains__("http") | lowerText.__contains__("ftp://") | lowerText.__contains__("www"):
        return "🚫 No links please"

    if lowerText.__contains__(validation_dummy_addr_lowercase):
        return validation_change_from_to

    str_array = str_text.partition("\n")
    emptyCnt = 0
    totalCnt = 0
    for s in str_array:
        if len(s) == 0:
            emptyCnt = emptyCnt +1
        else:
            totalCnt = totalCnt +1
    if len(re.findall("\w\.[a-z]{2,5}",str_text)):
        return "🚫 No domains please"
    if emptyCnt > 2:
        return validation_empty_lines1 + emptyCnt
    if totalCnt > 9:
        return validation_empty_lines1 + totalCnt
    if totalCnt < 5:
        return validation_min_lines + totalCnt

    return ""

