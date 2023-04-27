import pandas as pd
df_api_daily = pd.read_excel("API Data daily.xlsx")
df_api_monthly = pd.read_excel("API Data monthly.xlsx")

# df read_excel convert date to datetime64
df_api_daily["Date"] = pd.to_datetime(df_api_daily["Date"], utc=False)
df_api_monthly["Date"] = pd.to_datetime(df_api_monthly["Date"], utc=False)
# datetime64 of first day one month ago
from datetime import datetime, timedelta
last_day_last_month = datetime.today().replace(day=1, hour=23, minute=59, second=59) - timedelta(days=1)
first_day_last_month = last_day_last_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

#filter dataframe between first_day_last_month and last_day_last_month
df_lastmonth_api_daily = df_api_daily[(df_api_daily["Date"] >= first_day_last_month) & (df_api_daily["Date"] <= last_day_last_month)]
df_lastmonth_api_monthly = df_api_monthly[df_api_monthly["Date"] == first_day_last_month]

# groupby aggregate quantile 95
df_lastmonth_api_daily.groupby("Service").agg({"Date": "min", "Count": "sum", "Max Response Time": "max", "P95 Response Time": lambda x: x.quantile(0.95), "% Errors": "mean"})

# compare the two dataframes column count based on service
merged_api_daily_monthly = df_lastmonth_api_daily.groupby("Service").agg({"Count": "sum"}).reset_index().merge(df_lastmonth_api_monthly, on="Service", how="left")
