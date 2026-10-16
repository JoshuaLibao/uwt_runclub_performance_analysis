import pandas as pd 
import sqlite3

path = r'C:\Users\12063\Downloads\sqlite\uwt_run_club_performance_analysis\data\raw\run_club_data.xlsx'
df = pd.read_excel(path)

runs_df = pd.read_excel(path, sheet_name="runs")
runners_df = pd.read_excel(path, sheet_name="runners")
attendance_df = pd.read_excel(path, sheet_name="attendance")

# database schema:
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

def empty_column_check():

    f"{table}[{column_name}].isna().sum()"
missing_counts = {
empty_runner_id_1 = runners_df['runner_id'].isna().sum()
empty_runner_name = runners_df['runner_name'].isna().sum()
empty_run_id_1 = attendance_df['run_id'].isna().sum()
empty_runner_id_2 = attendance_df['runner_id'].isna().sum()
empty_first_time = attendance_df['first_time'].isna().sum()
empty_run_id_2 = runs_df['run_id'].isna().sum()
empty_route = runs_df['route'].isna().sum()
empty_run_date = runs_df['run_date'].isna().sum()
empty_distance_miles = runs_df['distance_miles'].isna().sum()

if empty_run_id_1 > 0:
    print(f"runner_id from the runners table failed! {empty_run_id_1} missing values detected")
if empty_runner_name > 0:
    print(f"runner_name from the runners table failed! {empty_runner_name} missing values detected")
if empty_run_id_1 > 0:
    print(f"empty_run_id from the attendance table failed! {empty_run_id_1} missing valued detected")
if empty_runner_id_2 > 0:
    print(f"runner_id from the attendance table failed! {empty_runner_id_2} missing values detected")
else:
    print("runner_id passed!")

# runs_df = runs_df[
#     (runs_df['run_id'].dtypes == int) and
#     (runs_df['route'].dtypes == str) and
#     (runs_df['distance_miles'].dtypes == float)
# ]

# attendance_df = attendance_df[
#     (attendance_df['run_df'].dtypes == int) and
#     (attendance_df['runner_id'].dtypes == int) and
#     (attendance_df['first_time'].dtypes == int)
# ]

# runners_df = runners_df[
#     (runners_df['runner_id'].dtypes == int) and
#     (runners_df['runner_name'].dtypes == str)
# ]

# data cleaning/validation:
# distance_miles data entry is > 0 
# first_time data entry is, >= 0 but <= 1
# runs_df = runs_df[
#     (runs_df['distance_miles'] > 0) and
#     ((runs_df['first_time'] == 0) or
#     (runs_df['first_time'] == 1)) 
#     ]

# print(runs_df)
# print(runners_df)
# print(attendance_df)

# print(runs_df.dtypes)
# print(runners_df.dtypes)
# print(attendance_df.dtypes)