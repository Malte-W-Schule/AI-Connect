from data_parser import DataParser
from BacktrackingSolver import BacktrackingSolver
from results_writer import append_results_csv

TOTAL_TESTS = 100
OUTPUT_FILE = "results.csv"

for i in range(TOTAL_TESTS):
    print(f"\n=== Solving testcase {i} ===")

    dataparser = DataParser(testcase=i)

    CSP_DOMAINS = dataparser.csp_domains
    houses = dataparser.houses
    constraints = dataparser.constraints

    backtracker = BacktrackingSolver(
        CSP_DOMAINS,
        constraints,
        houses
    )

    solved = backtracker.solve(use_ac3_preprocess=True)

    if solved:
        steps = backtracker.steps
        print(f"Testcase {i} solved in {steps} steps")
    else:
        steps = backtracker.steps
        print(f"Testcase {i} failed")

    append_results_csv(
        OUTPUT_FILE,
        f"test-{i:03}",
        solved,
        steps,
        domains=CSP_DOMAINS,
        houses=houses,
        categories=dataparser.categories
    )

print("\n=== ALL DONE ===")
print("results.csv GENERATED")
