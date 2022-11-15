import pandas as pd
import boto3
import io
import dateparser

# setting access
client = boto3.client(
    's3',
    aws_access_key_id='AKIAQQ3QG6SJ6W7J4DZJ',
    aws_secret_access_key='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',
    region_name='eu-west-1'
)

def getting_all_files():

    # reading files
    files = client.list_objects(Bucket='titan-data-transfer')
    all_files = []
    for item in files['Contents']:
        if ".csv" in item['Key']:
            all_files.append(item['Key'])
        else:
            continue
    # print(all_files)
    return all_files

def getting_latest_file(list_of_files):
    max_date = ''
    latest_file = ''
    for file in list_of_files:
        d = file.split('''/''')[-1].split("_")[-2]
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

def get_latest_and_second_latest_files(all_files):
    latest_file = getting_latest_file(all_files)
    all_files.remove(latest_file)
    second_latest_file = getting_latest_file(all_files)
    return latest_file, second_latest_file

def read_files(path):
    #TODO: need to store mapping files in bucket to
    # Read Mapping Sheets
    newModel_df = pd.read_excel(
        'C:\\Users\\Lenovo\\Desktop\\Five_Proj\\PandasTask\\stellantis_prep-processing\\stellantis_mapping\\Stellantis_Germany_Daily_Data_Template_20221018_133109 - Process file for Portfolio and DF (1).xlsb',
        sheet_name='NewModel', engine='pyxlsb')
    newChannel_df = pd.read_excel(
        'C:\\Users\\Lenovo\Desktop\\Five_Proj\\PandasTask\\stellantis_prep-processing\\stellantis_mapping\\Stellantis_Germany_Daily_Data_Template_20221018_133109 - Process file for Portfolio and DF (1).xlsb',
        sheet_name='NewChannel', engine='pyxlsb')
    raw_file = client.get_object(Bucket='titan-data-transfer', Key=path)
    raw_df = pd.read_csv(io.BytesIO(raw_file['Body'].read()), sep=';')


    # Converting columns into strings (ensure uniform data type in column)
    raw_df['MIT Brand'] = raw_df['MIT Brand'].astype('str')
    raw_df['MIT Model Sub Category Consolidated'] = raw_df['MIT Model Sub Category Consolidated'].astype('str')
    raw_df['MIT Range Category Consolidated'] = raw_df['MIT Range Category Consolidated'].astype('str')

    newModel_df['MIT Brand'] = newModel_df['MIT Brand'].astype('str')
    newModel_df['MIT Model Sub Category Consolidated'] = newModel_df['MIT Model Sub Category Consolidated'].astype(
        'str')
    newModel_df['MIT Range Category Consolidated'] = newModel_df['MIT Range Category Consolidated'].astype('str')

    # Add new date column
    raw_df['Month-Year'] = pd.to_datetime(raw_df['Year/Month'], errors='coerce').dt.strftime('%b-%Y')

    return raw_df, newModel_df, newChannel_df

def joining_dfs(df_raw, df1, df2):
    
    # Joining Mapping Files
    pre_processed_df = df_raw.merge(df1, on=['MIT Brand','MIT Model Sub Category Consolidated', 'MIT Range Category Consolidated'], how='left') \
                            .merge(df2, on=['MIT Media', 'MIT Channel'], how='left')
    return pre_processed_df

def df_properties_check(df):
  # Checking df size and checking for any null values
    print(f'Size of file {df.shape}')
    print(f'Null values: \n{df.isnull().sum()}')
    

def daily_media_aggregations(df):
    #Media aggregations for QA check
    return df[['MIT Media','MIT Channel','MIT Net Net Media EUR BY DAY']].groupby(by=['MIT Media','MIT Channel']).sum().round(2)

def merging_total_spends(df):
    # Created dataframe for totals spends of channels and models
    df_total_channel = df[['NewChannel', 'MIT Final Cost to Client EUR BY DAY']].groupby(['NewChannel']).sum().round(3).reset_index()
    # Rename column
    df_total_channel.rename(columns={"MIT Final Cost to Client EUR BY DAY":"total_channel_spend"}, inplace = True)
    print(df_total_channel)

    # Repeat process of models
    df_total_model = df[['New_Model', 'MIT Final Cost to Client EUR BY DAY']].groupby(['New_Model']).sum().round(3).reset_index()
    df_total_model.rename(columns={"MIT Final Cost to Client EUR BY DAY":"total_model_spend"}, inplace = True)
    print(df_total_model)

    # merge channel and model total to processed dataframe
    df_model_channel_merged =  df.merge(df_total_channel, on=['NewChannel'], how='left')\
                                           .merge(df_total_model, on=['New_Model'],how='left')

    return df_model_channel_merged

def df_aggregated(file):
    df_raw,df1,df2 = read_files(file)

    # check properties of daily raw file
    df_properties_check(df_raw)
    df_merged = joining_dfs(df_raw, df1, df2)
    df_aggregated = merging_total_spends(df_merged)

    # check properties of aggregated file
    df_properties_check(df_aggregated)
    return df_aggregated

def comparison_df(df1, df2):
    df3 = pd.merge(df1,df2, on=['NewChannel','New_Model'])
    df3['TotalChannelSpendDifference'] = df3['total_channel_spend'] - df3['yesterday_total_channel_spend']
    df3['TotalModelSpendDifference'] = df3['total_model_spend'] - df3['yesterday_total_model_spend']
    return df3


##################################################################################################################
##################################################################################################################
if __name__ == "__main__":
    all_files = getting_all_files()
    today_file, yesterday_file = get_latest_and_second_latest_files(all_files)
    prev_week_file = 'titan-data-transfer/Stellantis_Germany_Daily_Data_Template_20221019_170010.csv'
    #display all the new models added when merge give NaNs
    print('============================')
    print('==========TODAY=============')
    print('============================')

    df_today = df_aggregated(today_file)
    df_today_unmapped = df_today[df_today.isnull().any(axis=1)].reset_index(drop=True)
    df_today_unmapped.to_csv("TodayFileMappingRequired.csv")
    df_today_mapped = df_today.dropna()
    df_properties_check(df_today_mapped)

    print('============================')
    print('==========YESTERDAY=============')
    df_yesterday = df_aggregated(yesterday_file)
    df_yesterday_unmapped = df_yesterday[df_yesterday.isnull().any(axis=1)].reset_index(drop=True)
    df_yesterday_unmapped.to_csv("YesterdayFileMappingRequired.csv")
    df_yesterday_mapped = df_yesterday.dropna()
    df_properties_check(df_yesterday_mapped)

    df_yesterday_truncated = df_yesterday_mapped[['NewChannel','New_Model','total_channel_spend','total_model_spend']].\
        rename(columns={"total_model_spend":"yesterday_total_model_spend", "total_channel_spend":"yesterday_total_channel_spend"})
    # print(df_today_mapped[['NewChannel','New_Model','total_channel_spend','total_model_spend']])
    # print(df_yesterday_truncated)
    final_df = comparison_df(df_today_mapped, df_yesterday_truncated)
    final_df.to_csv("Final_Merge.csv")