import numpy as np
from .model import AssignmentProblem, Assignment, NormalizedAssignmentProblem
from ..simplex.model import Model
from ..simplex.expressions.expression import Expression
from dataclasses import dataclass
from typing import List


class Solver:
    """
    A simplex solver for the assignment problem.

    Methods:
    --------
    __init__(problem: AssignmentProblem):
        creates a solver instance for a specific problem
    solve() -> Assignment:
        solves the given assignment problem
    """

    def __init__(self, problem: AssignmentProblem):
        self.problem = NormalizedAssignmentProblem.from_problem(problem)

    def solve(self) -> Assignment:
        model = Model("assignment")

        # 1) creates variables, one for each cost in the cost matrix
        # 2) add constraint, that sum of every row has to be equal 1
        # 3) add constraint, that sum of every col has to be equal 1
        # 4) add constraint, that every variable has to be <= 1
        # 5) create an objective expression, involving all variables weighted by their cost
        # 6) add the objective to model (minimize it!)

        ilosc_wierszy = len(self.problem.costs)
        ilosc_kolumn = len(self.problem.costs[0])
        xs = [[model.create_variable(f'x{i, j}') for j in range(ilosc_kolumn)] for i in range(ilosc_wierszy)]

        for i in range(ilosc_wierszy):
            constraint = Expression()
            for j in range(ilosc_kolumn):
                constraint += xs[i][j]
            model.add_constraint(constraint == 1)

        for j in range(ilosc_kolumn):
            constraint = Expression()
            for i in range(ilosc_wierszy):
                constraint += xs[i][j]
            model.add_constraint(constraint == 1)

        for i in range(ilosc_wierszy):
            for j in range(ilosc_kolumn):
                model.add_constraint(xs[i][j] <= 1)

        obj = Expression()
        for i in range(ilosc_wierszy):
            for j in range(ilosc_kolumn):
                obj += xs[i][j] * self.problem.costs[i][j]
        model.minimize(obj)

        solution = model.solve()

        # 1) extract assignment for the original problem from the solution object
        # tips:
        # - remember that in the original problem n_workers() not alwyas equals n_tasks()

        assigned_tasks = [-1] * len(self.problem.original_problem.costs)
        objective = 0
        for i in range(len(self.problem.original_problem.costs)):
            for j in range(len(self.problem.original_problem.costs[0])):
                if solution.assignment[i * ilosc_wierszy + j] == 1:
                    assigned_tasks[i] = j
                    objective += self.problem.original_problem.costs[i][j]

        return Assignment(assigned_tasks, objective)
