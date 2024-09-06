import re


def capfirst(x):
    """Capitalize the first letter of a string. Kindly borrowed from Django"""
    return x and str(x)[0].upper() + str(x)[1:]


def get_subject(text):
    """Generate subject based on message text"""
    words = [word.lower() for word in re.split(r'\s+', text)]
    words[0] = capfirst(words[0])

    if len(words) > 1:
        if len(words) in [2, 3]:
            return ' '.join(words[:3])

        return ' '.join(words[:3]) + '...'

    if len(words[0]) < 32:
        return words[0][:32]

    return words[0][:32] + '...'  # first 32 characters
