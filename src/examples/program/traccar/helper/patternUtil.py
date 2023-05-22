import re


class PatternUtil:

    _LOGGER =" LoggerFactory.getLogger(PatternUtil.class)"

    def __init__(self):
        pass

    class MatchResult:

        def __init__(self):
            #instance fields found by Java to Python Converter:
            self._patternMatch = None
            self._patternTail = None
            self._stringMatch = None
            self._stringTail = None


        def getPatternMatch(self):
            return self._patternMatch

        def getPatternTail(self):
            return self._patternTail

        def getStringMatch(self):
            return self._stringMatch

        def getStringTail(self):
            return self._stringTail

    @staticmethod
    def checkPattern(pattern, input):

        if not str("ManagementFactory.getRuntimeMXBean().getInputArguments()").contains("-agentlib:jdwp"):
            raise Exception("PatternUtil usage detected")

        result = "MatchResult()"

        i = 0
        while i < len(pattern):
            try:
                matcher = re.Pattern.compile("(" + pattern[0:i] + ")[\\s\\S]*").matcher(input)
                if matcher.matches():
                    result.patternMatch = pattern[0:i]
                    result.patternTail = pattern[i:]
                    result.stringMatch = matcher.group(1)
                    result.stringTail = input[matcher.group(1).length():]
            except Exception as error:
                PatternUtil._LOGGER.warn("Pattern matching error", error)
            i += 1

        return result
