class StringUtil:

    def __init__(self):
        pass

    @staticmethod
    def containsHex(value):
        for c in value.toCharArray():
            if c >= 'a' and c <= 'f' or c >= 'A' and c <= 'F':
                return True
        return False
