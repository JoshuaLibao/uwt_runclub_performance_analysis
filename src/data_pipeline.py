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

run_attendance_summary = pd.read_sql("""
    WITH
    attendance_count_setup AS (
        SELECT
            run_id,
            COUNT(*) AS attendance_count,
            SUM(first_time) AS first_time_attendees
        FROM attendance
        GROUP BY run_id
    ),

    first_run_date_final AS (
        SELECT
            attendance.runner_id AS runner_id,
            MIN(runs.run_date) AS first_run_date
        FROM attendance
        JOIN runs
            ON runs.run_id = attendance.run_id
        GROUP BY attendance.runner_id
    ),

    runs_v2 AS (
        SELECT
            runs.run_id AS run_id,
            runs.run_date AS run_date,
            attendance.runner_id AS runner_id,
            attendance.first_time AS first_time
        FROM runs
        JOIN attendance
            ON runs.run_id = attendance.run_id
    ),

    returning_setup AS (
        SELECT
            runs_v2.run_id AS run_id,
            runs_v2.runner_id AS runner_id,
            CASE
                WHEN first_run_date_final.first_run_date < runs_v2.run_date
                THEN 1
                ELSE 0
            END AS is_returning
        FROM runs_v2
        JOIN first_run_date_final
            ON runs_v2.runner_id = first_run_date_final.runner_id
    ),

    returning_final AS (
        SELECT
            run_id,
            SUM(is_returning) AS returning_attendees
        FROM returning_setup
        GROUP BY run_id
    )

    SELECT
        runs.run_id AS run_id,
        runs.run_date AS run_date,
        COALESCE(attendance_count_setup.attendance_count, 0) AS attendance_count,
        COALESCE(attendance_count_setup.first_time_attendees, 0) AS first_time_attendees,
        COALESCE(returning_final.returning_attendees, 0) AS returning_attendees
    FROM runs
    LEFT JOIN attendance_count_setup
        ON runs.run_id = attendance_count_setup.run_id
    LEFT JOIN returning_final
        ON runs.run_id = returning_final.run_id
""", conn)

run_attendance_summary.to_sql("run_attendance_summary", conn, if_exists='replace',index=False)

weekly_club_metrics = pd.read_sql("""
    SELECT 
        strftime('%Y-%W', run_date) AS week,
        SUM(attendance_count) AS total_attendance,
        SUM(first_time_attendees) AS total_first_time_attendees,
        SUM(returning_attendees) AS total_returning_attendees
    FROM run_attendance_summary
    GROUP BY strftime('%Y-%W', run_date)
""", conn)

weekly_club_metrics.to_sql("weekly_club_metrics", conn, if_exists='replace',index=False)

conn.commit()
conn.close()