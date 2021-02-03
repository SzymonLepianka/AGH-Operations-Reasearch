from ..abstractsolver import AbstractSolver
from ..model import Problem, Solution, Item
from typing import List
from ...integer.model import Model
from ...simplex.expressions.expression import Expression


class IntegerSolver(AbstractSolver):
    """
    An Integer Programming solver for the knapsack problems

    Methods:
    --------
    create_model() -> Models:
        creates and returns an integer programming model based on the self.problem
    """

    def create_model(self) -> Model:
        model = Model("knapsack problem model")
        items = self.problem.items
        variables = [model.create_variable(f"x{i}") for i in range(len(items))]
        weight_sum = Expression()
        value_sum = Expression()
        for i, variable in enumerate(variables):
            weight_sum += variable * items[i].weight
            value_sum += variable * items[i].value
            model.add_constraint(variable <= 1)
        model.add_constraint(weight_sum <= self.problem.capacity)
        model.maximize(value_sum)
        return model

    def solve(self) -> Solution:
        m = self.create_model()
        integer_solution = m.solve(self.timelimit)
        items = [item for (i, item) in enumerate(
            self.problem.items) if integer_solution.value(m.variables[i]) > 0]
        solution = Solution.from_items(items, not m.solver.interrupted)
        self.total_time = m.solver.total_time
        return solution
