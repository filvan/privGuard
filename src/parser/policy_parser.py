# MIT License

# Copyright (c) 2021 sunblaze-ucb

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" The parser for Legalease policy. """

from pyparsing import oneOf, Word, Literal, pyparsing_common, Regex, Optional, Suppress, infix_notation, OneOrMore, \
    OpAssoc, nums, alphanums, delimitedList, Combine
from src.parser.typed_value import IntegerV, StringV, ExtendV
from src.parser.abstract_domain import ClosedIntervalL
from src.parser.attribute import RoleAttribute, PurposeAttribute, RedactAttribute, PrivacyAttribute, FilterAttribute, \
    SchemaAttribute, ArticleAttribute, ReferencesAttribute

# define basic parsers for tokens in the policy.
COMPARATOR = oneOf(['==', '!=', '>', '>=', '<', '<=']).setName('COMPARATOR')
COLUMN = Word(alphanums).setName('COLUMN')
INTEGER = Word(nums).setName('INTEGER').addParseAction(lambda toks: IntegerV(int(toks[0])))
SCALAR_INT = Word(nums).setName('SCALAR_INT').addParseAction(lambda toks: int(toks[0]))
SCALAR_FLOAT = pyparsing_common.fnumber
STRING = Regex("'(''|[^'])*'").setName('STRING').addParseAction(lambda toks: StringV(toks[0][1:-1]))
LIST = delimitedList(COLUMN)
VARIABLE = Word(alphanums).setName('VARIABLE')
ARTICLE_NAME = Regex(r"\d+((\(\d+\))(\([a-z]\))?)?").setName('ARTICLE_NAME')
ARTICLES_INTERVAL = Combine(ARTICLE_NAME + Optional(oneOf(['-', ' -', '- ', ' - ']) + ARTICLE_NAME)).setName('ARTICLES_INTERVAL')
ARTICLES_LIST = Combine(delimitedList(ARTICLES_INTERVAL, delim=', ', combine=True), adjacent=False).setName('ARTICLES_LIST')
COR = Combine(delimitedList(ARTICLE_NAME, delim=oneOf(['->', ' ->', '-> ', ' -> ']), combine=True), adjacent=False).setName('COR')


def filter_action(toks):
    """ How to parse a filter attribute. """
    col = toks[1]
    op = toks[2]
    interval = None
    if op == '==':
        interval = ClosedIntervalL(ExtendV(toks[3]), ExtendV(toks[3]))
    if op == '!=':
        raise NotImplemented("'!=' is currently not implemented. Please use '>=', '<=', '>', '<' to express '!='.")
    if op == '<=':
        interval = ClosedIntervalL(ExtendV('ninf'), ExtendV(toks[3]))
    if op == '>=':
        interval = ClosedIntervalL(ExtendV(toks[3]), ExtendV('inf'))
    if op == '<':
        if isinstance(toks[3], IntegerV):
            interval = ClosedIntervalL(ExtendV('ninf'), ExtendV(toks[3] - 1))
        else:
            raise NotImplemented("'<' is only implemented for integer types. Please try '<='.")
    if op == '>':
        if isinstance(toks[3], IntegerV):
            interval = ClosedIntervalL(ExtendV(toks[3] + 1), ExtendV('inf'))
        else:
            raise NotImplemented("'>' is only implemented for integer types. Please try '>='.")
    return FilterAttribute(col, interval, op)


def redact_action(toks):
    """ How to parse a redact attribute. """
    if len(toks) == 3:
        return RedactAttribute(toks[1])
    elif len(toks) == 4:
        if toks[2] == ':':
            return RedactAttribute(toks[1], (None, toks[3]))
        else:
            return RedactAttribute(toks[1], (toks[2], None))
    elif len(toks) == 5:
        return RedactAttribute(toks[1], (toks[2], toks[4]))


def schema_action(toks):
    """ How to parse a schema attribute. """
    return SchemaAttribute(toks[1:])


def privacy_action(toks):
    """ How to parse a privacy attribute. """
    if toks[1] == 'K-Anonymity':
        return PrivacyAttribute(toks[1], k=toks[2])
    elif toks[1] == 'L-Diversity':
        return PrivacyAttribute(toks[1], l=toks[2])
    elif toks[1] == 'T-Closeness':
        return PrivacyAttribute(toks[1], t=toks[2])
    elif toks[1] == 'DP':
        return PrivacyAttribute(toks[1], eps=toks[2], delta=toks[3])
    else:
        return PrivacyAttribute(toks[1])


