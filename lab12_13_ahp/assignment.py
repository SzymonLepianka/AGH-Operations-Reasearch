from __future__ import annotations
import ahp
from dataclasses import dataclass
import numpy as np
from typing import Tuple


@dataclass
class RankingSolution:
    rankings: Tuple[np.Array]
    preference_ranking: np.Array
    global_ranking: np.Array
    choice: int


@dataclass
class ConsistencySolution:
    saaty: float
    koczkodaj: float


def ranking_assignment():
    Cs = (
        ahp.read_comparison_matrix("1/7,1/5;3"),
        ahp.read_comparison_matrix("5,9;4"),
        ahp.read_comparison_matrix("4,1/5;1/9"),
        ahp.read_comparison_matrix("9,4;1/4"),
        ahp.read_comparison_matrix("1,1;1"),
        ahp.read_comparison_matrix("6,4;1/3"),
        ahp.read_comparison_matrix("9,6;1/3"),
        ahp.read_comparison_matrix("1/2,1/2;1")
    )
    c_p = ahp.read_comparison_matrix("4,7,5,8,6,6,2;5,3,7,6,6,1/3;1/3,5,3,3,1/5;6,3,4,1/2;1/3,1/4,1/7;1/2,1/5;1/5")

    # calculate for both metods
    # - ranking for every comparison matrix
    # - ranking of the preferences comparison matrix
    # - global ranking of alternative
    # - chosen alternative according to the global ranking
    # Use methods from modle ahp, remember to fill the #tod section
    evm_rankings = []
    for i in Cs:
        evm_rankings.append(ahp.evm(i))

    evm_p_ranking = ahp.evm(c_p)

    evm_global_ranking = []
    for i in range(len(evm_rankings[0])):
        tmp = 0
        for j in range(len(evm_rankings)):
            tmp += evm_p_ranking[j] * evm_rankings[j][i]
        evm_global_ranking.append(tmp)

    evm_choice = evm_global_ranking.index(max(evm_global_ranking))

    evm_solution = RankingSolution(evm_rankings, evm_p_ranking, evm_global_ranking, evm_choice)

    gmm_rankings = []
    for i in Cs:
        gmm_rankings.append(ahp.gmm(i))

    gmm_p_ranking = ahp.gmm(c_p)

    gmm_global_ranking = []
    for i in range(len(gmm_rankings[0])):
        tmp = 0
        for j in range(len(gmm_rankings)):
            tmp += gmm_p_ranking[j] * gmm_rankings[j][i]
        gmm_global_ranking.append(tmp)

    gmm_choice = gmm_global_ranking.index(max(gmm_global_ranking))

    gmm_solution = RankingSolution(gmm_rankings, gmm_p_ranking, gmm_global_ranking, gmm_choice)

    return evm_solution, gmm_solution


def consistency_assignment():
    Cs = (
        ahp.read_comparison_matrix("7,3;2"),
        ahp.read_comparison_matrix("1/5,7,1;1/2,2;3"),
        ahp.read_comparison_matrix("2,5,1,7;3,1/2,5;1/5,2;7")
    )

    # calculate for every matrix
    # - saaty index
    # - koczkodaj index
    # saaty_indexes should contain saaty index for each matrix
    # koczkodaj_indexes shold cotain koczkodaj index for each matrix 
    # Use methods from modle ahp, remember to fill the #TOD section
    saaty_indexes = []
    koczkodaj_indexes = []
    for i in Cs:
        saaty_indexes.append(ahp.saaty_index(i))
        koczkodaj_indexes.append(ahp.koczkodaj_index(i))

    return (ConsistencySolution(s, k) for s, k in zip(saaty_indexes, koczkodaj_indexes))
