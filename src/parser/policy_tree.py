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

""" Syntax tree of Legalease policy. """

from typing import List
from copy import deepcopy
from src.parser.attribute import Attribute, Satisfied, Unsatisfiable, FilterAttribute, SchemaAttribute, \
    PrivacyAttribute, RedactAttribute, PurposeAttribute, AlertAttribute
from src.parser.typed_value import ExtendV
from src.parser.abstract_domain import ClosedIntervalL
from src.parser.policy_parser import policy_parser


class ConjunctClause:
    """
    A conjunctive clause of Attribute(s).
    """

    def __init__(self, attr_lst: List[Attribute]):
        """
        Initialize the conjunctive clause.

        Parameters
        ----------
        attr_lst : List[Attribute]
            List of attributes to include in the poset.
        """

        if not isinstance(attr_lst, list):
            raise RuntimeError(f'Expect a list of attributes. Got: {attr_lst}')

        self.attr_lst = attr_lst

    def __iter__(self):
        """
        Iterate over the Attributes in the conjunctive clause.
        """

        return iter(self.attr_lst)

    def __str__(self):

        return f'ConjunctClause({", ".join([str(x) for x in self.attr_lst])})'

    __repr__ = __str__

    def copy(self):
        return ConjunctClause(self.attr_lst.copy())

    def list_attr(self):
        return self.attr_lst.copy()

    def add(self, req):
        """
        Add an Attribute to the conjunctive clause. If the Attribute is less 
        strict than an existing Attribute in the conjunctive clause, drop it.

        Parameters
        ----------
        req : Attribute
            New element to include in the conjunctive clause.
        """

        newClause = []
        flag = False
        for x in self.attr_lst:
            if x.is_stricter_than(req):
                flag = True
            newClause.append(x)

        if not flag:
            newClause.append(req)

        return ConjunctClause(newClause)


class DNF:
    """
    A disjunctive normal form to represent a policy.
    """

    def __init__(self, cc_lst: List[ConjunctClause]):
        """
        Initialize the disjunctive normal form.

        Parameters
        ----------
        cc_lst : List[ConjunctClause]
            List of conjunctive clauses to include in the set.
        """

        self.cc_lst = cc_lst

    def __iter__(self):
        """
        Iterate over the conjunctive clauses in the disjunctive normal form.
        """

        return iter(self.cc_lst)

    def __str__(self):
        return f'DNF({", ".join([str(x) for x in self.cc_lst])})'

    __repr__ = __str__

    def copy(self):
        return DNF(self.cc_lst.copy())

    def add(self, clause: ConjunctClause):
        """
        Add a clause to the disjunctive normal form. If the clause is subsumed, drop it.

        Parameters
        ----------
        clause : ConjunctClause
            A new clause to include in the disjunctive normal form.
        """

        subsumed = any([all([any([r1.is_stricter_than(r2) for r1 in c1]) for r2 in clause]) for c1 in self.cc_lst])
        if not subsumed:
            self.cc_lst.append(clause)


def clause2DNF(clause):
    """
    Convert a policy clause returned by the policy parser to disjunctive normal form (DNF).

    Parameters
    ----------
    clause : List
        A nested list of Attributes, 'AND' or 'OR'.

    Returns
    ----------
    result : list[list[Attribute]]
        The policy in DNF.
    """

    if isinstance(clause, Attribute):
        return [[clause]]
    elif clause[1] == 'AND':
        lhs = clause2DNF(clause[0])
        rhs = clause2DNF(clause[2])
        result = []
        for lvalue in lhs:
            for rvalue in rhs:
                conjunct_value = deepcopy(lvalue)
                conjunct_value.extend(rvalue)
                result.append(conjunct_value)
        return result
    elif clause[1] == 'OR':
        lhs = clause2DNF(clause[0])
        rhs = clause2DNF(clause[2])
        lhs.extend(rhs)
        return lhs
    else:
        raise ValueError("Invalid input policy.")


def policy2DNF(policy_to_convert):
    """
    Convert a policy to disjunctive normal form (DNF)

    Parameters
    ----------
    policy_to_convert : List
        A list of clauses.

    Returns
    ----------
    result : list[list[Attribute]]
        The policy in DNF.
    """

    result = []
    for clause in policy_to_convert:
        result.extend(clause2DNF(clause))
    return result


