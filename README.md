# Ontario University Finder

**Live site: https://universitycomparison.onrender.com**

> The site runs on a free host that sleeps when nobody is using it. If it hasn't been visited in a while, the first load can take about a minute.

Pick what you want to study and see how six Ontario universities compare on **graduate employment** and **first-year tuition**, side by side. Every tuition figure says what it includes and links to where it came from.

![Home page](screenshots/home.png)
![Results for Computer Science](screenshots/results.png)

## The question

When you're choosing a university, the same program can lead to very different outcomes depending on where you study it. This project asks: **for the program you want, how do Ontario universities compare on jobs after graduation and on cost?**

## What you can do

- Choose a program area (25 are available, such as Computer Science, Engineering, Nursing, Business & Commerce, Mathematics).
- See universities ranked by the share of graduates employed 2 years after graduating, with the 6-month rate alongside.
- See first-year tuition for Ontario residents where it's available, with a note and a source link on each figure.

Universities covered: McMaster, Ontario Tech, Toronto, Waterloo, Western, and York.

## What the data shows

These are descriptive findings for the six universities in this project, using the graduating classes of 2021 and 2022. They are not claims about cause.

- **Computer Science, 2 years after graduating (class of 2022):** employment ranges from about 95% at Waterloo (94.95%) to about 81% at Ontario Tech (80.77%), a gap of roughly 14 points.
- **Computer Science employment fell from the class of 2021 to 2022 at five of six universities.** York was the exception (+3.6 points). The largest drops were at McMaster (100% to 87.5%) and Ontario Tech (91.78% to 80.77%). Single-year changes in smaller programs can be noisy, so I'd treat this as a signal to watch, not a conclusion.
- **Across all programs,** the 2-year employment rate dropped between the two classes in 58 of 98 matched university-and-program pairs, rose in 25, and stayed the same in 15. The median change was -0.9 points.
- **Six months vs. two years:** in Computer Science, the 6-month rate was below the 2-year rate at five of six universities. The biggest gap was at Ontario Tech (58% vs. 80.77%). Across all programs in the class of 2022, the 2-year rate was higher than the 6-month rate in 63 of 99 cases, with an average gap of 3.3 points.
- **Computer Science tuition** (tuition-only figures): about $8,077 at Western (draft schedule), about $8,800 at York, and about $9,290 at McMaster (calculated). Waterloo's $16,000 is an estimate that includes incidental fees, so it can't be compared directly with the others.

## How it works

1. **Source data.** Employment rates come from the Council of Ontario Universities' Common University Data Ontario (CUDO) reports (report K2, employment rate of graduates in undergraduate programs), exported from the COU's customized reports. Tuition comes from each university's 2026-27 fee information.
2. **Cleaning the exports.** The COU files are wide spreadsheets with a three-row header (measure, university, year), where university names appear once per block and blank cells follow. `src/tidy.py` reshapes them into a tidy table with one row per university, program, year and measure. It forward-fills the headers, converts suppressed values (`*`) to missing values, and fixes a character-encoding glitch in a university name.
3. **Checking my work.** I compared the parsed output against numbers I had collected separately from the University of Windsor's own CUDO page. The 2021 Computer Science rates matched exactly (92.42% and 82.54%), which also confirmed what the year labels mean (graduating class).
4. **Building the dataset.** `src/build_dataset.py` filters to the six universities, drops the "Overall Average" summary row, and pivots the 2-year and 6-month rates into side-by-side columns.
5. **Adding tuition.** `data/tuition.csv` is a hand-checked table. Each row records the amount, what it includes, the year, and the source URL. `src/add_tuition.py` merges it into the dataset.
6. **The site.** A small Flask app (`app.py`) reads the dataset with pandas and renders it with a Jinja template, HTML and CSS. It's deployed on Render using Gunicorn.

## Tech stack

Python, pandas, Flask, Jinja, HTML, CSS, Gunicorn, Git/GitHub, Render.

## Project structure

```
UniversityComparison/
├── app.py                  Flask app
├── requirements.txt
├── data/
│   ├── raw/                Original COU exports
│   ├── tuition.csv         Hand-checked tuition, with sources
│   └── universities.csv    Final dataset used by the site
├── src/
│   ├── tidy.py             Reshapes the COU exports
│   ├── build_dataset.py    Builds the employment dataset
│   └── add_tuition.py      Merges in tuition
├── templates/index.html
├── static/style.css
└── screenshots/
```

## Run it locally

```bash
git clone https://github.com/AkshayBasti123/UniversityComparison.git
cd UniversityComparison
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5001.

To rebuild the dataset from the raw export:

```bash
python src/build_dataset.py
python src/add_tuition.py
```

## Limitations

I'd rather be upfront about these than have them found later.

- **Six universities only.** Other Ontario universities aren't included yet.
- **Program areas, not individual programs.** The employment data groups students into broad areas such as "Engineering" or "Social Science".
- **Tuition is incomplete.** Tuition is missing for the University of Toronto, and for Ontario Tech in Computer Science, Engineering, Business and Nursing. Out of 101 university-and-program combinations, 27 have tuition.
- **Tuition figures aren't all the same kind.** Western's schedule is marked as a draft. McMaster charges per unit, so its figures are calculated at a 30-unit year, and engineering loads may be higher. Waterloo's are rounded estimates that include incidental fees. York's are approximate. Each card says which applies.
- **Employment data is one graduating class.** The site shows the class of 2022. Small programs can change a lot from year to year.
- **No causal claims.** The site compares outcomes. It doesn't say why one university's graduates are employed at a higher rate than another's.
- **I excluded the retention data.** The retention report (K3) had values that looked like entry errors (for example, 0.9 where a percentage near 90 would be expected), so I left it out rather than guess.

## What I'd add next

- More universities, starting with the rest of Ontario's public universities.
- Co-op availability for each program.
- A comparison of the class of 2021 and 2022 on the same card.
- Filling in the missing tuition figures from official fee schedules.

## About

Built by Akshay Bastiampillai, a data science student at Ontario Tech University.
[LinkedIn](https://www.linkedin.com/in/akshay-bastiampillai-974571356/)
