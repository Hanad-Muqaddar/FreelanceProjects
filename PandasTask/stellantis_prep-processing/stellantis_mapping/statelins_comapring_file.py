from stellantis_pre_processing import read_files
from stellantis_pre_processing import  joining_dfs
import pandas as pd
import datetime
import dateparser
import glob
import os
pd.get_option("display.max_columns", 10)
pd.get_option("display.max_rows")


def getting_list_of_files():
    return glob.glob('C:\\Users\\Lenovo\\Desktop\\Five_Proj\\PandasTask\\stellantis_prep-processing\\stellantis-raw/*.csv')

def getting_latest_file(list_of_files):
    max_date = ''
    latest_file = ''
    for file in list_of_files:
        d = file.split('''\\''')[-1].split("_")[-2]
        n = 2
        dm = [d[i:i+n] for i in range(0, len(d), n)]
        date_structue = ','.join(dm[1:])
        final_date = dateparser.parse(date_structue, settings={'DATE_ORDER' :'YMD'})
        if max_date == "":
            max_date = final_date
        elif final_date > max_date:
            max_date = final_date
            latest_file = file
        else:
            continue
    return latest_file

def get_latest_and_second_latest_files():
    files = getting_list_of_files()
    latest_file = getting_latest_file(files)
    files.remove(latest_file)
    second_latest_file = getting_latest_file(files)
    return latest_file, second_latest_file

def get_rid_of_under_score(data):
    return data.replace("_", " ")


def summary_for_new_model(df3, df3_):
    
    df3_today_comparison = df3[['New_Model', 'MIT Final Cost to Client EUR BY DAY']].groupby(['New_Model']).sum().round(3)
    df3_yesterday_comparison = df3_[['New_Model', 'MIT Final Cost to Client EUR BY DAY']].groupby(['New_Model']).sum().round(3)

    # print(df3_today_comparison)
    # print(df3_yesterday_comparison)
    df3_today_comparison = df3_today_comparison.rename(columns={'MIT Final Cost to Client EUR BY DAY':'Total_spend_today'})
    df3_yesterday_comparison = df3_yesterday_comparison.rename(columns={'MIT Final Cost to Client EUR BY DAY':'Total_spend_Yesterday'})

    df3_today_comparison.reset_index()
    df3_yesterday_comparison.reset_index()

    final_comparison_df = pd.merge(df3_today_comparison, df3_yesterday_comparison, on='New_Model')

    # print(final_comparison_df)
    final_comparison_df['Diffrence'] = final_comparison_df['Total_spend_today'] - final_comparison_df['Total_spend_Yesterday']
    print(final_comparison_df)


def summary_of_New_channel(df3, df3_):
    df3_today_comparison = df3[['NewChannel', 'MIT Final Cost to Client EUR BY DAY']].groupby(['NewChannel']).sum().round(3)
    df3_yesterday_comparison = df3_[['NewChannel', 'MIT Final Cost to Client EUR BY DAY']].groupby(['NewChannel']).sum().round(3)

    # print(df3_today_comparison)
    # print(df3_yesterday_comparison)
    df3_today_comparison = df3_today_comparison.rename(columns={'MIT Final Cost to Client EUR BY DAY':'Total_spend_today'})
    df3_yesterday_comparison = df3_yesterday_comparison.rename(columns={'MIT Final Cost to Client EUR BY DAY':'Total_spend_Yesterday'})

    df3_today_comparison.reset_index()
    df3_yesterday_comparison.reset_index()

    final_comparison_df = pd.merge(df3_today_comparison, df3_yesterday_comparison, on='NewChannel')

    # print(final_comparison_df)
    final_comparison_df['Diffrence'] = final_comparison_df['Total_spend_today'] - final_comparison_df['Total_spend_Yesterday']
    print(final_comparison_df)



today_data, yesterday_data = get_latest_and_second_latest_files()

raw_df, newModel_df, newChannel_df = read_files(today_data)

pre_processed_df = joining_dfs(raw_df, newModel_df, newChannel_df)
# print(pre_processed_df)
# print(pre_processed_df.columns)

df1 = pre_processed_df[['MIT Brand','MIT COUNTRY CONSOLIDATED','MIT Model Sub Category Consolidated','New_Model','NewChannel','MIT Final Cost to Client EUR BY DAY']].groupby(['New_Model','NewChannel', 'MIT COUNTRY CONSOLIDATED', 'MIT Brand','MIT Model Sub Category Consolidated']).sum().round(3)
df2 = df1.reset_index()
# print(df2.columns)
df3 = df2[['MIT COUNTRY CONSOLIDATED','MIT Brand', 'MIT Model Sub Category Consolidated','New_Model','NewChannel','MIT Final Cost to Client EUR BY DAY']]
# new_df.to_csv("GroupBy_dataframe.csv")
# print(df3.head(25))
df3['NewChannel'] = df3['NewChannel'].map(get_rid_of_under_score)
df3['New_Model'] = df3['New_Model'].map(get_rid_of_under_score)
# print(df3.head(5).iloc[:, 2:])


##############################################################################

raw_df_1, newModel_df_1, newChannel_df_1 = read_files(yesterday_data)

pre_processed_df_1 = joining_dfs(raw_df_1, newModel_df_1, newChannel_df_1)
# print(pre_processed_df)
# print(pre_processed_df.columns)

df1_ = pre_processed_df_1[['MIT Brand','MIT COUNTRY CONSOLIDATED','MIT Model Sub Category Consolidated','New_Model','NewChannel','MIT Final Cost to Client EUR BY DAY']].groupby(['New_Model','NewChannel', 'MIT COUNTRY CONSOLIDATED', 'MIT Brand','MIT Model Sub Category Consolidated']).sum().round(3)
df2_ = df1_.reset_index()
# print(df2_.columns)
df3_ = df2_[['MIT COUNTRY CONSOLIDATED','MIT Brand', 'MIT Model Sub Category Consolidated','New_Model','NewChannel','MIT Final Cost to Client EUR BY DAY']]
# new_df.to_csv("GroupBy_dataframe.csv")
# print(df3.head(25))
df3_['NewChannel'] = df3_['NewChannel'].map(get_rid_of_under_score)
df3_['New_Model'] = df3_['New_Model'].map(get_rid_of_under_score)
# print(df3_.head(5).iloc[:, 2:])


# Till there you have two dataframes named as df3, and df3_. df3 is for today_csv, and df3_ is for yesterday csv.


# summary_of_New_channel(df3, df3_)
summary_for_new_model(df3, df3_)



