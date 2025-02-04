from numpy.matrixlib.defmatrix import matrix
from saport.simplex.expressions.constraint import Constraint
from typing import List
# from .solver import Solver
from .expressions.variable import Variable
from .expressions.objective import Objective, ObjectiveType
import numpy as np


class Model:
    """
        A class to represent a linear programming problem.


        Attributes
        ----------
        name : str
            name of the problem
        variables : list[Variable]
            list with the problem variable, variable with index 'i' is always stored at the variables[i]
        constraints : list[Constraint]
            list containing problem constraints
        objective : Objective
            object representing the objective function

        Methods
        -------
        __init__(name: str) -> Model:
            constructs new model with a specified name
        create_variable(name: str) -> Variable:
            returns a new variable with a specified named, the variable is automatically indexed and added to the variables list
        add_constraint(constraint: Constraint)
            add a new constraint to the model
        maximize(expression: Expression)
            sets objective to maximize the specified Expression
        minimize(expression: Expression)
            sets objective to minimize the specified Expression
        solve() -> Solution
            solves the current model using Simplex solver and returns the result
            when called, the model should already contain at least one variable and objective
    """

    def __init__(self, name, variables=None, constraints=None, objective=None):
        self.name = name
        self.variables = variables or []
        self.constraints = constraints or []
        self.objective = objective

    def create_variable(self, name):
        for var in self.variables:
            if (var.name == name):
                raise Exception(f"There is already a variable named {name}")

        new_index = len(self.variables)
        variable = Variable(name, new_index)
        self.variables.append(variable)
        # self.constraints.append(variable >= 0)
        return variable

    @property
    def bounds_vector(self):
        return np.array([constraint.bound for constraint in self.constraints if constraint.is_polynomial()])

    @property
    def constraint_factors_matrix(self):
        constraint_vectors = [np.r_[constraint.factor_vector(self.variables)]
                              for constraint in self.constraints if constraint.is_polynomial()]
        return np.vstack(constraint_vectors)

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def maximize(self, expression):
        self.objective = Objective(expression, ObjectiveType.MAX)

    def minimize(self, expression):
        self.objective = Objective(expression, ObjectiveType.MIN)

    def _simplify(self):
        self.constraints = [c.simplify() for c in self.constraints]
        self.objective = self.objective.simplify()

    def solve(self, solver):
        if len(self.variables) == 0:
            raise Exception("Can't solve a model without any variables")

        if self.objective == None:
            raise Exception("Can't solve a model without an objective")

        self._simplify()
        # solver = Solver()
        return solver.solve(self)

    def __str__(self):
        separator = '\n\t'
        text = f'''- name: {self.name}
- variables: {", ".join([v.name for v in self.variables])}
- constraints:{separator}{separator.join([str(c) for c in self.constraints])}
- objective:{separator}{self.objective}
'''
        return text
