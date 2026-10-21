import pandas as pd 
import sqlite3

excel_path = r'C:\Users\12063\Downloads\sqlite\uwt_runclub_performance_analysis\data\raw\run_club_data.xlsx'
db_path = r'C:\Users\12063\Downloads\sqlite\uwt_runclub_performance_analysis\data\processed\processed_data.db'
df = pd.read_excel(excel_path)
conn = sqlite3.connect(db_path)

runs_df = pd.read_excel(excel_path, sheet_name="runs")
runners_df = pd.read_excel(excel_path, sheet_name="runners")
attendance_df = pd.read_excel(excel_path, sheet_name="attendance")

# data cleaning/validation:
# runner_id = int
# run_id = int 
# route = str
# run_date = datetime64[us]
# first_time = int
# runner_name = str
runs_df['run_date'] = pd.to_datetime(
    runs_df['run_date'],
    errors="coerce"
)

missing_counts = {
"runners_runner_id":runners_df['runner_id'].isna().sum(),
"runners_runner_name":runners_df['runner_name'].isna().sum(),
"attendance_run_id":attendance_df['run_id'].isna().sum(),
"attendance_runner_id":attendance_df['runner_id'].isna().sum(),
"attendance_first_time":attendance_df['first_time'].isna().sum(),
"runs_run_id":runs_df['run_id'].isna().sum(),
"runs_route":runs_df['route'].isna().sum(),
"runs_run_date":runs_df['run_date'].isna().sum(),
"runs_distance_miles":runs_df['distance_miles'].isna().sum()
}

for column, count in missing_counts.items():
    if count > 0:
        print(
            f"{column} failed validation! "
            f"{count} missing values detected."
        )
    else:
        print(f"{column} success")

runs_df = runs_df.astype({'run_id':int, 'route':str, 'distance_miles':float})
attendance_df = attendance_df.astype({'run_id':int, 'runner_id':int, "first_time":int})
runners_df = runners_df.astype({'runner_id':int, 'runner_name':str})

runs_df = runs_df[
    (runs_df['distance_miles'] > 0)
]
attendance_df = attendance_df[
    ((attendance_df['first_time'] == 0) |
    (attendance_df['first_time'] == 1)) 
]

runs_df.to_sql("runs", conn, if_exists="replace", index=False)
runners_df.to_sql("runners", conn, if_exists="replace", index=False)
attendance_df.to_sql("attendance", conn, if_exists="replace", index=False)

# combine runs and attendance tables: date, route, attendance count, returning attendees(0/1)
# attendance_count -> engineers attendance_count column
# most_recent_run -> engineers last_run_date column
# returning_raw -> engineers first_run_date column and returning cutoff column
# # final table puts everything together

run_attendance_summary = pd.read_sql("""
    WITH
    attendance_count_setup AS (
        SELECT
            run_id,
            SUM(run_id) AS attendance_count,
            SUM(first_time) AS first_time_attendees
        FROM attendance
    ),
    first_run_date_setup AS (
        SELECT 
            attendance.runner_id,
            attendance.run_id,
            MIN(runs.run_date) AS first_run_date
        FROM attendance
        JOIN runs 
            ON runs.run_id = attendance.run_id
        GROUP BY attendance.runner_id
    ),
    first_run_date_final AS (
        SELECT 
            first_run_date_setup.run_id,
            first_run_date_setup.runner_id,
            first_run_date_setup.first_run_date
        FROM first_run_date_setup
        JOIN runners
            ON first_run_date_setup.runner_id = runners.runner_id
    ),
    returning_cutoff_setup AS (
        SELECT 
            first_run_date_setup.run_id,
            date(first_run_date_setup.first_run_date, '+30 days') AS returning_cutoff
        FROM first_run_date_setup
        JOIN runners
            ON first_run_date_setup.runner_id = runners.runner_id
    ),
    last_run_date_setup AS (
        SELECT 
            attendance.runner_id AS runner_id,
            MAX(runs.run_date) AS last_run_date
        FROM runs
        JOIN attendance 
            ON runs.run_id = attendance.run_id
        GROUP BY attendance.runner_id
    ),
    last_run_date_final AS (
        SELECT
            last_run_date_setup.runner_id AS runner_id,
            last_run_date_setup.last_run_date AS last_run_date,
            attendance.run_id AS run_id
        FROM last_run_date_setup
        JOIN attendance 
            ON attendance.runner_id = last_run_date_setup.runner_id
    ),
    returning_setup AS (
        SELECT 
            returning_cutoff_setup.run_id AS run_id,
            CASE WHEN last_run_date_final.last_run_date < returning_cutoff_setup.returning_cutoff THEN 1 else 0 END AS is_returning
        from last_run_date_final
        JOIN returning_cutoff_setup 
            ON last_run_date_final.run_id = returning_cutoff_setup.run_id
    ),
    returning_final AS (
        SELECT 
            run_id,
            COUNT(is_returning) AS returning_attendees
        FROM returning_setup
    )
    SELECT 
        attendance_count_setup.attendance_count,
        attendance_count_setup.first_time_attendees,
        returning_final.returning_attendees
    FROM attendance_count_setup
    CROSS JOIN returning_final
""", conn)

print(run_attendance_summary)
run_attendance_summary.to_sql("run_attendance_summary", conn, if_exists='replace',index=False)

conn.commit()
conn.close()