class Policy(object):
    """
    A Legalease policy in PrivGuard.
    """

    def __init__(self, policy_parameter=None):
        """
        Initialize the policy object; flexible in the representation of the input policy.

        Parameters
        ----------
        policy_parameter : String | list | DNF
            The policy, represented as a string (surface syntax), list of clauses, or set.
        """

        p = None
        if isinstance(policy_parameter, str) and len(policy_parameter) > 0:
            p = policy2DNF(policy_parser.parseString(policy_parameter))
        elif isinstance(policy_parameter, list):
            p = policy_parameter
        elif isinstance(policy_parameter, DNF):
            self.policy = policy_parameter
            return
        elif not policy_parameter:
            self.policy = Policy([[Satisfied()]])
            return
        else:
            raise RuntimeError("Failed")

        self.policy = DNF([])
        for clause in p:
            self.policy.add(ConjunctClause(clause))

    def copy(self):
        return Policy(policy_parameter=self.policy.copy())

    def __str__(self):
        return ",\n  ".join([str(clause) for clause in self.policy])

    __repr__ = __str__

    def join(self, other):
        """
        *Join* two policies (i.e. take their least upper bound). The new policy is at
        least as strict as either of the two input policies.

        Parameters
        ----------
        other : Policy
            The policy to join with self.

        Returns
        ----------
        result : Policy
            The least upper bound of self and other
        """

        if other is None:
            return Policy(self.policy)

        assert isinstance(other, Policy)

        newPolicy = []
        newClause = []

        for c1 in self.policy:
            for c2 in other.policy:
                newClause = c1.copy()
                for req in c2:
                    newClause = newClause.add(req)
            newPolicy.append(newClause.attr_lst)

        return Policy(newPolicy).dealSat().dealUnsat()

    def runFilter(self, col, value, op):
        """
        Return a new policy based on the policy effects of a filter operation. This method
        should be run when the analysis program performs an operation like:

          filter(df, 'col' >= val)

        The updated policy will remove policy requirements which are satisfied by the filter
        operation. The above example would remove requirements that 'col' is greater than or
        equal to val.

        Parameters
        ----------
        col : String
            The column on whose value rows are filtered

        value : Val
            The value being compared to column values (usually a constant, string or 
            integer representation)

        op : String
            The filtering operation: one of 'eq', 'le', 'ge'

        Returns
        ----------
        result : Policy
            The updated policy after filtering.
        """

        newPolicy = [[self._runFilter(attr, col, value, op) for attr in clause] for clause in self.policy]
        return Policy(newPolicy).dealSat().dealUnsat()

    def _runFilter(self, attr: Attribute, col, value, op):

        if isinstance(attr, FilterAttribute) and attr.col == col:
            assert isinstance(value, (int, float, str))

            l = attr.interval.lower
            u = attr.interval.upper
            c = ExtendV(value)

            if op == 'eq':
                if l <= c <= u:
                    return Satisfied()
                else:
                    return Unsatisfiable()

            elif op == 'le':
                if c <= u:
                    if l == ExtendV('ninf'):
                        return Satisfied()
                    elif c < l:
                        return Unsatisfiable()
                    else:
                        newInterval = ClosedIntervalL(l, ExtendV('inf'))
                        return FilterAttribute(attr.col, newInterval)
                else:
                    return attr

            elif op == 'ge':
                if c >= l:
                    if u == ExtendV('inf'):
                        return Satisfied()
                    elif c > u:
                        return Unsatisfiable()
                    else:
                        newInterval = ClosedIntervalL(ExtendV('ninf'), u)
                        return FilterAttribute(attr.col, newInterval)
                else:
                    return attr

            # TODO: add support for le, neq, ge
            else:
                raise ValueError(f'Invalid operator: {op}')

        else:
            return attr

    def runProject(self, cols):
        """
        Return a new policy based on the policy effects of a project operation. This method
        should be run when the analysis program performs an operation like:

          project(df, ['col1', 'col2'])

        The updated policy will remove policy requirements which are satisfied by the projection
        operation. The above example would remove requirements that columns other than col1
        and col2 are redacted from the output.

        Parameters
        ----------
        cols : list[String]
            The columns being projected

        Returns
        ----------
        result : Policy
            The updated policy after projection
        """
        newPolicy = [[self._runProject(attr, cols) for attr in clause] for clause in self.policy]
        return Policy(newPolicy).dealSat().dealUnsat()

    def _runProject(self, attr, cols):
        if isinstance(attr, SchemaAttribute):
            new_cols = []
            flag = False
            for col in cols:
                if col in attr.cols():
                    new_cols.append(col)
                else:
                    flag = True
            if not new_cols:
                return Unsatisfiable()
            elif not flag:
                return Satisfied()
            else:
                return SchemaAttribute(new_cols)

        elif isinstance(attr, FilterAttribute):
            if attr.col not in cols:
                return Unsatisfiable()
            return attr

        elif isinstance(attr, RedactAttribute):
            if attr.col not in cols:
                return Satisfied()
            return attr

        else:
            return attr

    def runRedact(self, col, left=None, right=None):
        newPolicy = [[self._runRedact(attr, col) for attr in clause] for clause in self.policy]
        return Policy(newPolicy).dealSat().dealUnsat()

    def _runRedact(self, attr: Attribute, col, left=None, right=None):
        if isinstance(attr, RedactAttribute) and attr.col == col:
            if (left is None or left <= attr.slice[0]) and (right is None or right >= attr.slice[1]):
                return True
        return False

    def runPurpose(self, purpose, col):
        newPolicy = [self._runPurpose(clause, col, purpose) for clause in self.policy]
        return Policy(newPolicy).dealSat().dealUnsat()

    def _runPurpose(self, clause, col, purpose):
        attributes = []
        flag = False
        newClause = []
        for attribute in clause:
            if isinstance(attribute, SchemaAttribute):
                newClause.append(attribute)
                for attr in attribute.cols():
                    if attr in col:
                        attributes.append(attr)
                    else:
                        newClause.append(attribute)

            elif isinstance(attribute, PurposeAttribute):
                if attribute.purpose == purpose:
                    flag = True
            else:
                newClause.append(attribute)

        if flag & attributes.__len__():
            return newClause
        return clause.list_attr()

    def runPrivacy(self, priv_tech, **kwargs):
        newPolicy = [[self._runPrivacy(attr, priv_tech) for attr in clause] for clause in self.policy]
        return Policy(newPolicy).dealSat().dealUnsat()

    def _runPrivacy(self, attr: Attribute, priv_tech, **kwargs):
        if isinstance(attr, PrivacyAttribute) and attr.priv_tech == priv_tech:
            if priv_tech == 'k-anonymity':
                if kwargs['k'] >= attr.k:
                    return Satisfied()
            elif priv_tech == 'l-diversity':
                raise NotImplemented
            elif priv_tech == 't-closeness':
                raise NotImplemented
            elif priv_tech == 'DP':
                if kwargs['eps'] < attr.eps and kwargs['delta'] < attr.delta:
                    return Satisfied()
            else:
                return Satisfied()
        return attr

    def dealUnsat(self):
        newPolicy = []
        for idx, clause in enumerate(self.policy):
            clause_flag = False
            for attr in clause:
                if isinstance(attr, Unsatisfiable):
                    clause_flag = True
                    break
            if not clause_flag:
                newPolicy.append(clause.attr_lst)
        if not newPolicy:
            newPolicy = [[Unsatisfiable()]]
        return Policy(newPolicy)

    def dealSat(self):
        newPolicy = []
        for clause in self.policy:
            newClause = []
            clause_flag = True
            for attr in clause:
                if not isinstance(attr, Satisfied):
                    clause_flag = False
                    newClause.append(attr)
            if clause_flag:
                newPolicy = [[Satisfied()]]
                break
            newPolicy.append(newClause)
        return Policy(newPolicy)

    def unSat(self, attr, **kwargs):
        newPolicy = []

        if attr == 'filter':
            col = kwargs.get('col')
        elif attr == 'privacy':
            priv_tech = kwargs.get('priv_tech')
        else:
            raise ValueError(f'Unsupported attribute: {attr}')

        for clause in self.policy:
            newClause = []
            for req in clause:
                if attr == 'filter' and isinstance(req, FilterAttribute) and req.col == col:
                    newClause.append(Unsatisfiable())
                elif attr == 'privacy' and isinstance(req, PrivacyAttribute) and req.priv_tech == priv_tech:
                    newClause.append(Unsatisfiable())
                else:
                    newClause.append(req)
            newPolicy.append(newClause)

        return Policy(newPolicy).dealUnsat()

    def isSat(self):
        if len(self.policy) == 1 and len(self.policy[0]) == 1 and isinstance(self.policy[0][0], Satisfied):
            return True
        return False

    def isUnsat(self):
        if len(self.policy) == 1 and len(self.policy[0]) == 1 and isinstance(self.policy[0][0], Unsatisfiable):
            return True
        return False


if __name__ == '__main__':
    # policy_str = "ALLOW FILTER age >= 18 AND (SCHEMA age OR (FILTER gender == 'M' AND (ROLE MANAGER OR FILTER age <= 90)))"
    # policy_str = "ALLOW ROLE Oncologist AND SCHEMA age, condition AND PRIVACY DP(1.0,1e-5) AND FILTER age > 18 AND REDACT zip(2:) AND PURPOSE PublicInterest"
    # Test policy parsing

    # Test runFilter
    # print(policy.runFilter('age', 18, 'ge'))
    # print(policy.runPurpose('BUSINESS', ['age']))
    # print(policy.runFilter('age', 17, 'le'))

    # TODO: Test runProject
    # print(policy.runProject(['age']))
    # print(policy.runProject(['age', 'gender','purpose']))
    # print(policy.runProject(['gender']))

    policy_str = input("Please input a valid Legalease policy: \n")
    policy = Policy(policy_str)
    print(policy)
