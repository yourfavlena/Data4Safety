Data4Safety

What the code does:
- This project is a small Streamlit app called Data4Safety.
- It reads a CSV file with temporary protection decisions (by country/citizenship, time, sex).
- The app shows data cleaning steps and basic statistics.
- It creates a dashboard with time series charts, a geographic map, and bar charts to explore the data.

How to run:
1. Open a terminal and move to the project folder (where `app.py` is).
2. Run this command in the terminal:

   streamlit run app.py

That's all. The app will open in your browser (usually at http://localhost:85XX).

Notes:
- Make sure the dataset `estat_migr_asytpfm_en.csv/estat_migr_asytpfm_en.csv` is in the project folder, or update the path in `app.py`.
- If Streamlit is not installed, install it with `pip install streamlit` before running.
 
Data source:
The data used by this app is taken from the European data portal: https://data.europa.eu/data/datasets/uwyrsvz2fpqtles5ntwdoa?locale=en
