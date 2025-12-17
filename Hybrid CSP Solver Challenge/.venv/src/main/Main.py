from data_parser import DataParser
from Ac3 import AC3
import pandas as pd
import os
import re

dataparser = DataParser()

CSP_DOMAINS = dataparser.csp_domains
houses = dataparser.houses
constraints = dataparser.constraints

solver = AC3(dataparser.csp_domains, dataparser.constraints, dataparser.houses)
#solver.solve()

from BacktrackingSolver import BacktrackingSolver
backtracker = BacktrackingSolver(CSP_DOMAINS,constraints,houses)
backtracker.solve(use_ac3_preprocess=True)
solver.print_domains(CSP_DOMAINS)