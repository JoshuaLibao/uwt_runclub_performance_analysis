# UWT Run Club Analytics Report

Dashboard of analytics providing insights on how UW Tacoma Run Club is performing

## Business Questions
Dashboard 1: Club Overview
- How many people attended each run?
- Is attendance increasing, decreasing, or staying consistent over time?
- Which runs have the highest and lowest attendance?
- How many first-time attendees are coming to each run?

Dashboard 2: Recruitment and retention
- How many attendees are first-time participants versus only once or twice?
- Are people who attend for the first time coming back to future runs?
- What proportion of eligible first-time attendees return within 30 days?
- Are we attracting new people but struggling to get them to return?
  
Dashboard 3:
- How frequently do individual runners attend?
- How many runners attend regularly versus only once or twice?
- Which runners have not attended recently?
- What does repeat participation look like across the club?

## Dataset
- Data source: UWT Run Club data stored on excel
- Key tables: runners, attendance and runs

## Tools & Technologies
- Python
- Pandas
- SQL
- Power BI
- Excel

## Data Pipeline
1. Data collection
2. Data cleaning / transformation
3. SQL analysis
4. Visualization in Power BI

## Key Metrics
| Metric | Definition |
|---|---|
| Total Attendance | The total amount of people who attended overall |
| Unique Runners | The number of unique runners |
| First-Time Runners | It is a person's first time running with the run club |
| Returning Runners | The runners who came back after at least one run |
| 30-Day Return Rate | The runners who came back after at least one run within the last 30 days |
| Runners Attending 4+ Times | The runners who attended 4 or more run clubs |

## Dashboard

![Dashboard Screenshots] 
https://cdn.corenexis.com/f/OdT7xvvFzMl.png
https://cdn.corenexis.com/f/xwvOCL5eAte.png
https://cdn.corenexis.com/f/dvSbQzUHm8K.png

## How to Run
1. Clone this repository.
2. Set up the required environment.
3. Load the dataset.
4. Run the SQL scripts.
5. Open the Power BI report.

## Repository Structure
uwt_runclub_performance_analysis/
├── data/
    ├── processed/
    ├── raw/
├── sql/
├── dashboard/
├── images/
├── src/
└── README.md
