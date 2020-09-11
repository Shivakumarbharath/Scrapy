# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# To save in the database
import sqlite3
# To process and clean the data
import pandas as pd
# To read from the database as a dataframe
from sqlalchemy import create_engine
# To remove the unwanted databse file
import os


class TickerPipeline(object):

    # When the spider is opened following operations are performed
    def open_spider(self, spider):
        # Create a database and the table
        self.db = sqlite3.connect('Bank.db')
        self.c = self.db.cursor()
        self.c.execute('''

        CREATE TABLE BankDetails(
        Bank_Name TEXT,
        Market_cap TEXT,
        CASA TEXT,
        PB_RATIO TEXT,
        Book_Value TEXT,
        Net_Intrest_Income TEXT,
        EPS TEXT,
        CAR TEXT,
        ROE TEXT,
        ROA TEXT,
        NPA TEXT,
        NIM TEXT,
        Advances_growth TEXT,
        Cost_of_Liabalities TEXT
        )

        ''')
        # Commit the Created table
        self.db.commit()

    def close_spider(self, spider):
        # Close the database file
        self.db.close()

        # Read the database file as a dataframe
        db_connect = create_engine('sqlite:///Bank.db')
        df = pd.read_sql('BankDetails', con=db_connect, index_col='Bank_Name')

        # Convert the columns into numeric values
        df['Market_cap'] = pd.to_numeric(df['Market_cap'])
        df['CASA'] = pd.to_numeric(df['CASA'])
        df['PB_RATIO'] = pd.to_numeric(df['PB_RATIO'])
        df['Book_Value'] = pd.to_numeric(df['Book_Value'])
        df['Net_Intrest_Income'] = pd.to_numeric(df['Net_Intrest_Income'])
        df['EPS'] = pd.to_numeric(df['EPS'])
        df['ROE'] = pd.to_numeric(df['ROE'])
        df['Advances_growth'] = pd.to_numeric(df['Advances_growth'])
        df['Cost_of_Liabalities'] = pd.to_numeric(df['Cost_of_Liabalities'])

        # Change the column names
        df.rename(columns={'Market_cap': 'Market Cap in ₹Cr.', 'CASA': 'CASA %', 'PB_RATIO': 'P/B',
                           'Net_Intrest_Income': 'Net Intrest Income ₹Cr.',
                           'EPS': 'EPS (TTM)', 'CAR': 'CAR %', 'ROE': 'ROE % for 3 years', 'ROA': 'ROA % for 5 years',
                           'NPA': 'Net NPA% for 5 years',
                           'Advances_growth': 'Advances Growth %', 'Cost_of_Liabalities': 'Cost of Liabalities %',
                           'Book_Value': 'BOOK VALUE (TTM) ₹',

                           }, inplace=True)

        # Few columns have % in thier value So remove the char else cannot be changed to numeric values
        df['NIM'] = df['NIM'].str.replace('%', '')
        df['CAR %'] = df['CAR %'].str.replace('%', '')
        df['Net NPA% for 5 years'] = df['Net NPA% for 5 years'].str.replace('%', '')
        df['ROA % for 5 years'] = df['ROA % for 5 years'].str.replace('%', '')

        # Convert the cleaned columns into numeric
        df['NIM'] = pd.to_numeric(df['NIM'])
        df['CAR %'] = pd.to_numeric(df['CAR %'])
        df['Net NPA% for 5 years'] = pd.to_numeric(df['Net NPA% for 5 years'])
        df['ROA % for 5 years'] = pd.to_numeric(df['ROA % for 5 years'])

        # As all the values are numeric
        # Replace the Nan values with 0 For Better Interface
        df.fillna(0, inplace=True)

        ##print(df)
        # Save the dataframe into excel sheet
        df.to_excel('Bank.xlsx', sheet_name='Bank')
        os.remove('Bank.db')

    def process_item(self, item, spider):
        self.c.execute('''
        INSERT INTO BankDetails(
        Bank_Name,
        Market_cap,
        CASA,
        PB_RATIO,
        Book_Value,
        Net_Intrest_Income,
        EPS,
        CAR,
        ROE,
        ROA,
        NPA,
        NIM,
        Advances_growth,
        Cost_of_Liabalities
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        
        ''', (item['Bank Name'], item['Market Cap'], item['CASA %'], item['P/B'], item['Book Value'],
              item['Net Intrest Income'], item['EPS'], item['CAR %'], item['ROE %'], item['ROA For 5 years'],
              item['NPA For 5 years'], item['NIM For 5 years'], item['Advances Growth'], item['COST OF LIABALITIES']
              ))
        self.db.commit()
        return item
