from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("data/universities.csv")
df = df[df["grad_year"] == 2022]


@app.route("/")
def home():
    programs = sorted(df["program"].unique())
    selected = request.args.get("program", "")
    results = []

    if selected:
        matches = df[df["program"] == selected]
        matches = matches.sort_values("emp_rate_2yr", ascending=False)
        #turn blanks (NaN) into None so the HTML can check for them
        matches = matches.astype(object).where(matches.notna(), None)
        results = matches.to_dict("records")

    return render_template(
        "index.html", programs=programs, selected=selected, results=results
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)