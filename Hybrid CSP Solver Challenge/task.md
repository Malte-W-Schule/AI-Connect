Overview
AI Connect 2025 – CSP Solver Challenge
Teaser
Hello students,
Ready to connect across continents and put your AI fundamentals into practice? AI Connect is a collaborative, student-centered project week co-hosted by HSBI (Germany), TDU (Türkiye), SEECS/NUST (Pakistan), and CST/RUB (Bhutan).

You will work in small, mixed teams (6–8 members), establish your ways of working, and create a 2-minute video to showcase your solution.

Start

7 days ago
Close
4 days to go
Description
Objective
Participants must build a CSP solver that combines:

A symbolic CSP solver for logic grid puzzles (e.g., Zebra puzzles).
Teams will compete on accuracy, efficiency, and generalization.
Dataset
ZebraLogicBench dataset: ~1,000 logic grid puzzles with varying sizes and clue sets.
(https://huggingface.co/datasets/allenai/ZebraLogicBench)
Each puzzle contains:
List of entities (e.g., people, pets, colors)
Clues in natural language
Ground-truth solution
- Structured JSON representation
Competition Timeline (11 days)
Week	Milestone
1	Set up CSP solver & data loader; parse puzzles into CSP format
1	Generate solver traces (search states + decisions)
2	evaluate on validation set
| 2 | Final evaluation on held-out test puzzles (Uploaded on Kaggle); report and video presentation (to be submitted on LMS) |
Data Parsing
Read ZebraLogicBench, extract puzzles into CSP variables, domains, and constraint lists
Example: houses, attributes, clues like “Alice lives in the red house”
Baseline Symbolic Solver
Backtracking CSP solver with MRV, forward checking, and arc consistency
Demonstrates solving small puzzles end-to-end
Trace Generator Script
Logs feature vectors at each decision (domain sizes, constraints, chosen variable/value)
Outputs structured traces for training
Evaluation Notebook
Runs your solver on validation/test sets
Computes Accuracy (correct puzzle solutions), Efficiency (search steps), Generalization (performance on unseen puzzle sizes)
Evaluation
Leaderboard and Evaluation
Composite Score: Your solution will be scored using the composite score:
Composite Score = Accuracy (%) – α × (AvgSteps / MaxAvgSteps)
Where:

Accuracy (%) = % of puzzles solved correctly.
AvgSteps = Average number of CSP search steps per puzzle.
MaxAvgSteps = Max value across all teams.
α = 10 is the efficiency penalty weight (scaling constant to balance speed vs correctness)
Rewards both correctness and solver efficiency
Submission
What to Submit
Jupyter notebooks or scripts:
Data parsing
Trace generation
Evaluation and analysis
Final Report:
Architecture overview
Experimental setup
Quantitative results (tables, charts)
Discussion and insights
Video: 2-minute recorded demonstration of your solver
Submission files: .zip containing:
solver.py or notebook.ipynb – hybrid solver
run.py – script to run solver on test puzzles
README.md – explanation of approach
results.json – output for the test set
Example results.json: ```json { "puzzle_001": { "Person1": {"color": "red", "pet": "dog", "drink": "tea"}, "Person2": {…} }, … }