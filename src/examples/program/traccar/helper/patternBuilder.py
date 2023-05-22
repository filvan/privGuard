import re


class PatternBuilder:

    def __init__(self):

        self._fragments = []




    def optional(self):
        return self.optional(1)


    def optional(self, count):
        self._fragments.insert(len(self._fragments) - count, "(?:")
        self._fragments.append(")?")
        return self

    def expression(self, s):
        s = s.replaceAll("\\|$", "\\\\|")

        self._fragments.append(s)
        return self

    def text(self, s):
        self._fragments.append(s.replaceAll("([\\\\.\\[{()*+?^$|])", "\\\\$1"))
        return self

    def number(self, s):
        s = s.replace("dddd", "d{4}").replace("ddd", "d{3}").replace("dd", "d{2}")
        s = s.replace("xxxx", "x{4}").replace("xxx", "x{3}").replace("xx", "x{2}")

        s = s.replace("d", "\\d").replace("x", "[0-9a-fA-F]").replaceAll("([.])", "\\\\$1")
        s = s.replaceAll("\\|$", "\\\\|").replaceAll("^\\|", "\\\\|")

        self._fragments.append(s)
        return self

    def any(self):
        self._fragments.append(".*")
        return self

    def binary(self, s):
        self._fragments.append(s.replaceAll("(\\p{XDigit}{2})", "\\\\$1"))
        return self

    def or_(self):
        self._fragments.append("|")
        return self

    def groupBegin(self):
        return self.expression("(?:")


    def groupEnd(self):
        return self.expression(")")


    def groupEnd(self, s):
        return self.expression(")" + s)

    def compile(self):
        return re.Pattern.compile(self.toString(), re.Pattern.DOTALL)

    def toString(self):
        builder = ""
        for fragment in self._fragments:
            builder += (fragment)
        return str(builder)
