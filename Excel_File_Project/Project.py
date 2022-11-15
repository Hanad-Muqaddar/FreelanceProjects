import pandas as pd
import numpy as np

def reading_dataframe():
    return pd.read_excel("Sample.xlsx")

def writing_data(text):
    f = open("Insights.txt", "a")
    f.writelines(text)
    f.close()

def present_week_preprocessing(df, this_week):
    columns_list = list(df.columns[1:13])
    choose_dataframe = df.iloc[:,0:19]
    this_week_dataframe = choose_dataframe.loc[choose_dataframe['Week'] == this_week]
    writing_data("For This week get total\n\n")
    columns_list.remove("Dozen Eggs")
    columns_list.remove("Flat Eggs")
    for column_name in columns_list:
        cleanedList = [x for x in this_week_dataframe[column_name].to_list() if str(x) != 'nan']
        sum_of_list = sum(cleanedList)        
        if sum_of_list == 0:
            continue
        writing_data(str(sum_of_list) + " : " + column_name + "\n")
    dozen = sum(12 * np.array([x for x in this_week_dataframe["Dozen Eggs"].to_list() if str(x) != 'nan']))
    flat_eggs = sum(30 * np.array([x for x in this_week_dataframe["Flat Eggs"].to_list() if str(x) != 'nan']))
    total_eggs = (dozen + flat_eggs) / 12
    writing_data(str(total_eggs) + " : " + "dozen eggs" + "\n")


def next_week_preprocessing(df, next_week):
    columns_list = list(df.columns[1:13])
    choose_dataframe = df.iloc[:,0:19]
    this_week_dataframe = choose_dataframe.loc[choose_dataframe['Week'] == next_week]
    writing_data("\nFor next week order\n\n")
    columns_list.remove("Dozen Eggs")
    columns_list.remove("Flat Eggs")
    for column_name in columns_list:
        cleanedList = [x for x in this_week_dataframe[column_name].to_list() if str(x) != 'nan']
        sum_of_list = sum(cleanedList)        
        if sum_of_list == 0:
            continue
        writing_data(str(sum_of_list) + " : " + column_name + "\n")
    dozen = sum(12 * np.array([x for x in this_week_dataframe["Dozen Eggs"].to_list() if str(x) != 'nan']))
    flat_eggs = sum(30 * np.array([x for x in this_week_dataframe["Flat Eggs"].to_list() if str(x) != 'nan']))
    total_eggs = (dozen + flat_eggs) / 12
    writing_data(str(total_eggs) + " : " + "dozen eggs" + "\n")
    writing_data("\n\n")

def getting_prices(df):
    item_list = [x for x in df['My_Item'].to_list() if str(x) != 'nan']
    price_list = [x for x in df['My_Price'].to_list() if str(x) != 'nan']
    return(dict(zip(item_list, price_list)))

def write_customer_data(cust_list, price_list):
    for i in cust_list:
        try:
            name = i['Customers']
            i.pop("Customers")
        except:
            pass
        try:
            address = i['Address']
            i.pop("Address")
        except:
            pass
        try:
            phone = i['Phone']
            i.pop("Phone")
        except:
            pass
        if i == {}:
            continue
        writing_data(name + " , " + address + " , " + phone + "\n")
        total_prices = []
        for index, row in i.items():
            writing_data("\t- " + str(row) + " : " +  index + "\n")
            for key , value in price_list.items():
                if key.lower() == index.lower():
                    total_prices.append(int(value) * int(row))
        writing_data("\t- Total Price : $" + str(sum(total_prices)))
        writing_data("\n")

def get_customers_data(df, this_week):
    choose_dataframe = df.iloc[:,0:19]
    this_week_dataframe = choose_dataframe.loc[choose_dataframe['Week'] == this_week]
    columns_list = list(df.columns[:13])
    columns_list.append("Address")
    columns_list.append("Phone")
    customers_list = []
    for index, row in this_week_dataframe.iterrows():
        item = {}
        for i in columns_list:
            if str(row[i]) != "nan":
                item[i] = str(row[i])
        customers_list.append(item)
    return customers_list
    

if __name__ == '__main__':
    # this_week = WEDNESDAY October 19th
    # next_week = WEDNEASDAY October 26th
    this_week = input("Enter this Week : ")
    next_week = input("Enter Next week : ")
    df = reading_dataframe()
    price_dict = getting_prices(df)
    present_week_preprocessing(df, this_week)
    next_week_preprocessing(df, next_week)
    cust_list = get_customers_data(df, this_week)
    write_customer_data(cust_list, price_dict)