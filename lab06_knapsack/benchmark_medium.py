from knapsack_benchmark import KnapsackBenchmark


problems = ["ks_50_0", "ks_50_1", "ks_60_0", "ks_82_0", "ks_100_0", "ks_100_1", "ks_100_2"]
# "ks_82_0", "ks_100_0", "ks_100_1", "ks_100_2" - Unable to allocate

benchmark = KnapsackBenchmark(problems)
benchmark.run()
