# Student Performance Analysis

This is a small Flask project for exploring student exam performance data.
It reads a CSV file of student records, calculates a few summary metrics, and
shows the results in a simple web dashboard.

The dashboard includes:

- average math, reading, and writing scores
- pass and fail percentages
- a gender filter
- four charts for quick visual analysis

The project is intentionally lightweight. It uses server-rendered HTML
templates and generates charts on the backend with Matplotlib.

## Project Structure

`app.py`
Main Flask application.

`templates/`
HTML templates for the home page and dashboard.

`static/`
Shared stylesheet for the frontend.

`data/StudentsPerformance.csv`
Dataset used by the app.

`test_app.py`
Basic regression tests for the main routes and filter behavior.

## Requirements

- Python 3.10 or newer is recommended
- pip

## Installation

1. Clone the repository:

```bash
git clone https://github.com/saqib-7/student-performance-analysis.git
cd student-performance-analysis
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Command Prompt:

```bat
.\.venv\Scripts\activate.bat
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Project

Start the Flask application with:

```bash
python app.py
```

Then open this address in your browser:

`http://127.0.0.1:5000/`

## Running Tests

To run the included tests:

```bash
python -m unittest test_app.py
```

## Notes

- The app expects the dataset file to be present at `data/StudentsPerformance.csv`.
- Charts are generated on the server and embedded directly into the page.
- The current app uses Flask's built-in development server, which is fine for local use and demos.
