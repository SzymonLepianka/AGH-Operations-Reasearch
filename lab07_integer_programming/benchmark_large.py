from knapsack_benchmark import KnapsackBenchmark
from knapsack_benchmark import KnapsackBenchmark
from saport.knapsack.solverfactory import SolverType

problems = ["ks_82_0"]

benchmark = KnapsackBenchmark(problems)
benchmark.run()