def role_action(toks):
    """ How to parse a role attribute. """
    return RoleAttribute(toks[1])


def purpose_action(toks):
    """ How to parse a purpose attribute. """
    return PurposeAttribute(toks[1])


def article_action(toks):
    """ How to parse an article attribute. """
    return ArticleAttribute(toks[1])


def references_action(toks):
    """ How to parse a references attribute, i.e. a chain of references (COR). """
    return ReferencesAttribute(toks[1])


# parsers for attributes.
FILTER_ATTRIBUTE = ('FILTER' + COLUMN + COMPARATOR + (INTEGER | STRING)).addParseAction(filter_action)
REDACT_ATTRIBUTE = ('REDACT' + COLUMN + Suppress('(') + Optional(SCALAR_INT) + ':' + Optional(SCALAR_INT) + Suppress(
    ')')).addParseAction(redact_action)
SCHEMA_ATTRIBUTE = ('SCHEMA' + LIST).addParseAction(schema_action)
PRIVACY_ATTRIBUTE = ('PRIVACY' + (Literal('Anonymization') | Literal('Aggregation') | ('K-Anonymity' + SCALAR_INT) | (
        'L-Diversity' + SCALAR_INT) | ('T-Closeness' + SCALAR_INT) | (
                                          'DP' + Suppress('(') + SCALAR_FLOAT + Suppress(',') + SCALAR_FLOAT + Suppress(')')))).addParseAction(privacy_action)
ROLE_ATTRIBUTE = ('ROLE' + VARIABLE).addParseAction(role_action)
PURPOSE_ATTRIBUTE = ('PURPOSE' + VARIABLE).addParseAction(purpose_action)
ARTICLE_ATTRIBUTE = ('ARTICLE' + ARTICLES_LIST).addParseAction(article_action)
REFERENCES_ATTRIBUTE = ('REFERENCES' + Combine(delimitedList(COR, delim=', ', combine=True), adjacent=False)).addParseAction(references_action)
ATTRIBUTE = FILTER_ATTRIBUTE | REDACT_ATTRIBUTE | SCHEMA_ATTRIBUTE | PRIVACY_ATTRIBUTE | ROLE_ATTRIBUTE | PURPOSE_ATTRIBUTE | ARTICLE_ATTRIBUTE | REFERENCES_ATTRIBUTE

# the parser for clauses
CLAUSE = (Suppress('ALLOW') + infix_notation(ATTRIBUTE, [('AND', 2, OpAssoc.RIGHT), ('OR', 2, OpAssoc.RIGHT)]))

# the parser for policies
policy_parser = OneOrMore(CLAUSE)

if __name__ == '__main__':
    # policy_str = input("Please input a valid Legalease policy: \n")
    # print(policy_parser.parseString(policy_str))

    # Uncomment the below examples to test corresponding functionality of the parser.
    result = policy_parser.parseString("ALLOW FILTER age >= 18 AND SCHEMA NotPHI, h2 AND FILTER gender == 'M' ALLOW (FILTER gender == 'M' OR (FILTER gender == 'F' AND SCHEMA PHI))")
    print(result)
    # print(policy_parser.parseString("ALLOW SCHEMA HF2 AND (SCHEMA HF2 OR FILTER HR1 <= 8)"))
    # print(policy_parser.parseString("ALLOW ((ROLE guest OR SCHEMA NotHR1) OR SCHEMA NotHF2)"))

    # print(policy_parser.parseString("ALLOW REDACT HealthcareOrganization ( : )"))
    # print(policy_parser.parseString("ALLOW REDACT HealthcareOrganization ( 2 : )"))
    # print(policy_parser.parseString("ALLOW REDACT HealthcareOrganization ( : 2 )"))
    # print(policy_parser.parseString("ALLOW REDACT HealthcareOrganization ( 1 : 2 )"))

    # print(policy_parser.parseString("ALLOW PRIVACY Anonymization"))
    # print(policy_parser.parseString("ALLOW PRIVACY K-Anonymity 100"))
    # print(policy_parser.parseString("ALLOW PRIVACY DP ( 1.0, 1e-5 )"))
