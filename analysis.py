"""
Task 3: Real-World Dataset Analysis
Dataset: UCI Student Performance (Mathematics course)
Run: python analysis.py
The script tries to download the original public UCI data. If internet access is unavailable,
it uses the bundled demonstration CSV so the workflow can still be tested offline.
"""
from pathlib import Path
import urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "outputs"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)
REAL_URLS = [
    "https://huggingface.co/datasets/DElmazi/Student_Performance/resolve/main/student-mat.csv",
    "https://www.stat.cmu.edu/~brian/valerie/617-2022/617-2021/project01/UCI%20ML%20data%20sets/student%20performance/student-mat.csv",
]
real_path = DATA / "student-mat.csv"
demo_path = DATA / "student-mat-demo.csv"

def obtain_data():
    if real_path.exists():
        return real_path, True
    for url in REAL_URLS:
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(request, timeout=12) as response:
                content = response.read()
            if len(content) > 1000 and b"G3" in content[:500]:
                real_path.write_bytes(content)
                return real_path, True
        except Exception:
            pass
    print("NOTICE: Internet download unavailable; using bundled demo data.")
    print("For final submission, place the original UCI student-mat.csv in the data folder.")
    return demo_path, False

def main():
    path, is_real = obtain_data()
    df = pd.read_csv(path, sep=";")
    print("=" * 60)
    print("STUDENT PERFORMANCE DATA ANALYSIS")
    print("Dataset mode:", "Original UCI data" if is_real else "Bundled demo data")
    print("Rows, columns:", df.shape)
    print("\nFirst five rows:\n", df.head().to_string(index=False))
    print("\nData types:\n", df.dtypes.to_string())
    print("\nMissing values:\n", df.isna().sum().to_string())
    print("Duplicate rows:", int(df.duplicated().sum()))

    # Cleaning / preprocessing
    df = df.drop_duplicates().copy()
    for col in df.select_dtypes(include=np.number).columns:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())
    for col in df.select_dtypes(exclude=np.number).columns:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].mode().iloc[0])
    if "G3" not in df.columns:
        raise ValueError("Expected final-grade column G3 was not found in the dataset.")
    df.to_csv(OUT / "cleaned_student_data.csv", index=False)

    # Summary and EDA
    summary = df.describe(include="all").transpose()
    summary.to_csv(OUT / "descriptive_statistics.csv")
    avg_grade = float(df["G3"].mean())
    print(f"\nAverage final grade (G3): {avg_grade:.2f}/20")
    print("Students with final grade >= 10:", int((df["G3"] >= 10).sum()))
    print("Students with final grade < 10:", int((df["G3"] < 10).sum()))
    if "studytime" in df.columns:
        print("Study time vs final grade correlation:", round(float(df["studytime"].corr(df["G3"])), 3))
    if "absences" in df.columns:
        print("Absences vs final grade correlation:", round(float(df["absences"].corr(df["G3"])), 3))

    # Save a text report with reproducible statistics
    with open(OUT / "key_findings.txt", "w", encoding="utf-8") as f:
        f.write("STUDENT PERFORMANCE ANALYSIS - KEY FINDINGS\n")
        f.write(f"Dataset mode: {'Original UCI data' if is_real else 'Bundled demo data'}\n")
        f.write(f"Rows after duplicate removal: {len(df)}\n")
        f.write(f"Columns: {len(df.columns)}\n")
        f.write(f"Average final grade (G3): {avg_grade:.2f}/20\n")
        f.write(f"Students with G3 >= 10: {int((df['G3'] >= 10).sum())}\n")
        f.write(f"Students with G3 < 10: {int((df['G3'] < 10).sum())}\n")
        if "studytime" in df.columns:
            f.write(f"Correlation studytime-G3: {df['studytime'].corr(df['G3']):.3f}\n")
        if "absences" in df.columns:
            f.write(f"Correlation absences-G3: {df['absences'].corr(df['G3']):.3f}\n")

    # Visualizations
    plt.figure(figsize=(8,5))
    df["G3"].plot(kind="hist", bins=10, edgecolor="black")
    plt.title("Distribution of Final Grades (G3)")
    plt.xlabel("Final grade (0-20)"); plt.ylabel("Number of students")
    plt.tight_layout(); plt.savefig(OUT/"final_grade_distribution.png", dpi=150); plt.close()

    if "studytime" in df.columns:
        means = df.groupby("studytime")["G3"].mean()
        plt.figure(figsize=(8,5))
        means.plot(kind="bar", edgecolor="black")
        plt.title("Average Final Grade by Weekly Study Time")
        plt.xlabel("Study time category (1=lowest, 4=highest)"); plt.ylabel("Average G3")
        plt.tight_layout(); plt.savefig(OUT/"studytime_vs_grade.png", dpi=150); plt.close()

    if "absences" in df.columns:
        plt.figure(figsize=(8,5))
        plt.scatter(df["absences"], df["G3"], alpha=0.7)
        plt.title("Absences vs Final Grade")
        plt.xlabel("Number of absences"); plt.ylabel("Final grade (G3)")
        plt.tight_layout(); plt.savefig(OUT/"absences_vs_grade.png", dpi=150); plt.close()

    if {"G1","G2","G3"}.issubset(df.columns):
        corr = df[["G1","G2","G3"]].corr()
        plt.figure(figsize=(6,5))
        plt.imshow(corr, vmin=-1, vmax=1, aspect="auto")
        plt.xticks(range(len(corr.columns)), corr.columns)
        plt.yticks(range(len(corr.index)), corr.index)
        plt.colorbar(label="Correlation")
        plt.title("Correlation Between Period Grades")
        for i in range(len(corr.index)):
            for j in range(len(corr.columns)):
                plt.text(j, i, f"{corr.iloc[i,j]:.2f}", ha="center", va="center")
        plt.tight_layout(); plt.savefig(OUT/"grade_correlation.png", dpi=150); plt.close()

    print("\nAnalysis complete. Check the outputs folder for CSV summaries, findings, and charts.")
    print("Dataset source: https://archive.ics.uci.edu/dataset/320/student+performance")

if __name__ == "__main__":
    main()
