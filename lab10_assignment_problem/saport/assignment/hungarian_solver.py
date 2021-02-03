import numpy as np
from .model import Assignment, AssignmentProblem, NormalizedAssignmentProblem
from typing import List, Dict, Tuple, Set


class Solver:
    """
    A hungarian solver for the assignment problem.

    Methods:
    --------
    __init__(problem: AssignmentProblem):
        creates a solver instance for a specific problem
    solve() -> Assignment:
        solves the given assignment problem
    extract_mins(costs: np.Array):
        substracts from columns and rows in the matrix to create 0s in the matrix
    find_max_assignment(costs: np.Array) -> Dict[int,int]:
        finds the biggest possible assinments given 0s in the cost matrix
        result is a dictionary, where index is a worker index, value is the task index
    add_zero_by_crossing_out(costs: np.Array, partial_assignment: Dict[int,int])
        creates another zero(s) in the cost matrix by crossing out lines (rows/cols) with zeros in the cost matrix,
        then substracting/adding the smallest not crossed out value
    create_assignment(raw_assignment: Dict[int, int]) -> Assignment:
        creates an assignment instance based on the given dictionary assignment
    """

    def __init__(self, problem: AssignmentProblem):
        self.problem = NormalizedAssignmentProblem.from_problem(problem)

    def solve(self) -> Assignment:
        costs = np.array(self.problem.costs)

        while True:
            self.extracts_mins(costs)
            max_assignment = self.find_max_assignment(costs)
            if len(max_assignment) == self.problem.size():
                return self.create_assignment(max_assignment)
            self.add_zero_by_crossing_out(costs, max_assignment)

    def extracts_mins(self, costs):

        # substract minimal values from each row and column

        ilosc_wierszy = len(costs)
        ilosc_kolumn = len(costs[0])
        for i in range(ilosc_wierszy):
            min_w_wierszu = costs[i][0]
            for j in range(ilosc_kolumn):
                if costs[i][j] < min_w_wierszu:
                    min_w_wierszu = costs[i][j]
            for j in range(ilosc_kolumn):
                costs[i][j] -= min_w_wierszu

        for j in range(ilosc_kolumn):
            min_w_kolumnie = costs[0][j]
            for i in range(ilosc_wierszy):
                if costs[i][j] < min_w_kolumnie:
                    min_w_kolumnie = costs[i][j]
            for i in range(ilosc_wierszy):
                costs[i][j] -= min_w_kolumnie

    def add_zero_by_crossing_out(self, costs: np.array, partial_assignment: Dict[int, int]):

        # 1) "mark" columns and rows according to the instructions given by teacher
        # 2) cross out marked columns and not marked rows
        # 3) find minimal uncrossed value and subtract it from the cost matrix
        # 4) add the same value to all crossed out columns and rows

        ilosc_wierszy = len(costs)
        ilosc_kolumn = len(costs[0])
        crossed = np.zeros_like(costs)
        for i in range(ilosc_wierszy):
            for j in range(ilosc_kolumn):
                if i in partial_assignment:
                    crossed[i][j] += 1
                if j in partial_assignment.values():
                    crossed[i][j] += 1

        minimal_uncrossed = -1
        for i in range(ilosc_wierszy):
            for j in range(ilosc_kolumn):
                if crossed[i][j] == 0:
                    if minimal_uncrossed == -1 or costs[i][j] < minimal_uncrossed:
                        minimal_uncrossed = costs[i][j]

        for i in range(ilosc_wierszy):
            for j in range(ilosc_kolumn):
                if crossed[i][j] == 0:
                    costs[i][j] -= minimal_uncrossed

        for i in range(ilosc_wierszy):
            for j in range(ilosc_kolumn):
                if crossed[i][j] == 2:
                    costs[i][j] += minimal_uncrossed

    def find_max_assignment(self, costs) -> Dict[int, int]:

        # find the bigest assignment in the cost matrix
        # 1) always try the row with the least amount of 0s
        # 2) then column with least amount of 0s
        # TIP: remember, rows and cols can't repeat in the assignment

        ilosc_wierszy = len(costs)
        ilosc_kolumn = len(costs[0])
        dictionary = {}
        crossed = np.zeros_like(costs)
        while True:
            minimalna_ilosc_zer_w_wierszu = ilosc_kolumn + 1
            indeks_wiersza = -1
            for i in range(ilosc_wierszy):
                if not i in dictionary:
                    biezaca_ilosc_zer_w_wierszu = 0
                    for j in range(ilosc_kolumn):
                        if costs[i][j] == 0 and crossed[i][j] == 0:
                            biezaca_ilosc_zer_w_wierszu += 1
                    if 0 < biezaca_ilosc_zer_w_wierszu < minimalna_ilosc_zer_w_wierszu:
                        minimalna_ilosc_zer_w_wierszu = biezaca_ilosc_zer_w_wierszu
                        indeks_wiersza = i

            minimalna_ilosc_zer_w_kolumnie = ilosc_wierszy + 1
            indeks_kolumny = -1
            for j in range(ilosc_kolumn):
                if j not in dictionary.values():
                    biezaca_ilosc_zer_w_kolumnie = 0
                    if costs[indeks_wiersza][j] == 0:
                        for i in range(ilosc_wierszy):
                            if costs[i][j] == 0 and crossed[i][j] == 0:
                                biezaca_ilosc_zer_w_kolumnie += 1
                        if 0 < biezaca_ilosc_zer_w_kolumnie < minimalna_ilosc_zer_w_kolumnie:
                            minimalna_ilosc_zer_w_kolumnie = biezaca_ilosc_zer_w_kolumnie
                            indeks_kolumny = j
            if indeks_kolumny == -1 or indeks_wiersza == -1:
                break
            dictionary[indeks_wiersza] = indeks_kolumny
            for i in range(ilosc_wierszy):
                for j in range(ilosc_kolumn):
                    if i == indeks_wiersza:
                        crossed[i][j] += 1
                    if j == indeks_kolumny:
                        crossed[i][j] += 1

        return dictionary

    def create_assignment(self, raw_assignment: Dict[int, int]) -> Assignment:

        # create an assignment instance based on the dictionary
        # tips:
        # 1) use self.problem.original_problem.costs to calculate the cost
        # 2) in case the original cost matrix (self.problem.original_problem.costs wasn't square)
        #    and there is more workers than task, you should assign -1 to workers with no task

        ilosc_wierszy = len(self.problem.original_problem.costs)
        ilosc_kolumn = len(self.problem.original_problem.costs[0])
        assigned_tasks = [-1] * ilosc_wierszy
        objective = 0
        for i in range(ilosc_wierszy):
            if i in raw_assignment:
                if raw_assignment[i] >= ilosc_kolumn:
                    assigned_tasks[i] = -1
                else:
                    assigned_tasks[i] = raw_assignment[i]
                    objective += self.problem.original_problem.costs[i][raw_assignment[i]]

        return Assignment(assigned_tasks, objective)
