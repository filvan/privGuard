import re


def run(str_text, locales):
    if len(str_text) > 300:
        return locales.validation_text_too_long + len(str_text)
    if len(str_text) < 20:
        return locales.validation_text_too_short + len(str_text)
    chars_to_match = ("🚗", "👋", "🚘")
    if not str_text.startsWith(chars_to_match):
        return locales.validation_prefix
    if str_text.__contains__("@"):
        return locales.validation_no_at

    lower_text = str_text.lower()
    if lower_text.__contains__("fuck") | lower_text.__contains__("хуй") | lower_text.__contains__(
            'пизда') | lower_text.__contains__('блядь'):
        return locales.validation_no_offensive_language

    if lower_text.__contains__("http") | lower_text.__contains__("ftp://") | lower_text.__contains__("www"):
        return "🚫 No links please"

    if lower_text.__contains__(locales.validation_dummy_addr_lowercase):
        return locales.validation_change_from_to

    str_array = str_text.partition("\n")
    empty_cnt = 0
    total_cnt = 0
    for s in str_array:
        if len(s) == 0:
            empty_cnt = empty_cnt + 1
        else:
            total_cnt = total_cnt + 1
    if len(re.findall("\w\.[a-z]{2,5}", str_text)):
        return "🚫 No domains please"
    if empty_cnt > 2:
        return locales.validation_empty_lines1 + empty_cnt
    if total_cnt > 9:
        return locales.validation_empty_lines1 + total_cnt
    if total_cnt < 5:
        return locales.validation_min_lines + total_cnt

    return ""
