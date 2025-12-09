import os
import pandas as pd
from tabulate import tabulate
from rich.console import Console
from rich.table import Table


# ANSI-Farbcodes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

showDataset = False

# Projekt-Root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

dataset_dir = os.path.join(project_root, "dataset", "grid_mode")  # dataset/grid_mode
files = [f for f in os.listdir(dataset_dir) if f.endswith(".parquet")]

df_list = [pd.read_parquet(os.path.join(dataset_dir, f)) for f in files]
df = pd.concat(df_list, ignore_index=True)

if df.head().empty:
    print("No data found")
else:

    # Headline Top
    print(f"\n{CYAN}{'#' * 50}{RESET}")
    print(f"\t{YELLOW}--- Data set correctly Loaded ---{RESET}")
    print(f"{CYAN}{'#' * 50}{RESET}\n")

    if showDataset:
        # show DataFrame
        print(tabulate(df.head(5), headers='keys', tablefmt='fancy_grid', showindex=False))

        # Headline Bottom
        print(f"\n{CYAN}{'#' * 50}{RESET}")
        print(f"\t{YELLOW}--- Data set correctly Loaded ---{RESET}")
        print(f"{CYAN}{'#' * 50}{RESET}\n")


