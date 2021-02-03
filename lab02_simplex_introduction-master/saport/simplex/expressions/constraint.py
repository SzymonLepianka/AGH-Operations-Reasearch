from enum import Enum
from os import name
from typing import Callable


class ConstraintType(Enum):
    """
        An enum to represent a constraint type:
        - LE = less than or equal
        - EQ = equality
        - GR = greater than or equal
    """
    LE = -1
    EQ = 0
    GE = 1

    def __str__(self):
        return {
            ConstraintType.LE: "<=",
            ConstraintType.EQ: "=",
            ConstraintType.GE: ">="
        }[self]

    def __neg__(self):
        return {
            ConstraintType.LE: ConstraintType.GE,
            ConstraintType.GE: ConstraintType.LE,
            ConstraintType.EQ: ConstraintType.EQ
        }[self]


class Constraint:
    """
        A class to represent a constraint in the linear programming expression, e.g. 4x + 5y <= 13, etc.

        Attributes
        ----------
        expression : Expression
            polynomial expressions that is bounded
        bound : float
            a bound constraining the linear polynomial
        type: ConstraintType
            type of the constraint: LE, EQ, GE

        Methods
        -------
        __init__(expression: Expression, bound: float, type: ConstraintType = ConstraintType.GE) -> Constraint:
            constructs new constraint with a specified polynomial, bound and type
        simplify() -> Constraint:
            returns new constraint with the simplified polynomial
    """
    def __init__(self, expression, bound, type=ConstraintType.GE, artificial_variable=None, extra_variable=None):
        if bound < 0:
            raise Exception("The abort linear solver doesn't support negative bounds")
        self.expression = expression
        self.bound = bound
        self.type = type
        self.extra_variable = extra_variable
        self.artificial_variable = artificial_variable

    def is_polynomial(self):
        return len(self.expression.atoms) > 1

    def factor_vector(self, variables):
        return self.expression.factor_vector(variables)

    def normalize(self, variable_factory: Callable[[str], 'Variable']):
        expression = None
        artificial_variable = None
        extra_variable = None
        if self.bound < 0:
            self._reverse()
        if self.type is ConstraintType.EQ:
            # artificial_variable = variable_factory('R')
            expression = self.expression # + artificial_variable
        elif self.type is ConstraintType.GE:
            # artificial_variable = variable_factory('R')
            extra_variable = surpuls_variable = variable_factory('s')
            expression = self.expression - surpuls_variable # + artificial_variable
        elif self.type is ConstraintType.LE:
            extra_variable = slack_variable = variable_factory('s')
            expression = self.expression + slack_variable
        return Constraint(expression, self.bound, ConstraintType.EQ, artificial_variable, extra_variable)

    def _reverse(self):
        (self.expression, self.bound, self.type) = (-self.expression, -self.bound, -self.type)

    def simplify(self):
        return Constraint(self.expression.simplify(), self.bound, self.type)

    def __str__(self):
        return f"{self.expression} {self.type} {self.bound}"