# Task 3 — Real-World Dataset Analysis Project

**Student:** Ramesh Singh Rajput  
**Course:** BCA 5th Semester  
**College:** Bhupal Nobles University, Udaipur  
**Project:** Student Performance Dataset Analysis

## Objective
Explore a public student-performance dataset, inspect its structure, clean data, perform exploratory data analysis (EDA), create visualizations, and summarize findings.

## Dataset source
UCI Machine Learning Repository — Student Performance dataset:
https://archive.ics.uci.edu/dataset/320/student+performance  
Citation: Cortez, P. (2008). *Student Performance* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T.

The original Mathematics file (`student-mat.csv`) contains 395 student records and 33 attributes. The script attempts to download the original file automatically. If internet access is unavailable, it runs with the included `student-mat-demo.csv` so the project can still be tested. **For final analysis results, confirm the script says “Original UCI data”; if it says “Bundled demo data”, add the original `student-mat.csv` to `data/` and rerun.**

## Project structure
- `analysis.py` — full analysis and visualization code
- `data/student-mat-demo.csv` — small offline demonstration dataset
- `requirements.txt` — required Python packages
- `outputs/` — generated results, charts, cleaned data and statistics (created after running)
- `Internship_Report.docx` and `Internship_Report.pdf` — report copies

## Run in VS Code
1. Install Python 3.10 or newer.
2. Extract the ZIP folder.
3. Open the extracted `Task3_Real_World_Dataset_Analysis` folder in VS Code.
4. Open Terminal → New Terminal.
5. Run: `python -m pip install -r requirements.txt`
6. Run: `python analysis.py`
7. Open the `outputs` folder to see the generated charts and CSV files.

If `python` does not work on Windows, try `py analysis.py`.

## Main analysis steps
1. Load and inspect rows, columns, data types, missing values, and duplicate records.
2. Remove duplicate rows and fill any missing numeric/categorical values appropriately.
3. Calculate descriptive statistics and grade counts.
4. Examine study time and absences in relation to final grade.
5. Create grade-distribution, study-time, absence, and grade-correlation charts.
6. Save reproducible outputs to the `outputs` directory.

## Limitations
Correlations do not prove causation. Student records are observational, and this analysis is educational only. Do not use results to make high-stakes decisions about individual students.
