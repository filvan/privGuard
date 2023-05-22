class BitUtil:

    def __init__(self):
        pass

    @staticmethod
    def check(number, index):
        return (number & (1 << index)) != 0

    @staticmethod

    def between(number, from_, to):
        return (number >> from_) & ((1 << to - from_) - 1)

    @staticmethod

    def from_(number, from_):
        return number >> from_

    @staticmethod

    def to(number, to):
        return BitUtil.between(number, 0, to)

    @staticmethod

    def between(number, from_, to):
        return (number >> from_) & ((1 << to - from_) - 1)

    @staticmethod

    def from_(number, from_):
        return number >> from_

    @staticmethod

    def to(number, to):
        return BitUtil.between(number, 0, to)
