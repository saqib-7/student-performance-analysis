from flask import Flask, render_template, request
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # Must be before pyplot import (no GUI backend needed)
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)


# Helper: load data
def load_data():
    path = os.path.join("data", "StudentsPerformance.csv")
    df = pd.read_csv(path)
    # Rename columns for easier use
    df.columns = [
        "gender",
        "race",
        "parent_edu",
        "lunch",
        "test_prep",
        "math",
        "reading",
        "writing",
    ]
    df["average"] = (df["math"] + df["reading"] + df["writing"]) / 3
    df["pass"] = df["average"].apply(lambda x: "Pass" if x >= 40 else "Fail")
    return df


#  Helper: convert plot to base64 image
def plot_to_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=100)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return img_base64


# Route: Home page
@app.route("/")
def index():
    return render_template("index.html")


#  Route: Dashboard
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    df = load_data()

    # Filter by gender if user selects one
    gender_filter = request.form.get("gender", "All")
    if gender_filter != "All":
        df = df[df["gender"] == gender_filter]

    # Analysis Stats
    stats = {
        "total_students": len(df),
        "avg_math": round(df["math"].mean(), 2),
        "avg_reading": round(df["reading"].mean(), 2),
        "avg_writing": round(df["writing"].mean(), 2),
        "pass_pct": round((df["pass"] == "Pass").mean() * 100, 2),
        "fail_pct": round((df["pass"] == "Fail").mean() * 100, 2),
    }

    #  Chart 1: Average score by gender (Bar chart)
    gender_avg = df.groupby("gender")[["math", "reading", "writing"]].mean()
    fig, ax = plt.subplots(figsize=(6, 4))
    gender_avg.plot(kind="bar", ax=ax, color=["#4e79a7", "#f28e2b", "#e15759"])
    ax.set_title("Average Scores by Gender")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Score")
    ax.legend(["Math", "Reading", "Writing"])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    chart1 = plot_to_base64()

    #  Chart 2: Math score distribution (Histogram)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df["math"], bins=20, color="#4e79a7", edgecolor="white")
    ax.set_title("Math Score Distribution")
    ax.set_xlabel("Score")
    ax.set_ylabel("Number of Students")
    chart2 = plot_to_base64()

    #  Chart 3: Reading vs Writing (Scatter plot)
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = {"Pass": "#59a14f", "Fail": "#e15759"}
    for label, group in df.groupby("pass"):
        ax.scatter(
            group["reading"],
            group["writing"],
            label=label,
            alpha=0.6,
            color=colors[label],
            s=20,
        )
    ax.set_title("Reading vs Writing Score")
    ax.set_xlabel("Reading Score")
    ax.set_ylabel("Writing Score")
    ax.legend()
    chart3 = plot_to_base64()

    #  Chart 4: Pass/Fail pie chart
    fig, ax = plt.subplots(figsize=(4, 4))
    counts = df["pass"].value_counts()
    ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=["#59a14f", "#e15759"],
        startangle=90,
    )
    ax.set_title("Pass / Fail Split")
    chart4 = plot_to_base64()

    return render_template(
        "dashboard.html",
        stats=stats,
        chart1=chart1,
        chart2=chart2,
        chart3=chart3,
        chart4=chart4,
        gender_filter=gender_filter,
    )


if __name__ == "__main__":
    app.run(debug=True)
