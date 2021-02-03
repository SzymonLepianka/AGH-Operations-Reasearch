from dataclasses import dataclass
from numpy.core.defchararray import rindex
from .solver import AbstractSolver
from ..model import Game, Equilibrium, Strategy
from ...simplex import model as lpmodel
from ...simplex import solution as lpsolution
from ...simplex.expressions import expression as expr
import numpy as np
from typing import Tuple, List


class MixedSolver(AbstractSolver):

    def solve(self) -> Equilibrium:
        shifted_game, shift = self.shift_game_rewards()

        # don't remove this print, it will be graded :)
        print(f"- shifted game: \n{shifted_game}")

        a_model = self.create_max_model(shifted_game)
        b_model = self.create_min_model(shifted_game)
        a_solution = a_model.solve()
        b_solution = b_model.solve()

        a_probabilities = self.extract_probabilities(a_solution)
        b_probabilities = self.extract_probabilities(b_solution)

        # TODO: the correct Equilibirum instead of None

        return Equilibrium(a_solution.objective_value() - shift, Strategy(a_probabilities), Strategy(b_probabilities))

    def shift_game_rewards(self) -> Tuple[Game, float]:

        # TODO:
        # check if game value can be negative
        # if it's the case calculate the correct reward shift
        # to make it nonnegative

        opponents_costs = [min(col) for col in self.game.reward_matrix]
        shift = 0 if max(opponents_costs) > 0 else abs(max(opponents_costs))
        return Game(self.game.reward_matrix + shift), shift

    def create_max_model(self, game: Game) -> lpmodel.Model:

        # TODO:
        # one variable for game value
        # + as many variables as there are actions available for player A
        # sum of those variables should be equal 1
        # for each column, value - column * actions <= 0
        # maximize value variable

        a_actions, b_actions = game.reward_matrix.shape
        a_model = lpmodel.Model("A")
        game_value = a_model.create_variable("z")
        variables = np.array([a_model.create_variable(f"x{i}") for i in range(a_actions)])
        a_model.add_constraint(variables.sum() == 1)
        for column in game.reward_matrix.T:
            action_constraint = game_value + variables @ column * -1
            a_model.add_constraint(action_constraint <= 0)
        a_model.maximize(game_value)
        return a_model

    def create_min_model(self, game: Game) -> lpmodel.Model:

        # TODO:
        # one variable for game value
        # + as many variables as there are actions available for playerBA
        # sum of those variables should be equal 1
        # for each row, value - row * actions >= 0
        # minimize value variable

        a_actions, b_actions = game.reward_matrix.shape
        b_model = lpmodel.Model("B")
        game_value = b_model.create_variable("z")
        variables = np.array([b_model.create_variable(f"x{i}") for i in range(b_actions)])
        b_model.add_constraint(variables.sum() == 1)
        for column in game.reward_matrix:
            action_constraint = game_value + variables @ column * -1
            b_model.add_constraint(action_constraint >= 0)
        b_model.minimize(game_value)
        return b_model

    def extract_probabilities(self, solution: lpsolution.Solution) -> List[float]:
        return [solution.value(x) for x in solution.model.variables if not solution.model.objective.depends_on_variable(solution.model, x)]
