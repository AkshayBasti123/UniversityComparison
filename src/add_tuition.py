import pandas as pd

#Load the employment dataset and the hand-checked tuition table
universities = pd.read_csv("data/universities.csv")
tuition = pd.read_csv("data/tuition.csv")

#Remove any old tuition columns so this script is safe to run more than once
old_cols = ["tuition_domestic", "tuition_note", "tuition_year", "source_url"]
universities = universities.drop(columns=[c for c in old_cols if c in universities.columns])

#Attach tuition to every matching university + program (both graduating years)
merged = universities.merge(tuition, on=["university", "program"], how="left")

merged.to_csv("data/universities.csv", index=False)

has_tuition = merged.drop_duplicates(["university", "program"])["tuition_domestic"].notna().sum()
total = len(merged.drop_duplicates(["university", "program"]))
print(f"Tuition filled for {has_tuition} of {total} university + program combinations")
print(merged[(merged["program"] == "Computer Science") & (merged["grad_year"] == 2022)]
      [["university", "emp_rate_2yr", "tuition_domestic"]].to_string(index=False))