import glob
import pandas as pd
from tidy import load_cudo

#The universities on the site: CUDO name -> (display name, city, website)
SCHOOLS = {
    "McMaster University": ("McMaster University", "Hamilton", "https://www.mcmaster.ca"),
    "Western - Main Campus": ("Western University", "London", "https://www.uwo.ca"),
    "University of Toronto": ("University of Toronto", "Toronto", "https://www.utoronto.ca"),
    "Ontario Tech University": ("Ontario Tech University", "Oshawa", "https://ontariotechu.ca"),
    "University of Waterloo": ("University of Waterloo", "Waterloo", "https://uwaterloo.ca"),
    "York University": ("York University", "Toronto", "https://www.yorku.ca"),
}

MEASURES = {
    "Employment Rate (2 Yrs)": "emp_rate_2yr",
    "Employment Rate (6 Mths)": "emp_rate_6mo",
}

k2_files = glob.glob("data/raw/K2_*.csv")  #finds your K2 file automatically
k2 = load_cudo(k2_files[0])

#Keep only our universities, and drop the "Overall Average" summary row
k2 = k2[k2["university"].isin(SCHOOLS) & (k2["label"] != "Overall Average")].copy()
k2["measure"] = k2["group"].map(MEASURES)

#One row per university + program + graduating year, with both rates side by side
wide = k2.pivot_table(
    index=["university", "label", "year"], columns="measure", values="value"
).reset_index()
wide = wide.rename(columns={"label": "program", "year": "grad_year"})
wide["grad_year"] = wide["grad_year"].astype(int)

#Add display name, city and website
wide["city"] = wide["university"].map(lambda u: SCHOOLS[u][1])
wide["website"] = wide["university"].map(lambda u: SCHOOLS[u][2])
wide["university"] = wide["university"].map(lambda u: SCHOOLS[u][0])

#Tuition and co-op stay blank until we fill them from official sources
wide["tuition_domestic"] = ""
wide["coop"] = ""

columns = ["university", "city", "program", "grad_year", "emp_rate_2yr",
           "emp_rate_6mo", "tuition_domestic", "coop", "website"]
wide = wide[columns].sort_values(["program", "university", "grad_year"])
wide.to_csv("data/universities.csv", index=False)

print("Rows:", len(wide))
print("Programs:", wide["program"].nunique())
print(wide[wide["program"] == "Computer Science"].to_string(index=False))