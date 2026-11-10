# Expense Tracker with Visuals

A simple web app to track personal expenses, see where the money goes, and download an Excel report. Built with Python and Streamlit as part of an internship project.

## Features

- Add expenses through a form (date, category, description, amount)
- Upload many expenses at once using a CSV file
- Automatic data cleaning (wrong dates and amounts, duplicates, category names)
- Filter by date range and category
- Summary: total spent, average expense, number of entries
- Pie chart of spending by category
- Bar chart of monthly spending
- Budget alert: green (safe), yellow (above 80%), red (budget crossed)
- Export a styled Excel report with 3 sheets: Expenses, By Category, By Month

## Tools Used

- Python 3
- Streamlit
- pandas
- matplotlib
- openpyxl

## How to Run

1. Install the libraries:

   ```
   pip install -r requirements.txt
   ```

2. Start the app:

   ```
   python -m streamlit run app.py
   ```

3. Open `http://localhost:8501` in your browser.

4. In the sidebar, upload `test_expenses.csv` and click **Load CSV**.

## CSV Format

The file should have these columns:

```
date,category,description,amount
2026-10-01,Food,Breakfast,60
2026-10-02,Travel,Bus fare,40
```

`test_expenses.csv` has 120 sample expenses (August to November 2026) that you can use for testing.

## Screenshots



![Charts](screenshots/charts.png)





![Budget alert](screenshots/budget_alert.png)





![Excel report](screenshots/excel_report.png)



## Project Files

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit app |
| `test_expenses.csv` | Sample data (120 expenses) |
| `requirements.txt` | Python libraries needed |
| `Expense_Tracker_Report.pdf` | Project report |

## Future Improvements

- Save data in a database so it is not lost on refresh
- User login
- Separate budget for each category
- Email reminders when the budget is close to the limit
