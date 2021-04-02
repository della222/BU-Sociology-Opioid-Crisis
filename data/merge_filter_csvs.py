import os
import glob
import pandas as pd
import numpy as np
import sys

def merge_csvs(folder,new_file_name):
    '''
    folder: folder containing split up csvs with same columns titles
    new_file_name: name you want the merged file written to
    
    Function merges the csv files and saves to a new file
    '''

    # -Change into the directory with all of the unmerged csv files
    os.chdir('./'+folder)
    #print(os.getcwd()) 

    # -Use glob pattern matching to gather all files with extension .csv
    # -Save to list --> all_filenames
    file_extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(file_extension))]
    #print("{} these are all the filenames ending in .csv".format(all_filenames))

    # -Combine files in the list using pd.concat() and export to csv
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    combined_csv.to_csv(new_file_name,index=False)

    return

def filter_empty_rows(csv_file):
    '''
    csv_file: the old file that needs filtering
    
    Drops all rows from empty campaign by checking for blank cells under Title column, returns updated dataframe
    '''
    csv = pd.read_csv(csv_file)
    csv.drop(csv.index[(csv["Title"].isnull()==True)],axis=0,inplace=True)
    
    #check_for_nan = csv['Title'].isnull()
    #rows_to_remove = np.where(check_for_nan==True)[0]
    #update_df = csv.drop(rows_to_remove,axis=0,inplace=True)

    return csv

def filter_country(dataframe):
    '''
    dataframe: pandas dataframe that is the most updated based on previous filtering functions

    Filters out international campaign by checking for currency codes other than 'USD', returns updated dataframe
    '''
    #print(type(dataframe))
    #sys.exit()
    dataframe.drop(dataframe.index[(dataframe["Currency_Code"] != "USD")],axis=0,inplace=True)
    return dataframe


def main():

    folder = 'First_2000_urls' #move all individual unmerged files to a new folder in './data', place the name of that folder here
    new_file_name = 'campaign_bs4_data_2000_all.csv' #choose the title of the merged files
    merge_csvs(folder,new_file_name)

    #os.chdir('./'+folder)
    updated_csv = filter_empty_rows('campaign_bs4_data_0_2000.csv')
    updated_csv = filter_country(updated_csv)
    
    updated_csv.to_csv('updated_csv_countries.csv',index=False)
    

if __name__ == '__main__':
    main()

