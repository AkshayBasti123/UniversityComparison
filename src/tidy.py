import csv
import pandas as pd


def load_cudo(path):
    #Turn a wide COU export (3 header rows) into a tidy table.
    with open(path, encoding="latin-1", newline="") as f:
        rows = list(csv.reader(f))

    width = max(len(r) for r in rows[1:4])

    def fill_right(row):
        row = row + [""] * (width - len(row))
        return pd.Series(row).replace(r"^\s*$", pd.NA, regex=True).ffill()

    group = fill_right(rows[1])
    university = fill_right(rows[2])
    year = pd.Series(rows[3] + [""] * (width - len(rows[3]))).str.strip()

    records = []
    for row in rows[4:]:
        if not any(cell.strip() for cell in row):
            continue
        row = row + [""] * (width - len(row))
        label = row[0].strip()
        for j in range(1, width):
            if pd.isna(university[j]):
                continue
            value = row[j].strip().replace(",", "")
            records.append((label, str(group[j]).strip(),
                            str(university[j]).strip(), year[j], value))

    df = pd.DataFrame(records, columns=["label", "group", "university", "year", "value"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    df["university"] = df["university"].str.replace("Universit?", "Université", regex=False)
    return df