import csv
import os
import json

HEADER = ["test_id", "grid_solution", "steps"]

def append_results_csv(filename, test_id, solved, steps, domains=None, houses=None, categories=None):
    file_exists = os.path.exists(filename)

    # build grid_solution
    if solved and domains is not None:
        header = ["House"] + [cat.__name__ for cat in categories]
        rows = []

        for h in sorted(houses, key=lambda x: x.value):
            row = [str(h.value)]
            for cat in categories:
                row.append(domains[h][cat][0].name.lower())
            rows.append(row)

        grid_solution = json.dumps({
            "header": header,
            "rows": rows
        })
    else:
        grid_solution = "failed"

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(HEADER)

        writer.writerow([test_id, grid_solution, steps])
