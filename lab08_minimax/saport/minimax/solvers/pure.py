from dataclasses import dataclass
from .solver import AbstractSolver
from ..model import Game, Equilibrium, Strategy
from typing import List
import numpy as np


class PureSolver(AbstractSolver):

    def solve(self) -> List[Equilibrium]:

        # TODO: basic solver finding all pure equilibriums
        #      reminder:
        #      if max of the column is the same as min of the row
        #      it is an equilibrium
        #      in case there is no pure equilibrium - should return an empty list

        self.game.reward_matrix
        eqiulibriums = []
        for bob_action in self.game.reward_matrix.T:
            alice_strategy, alice_value, alice_action_ind = self._find_strategy(bob_action, max)
            bob_strategy, bob_value, _ = self._find_strategy(self.game.reward_matrix[alice_action_ind], min)
            if alice_value == bob_value:
                eqiulibriums.append(Equilibrium(bob_value, alice_strategy, bob_strategy))
        return eqiulibriums

    def _find_strategy(self, choices: np.array, cost_function):
        best_action_ind = np.where(choices == cost_function(choices))[0][0]
        action_award = choices[best_action_ind]
        probabilities = [0] * len(choices)
        probabilities[best_action_ind] = action_award
        return Strategy(probabilities), action_award, best_action_ind
