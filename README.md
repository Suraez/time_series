# time_series

### scripts/merge.py explanation

You have 3 folders:
    1. requests_minute
    2. cpu_usage_minute
    3. memory_usage_minute
   

The script will ask you first number of days you want to merge, then the column number from each day-001.csv from each of the above folder to extract values

`For e.g. Enter how many days of data you want to merge (max 235): 6`

```
Specify the column index (>=2) to extract from each file (just one per file).
CPU column index: 6
Memory column index: 6
Request column index: 6
```

Then the script will go through day_00[1-6].csv file in each of the above folders and extract the **(6-2) = 4th columns** value from each csv file




