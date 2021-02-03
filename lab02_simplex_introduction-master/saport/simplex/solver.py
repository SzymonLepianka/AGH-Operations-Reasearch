from copy import deepcopy
# from dataclasses import dataclass
from os import name
from saport.simplex.expressions.objective import Objective, ObjectiveType
from saport.simplex.expressions.constraint import Constraint
from typing import Container, List, Tuple
from saport.simplex.expressions import constraint
from saport.simplex.expressions.variable import Variable
import numpy as np
from saport.simplex.model import Model


class Solution:
    """
        A class to represent a solution to linear programming problem.


        Attributes
        ----------
        model : Model
            model corresponding to the solution
        assignment : list[float]
            list with the values assigned to the variables
            order of values should correspond to the order of variables in model.variables list


        Methods
        -------
        __init__(model: Model, assignment: list[float]) -> Solution:
            constructs a new solution for the specified model and assignment
        value(var: Variable) -> float:
            returns a value assigned to the specified variable
        objective_value()
            returns value of the objective function
    """

    def __init__(self, model, assignment):
        "Assignment is just a list of values"
        self.assignment = assignment
        self.model = model

    def value(self, var):
        return self.assignment[var.index]

    def objective_value(self):
        return self.model.objective.evaluate(self.assignment)

    def __str__(self):
        text = f'- objective value : {self.objective_value()}\n'
        text += '- assignment :'
        for (i, var) in enumerate(self.assignment):
            text += f' {self.model.variables[i].name} = {var};'
        return text


class Tableu:
    pass


class Solver:
    """
        A class to represent a simplex solver.

        Methods
        -------
        solve(model: Model) -> Solution:
            solves the given model and return the first solution
    """

    # def __init__(self) -> None:
    #     self._extra_variables: List[ExtraVariable] = []

    def solve(self, model):
        normal_model = self._normalize_model(deepcopy(model))
        solution, basis_vector = self._find_initial_solution(normal_model)
        tableaux = self._tableux(normal_model, solution, basis_vector)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print(normal_model)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print(solution)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        # print(tableaux)
        self._print_tableaux(normal_model, tableaux)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return solution

    def _print_tableaux(self, model, tableaux):
        title = " | ".join(
            ["c_z    ", "Z.baz", *["%5.2s" % variable.name for variable in model.variables], 'Rozw.'])
        print(title)
        print('_ ' * int(len(title)/2))
        rows = [*[f'c{i}     ' for i in range(len(model.constraints)) if model.constraints[i].is_polynomial()],
                'z_j    ', 'c_j-z_j']
        for row_title, row in zip(rows, tableaux): print(" | ".join([row_title, *["%5.2f" % x for x in row]]))

    def _normalize_model(self, model: Model) -> Model:
        """
            _normalize_model(model: Model) -> Model:
                returns a normalized version of the given model 
        """

        """this method should create a new canonical model based on the current one
        # - canonical model has only the MAX objective
        # - canonical model has only EQ constraints (thanks to the additional slack / surplus variables)
        #   you should add extra (slack, surplus) variables and store them somewhere as the solver attribute
        """
        normalized_objective = model.objective.as_maximize()
        normalized_constraints = self._normalize_constraints(model)
        return Model("normalized model", model.variables, normalized_constraints, normalized_objective)

    def _normalize_constraints(self, model: Model) -> Tuple[List[Variable], List[Constraint]]:
        normalized_constraints = [*model.constraints]
        for index, constraint in enumerate(normalized_constraints):
            if constraint.is_polynomial():
                normalized_constraints[index] = constraint.normalize(
                    lambda name: self._variable_factory(model, index, name))
        return normalized_constraints

    def _variable_factory(self, model, index, name):
        return model.create_variable(f'{name}{index}')

    def _find_initial_solution(self, model: Model) -> Solution:
        """
        _find_initial_solution(model: Model) -> Solution
            returns an initial solution for the given model
        """
        """
        # - this method should find an initial feasible solution to the model
        # - should use the slack / surplus variables added during the normalization
        """
        artificial_variables = [constraint.artificial_variable for constraint in model.constraints if
                                constraint.artificial_variable]
        extra_variables = [constraint.extra_variable for constraint in model.constraints if constraint.extra_variable]
        return self._solve_for_extra_variables(model, extra_variables)

    def _solve_for_extra_variables(self, model, extra_variables):
        assignment = [0] * len(model.variables)
        for constraint in model.constraints:
            if constraint.extra_variable:
                assignment[constraint.extra_variable.index] = constraint.bound
        basis_vector = np.array([0] * len(extra_variables)).T
        return Solution(model, assignment), basis_vector

    def _solve_for_artificial_variables(self, model, artificial_variables):
        pass

    def _tableux(self, model: Model, solution: Solution, basis_vector):
        """
        _tableux(model: Model, solution: Solution) -> list[list[float]]
            returns a tableux for the given model and solution
        """
        """
        # this method should create an array (list of lists is fine, but you can cahnge it) 
        # representing the tableux for the given model and solution
        """
        constraints_factors = model.constraint_factors_matrix
        Z_j = np.array([np.dot(basis_vector, column.T) for column in constraints_factors.T])
        cost_vector = np.array((-model.objective.expression).factor_vector(model.variables) - Z_j)

        result = np.vstack([constraints_factors, Z_j, cost_vector])
        constant_term = model.bounds_vector
        # pivot_column = self._get_pivot_column(model.objective, cost_vector, constraints_factors)
        # rhs_ratio = constant_term / pivot_column
        return np.c_[np.r_[basis_vector, 0, 0], result, np.r_[constant_term, 0, model.objective.evaluate(solution.assignment)]]
        # np.c_[np.r_[basis_vector, 0, 0], result, np.r_[constant_term, 0, model.objective.evaluate(solution.assignment)], np.r_[rhs_ratio, 0, 0]]

    def _get_pivot_column(self, objective: Objective, cost_vector, constraints_factors):
        non_zero_values = cost_vector[np.where(cost_vector != 0)]
        if objective.type is ObjectiveType.MAX:
            col_index = np.where(non_zero_values == max(non_zero_values))
        else:
            col_index = np.where(non_zero_values == min(non_zero_values))
        return constraints_factors[:, col_index[0][0]]
