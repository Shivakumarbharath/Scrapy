import pandas as pd
from sqlalchemy import create_engine

db_connect = create_engine('sqlite:///Bank.db')
df = pd.read_sql('BankDetails', con=db_connect, index_col='Bank_Name')

df['Market_cap'] = pd.to_numeric(df['Market_cap'])
df['CASA'] = pd.to_numeric(df['CASA'])
df['PB_RATIO'] = pd.to_numeric(df['PB_RATIO'])
df['Book_Value'] = pd.to_numeric(df['Book_Value'])
df['Net_Intrest_Income'] = pd.to_numeric(df['Net_Intrest_Income'])
df['EPS'] = pd.to_numeric(df['EPS'])
df['ROE'] = pd.to_numeric(df['ROE'])
df['Advances_growth'] = pd.to_numeric(df['Advances_growth'])
df['Cost_of_Liabalities'] = pd.to_numeric(df['Cost_of_Liabalities'])

df.rename(columns={'Market_cap': 'Market Cap in ₹Cr.', 'CASA': 'CASA %', 'PB_RATIO': 'P/B',
                   'Net_Intrest_Income': 'Net Intrest Income ₹Cr.',
                   'EPS': 'EPS (TTM)', 'CAR': 'CAR %', 'ROE': 'ROE % for 3 years', 'ROA': 'ROA % for 5 years',
                   'NPA': 'Net NPA% for 5 years',
                   'Advances_growth': 'Advances Growth %', 'Cost_of_Liabalities': 'Cost of Liabalities %',
                   'Book_Value': 'BOOK VALUE (TTM) ₹',

                   }, inplace=True)
df['NIM'] = df['NIM'].str.replace('%', '')
df['CAR %'] = df['CAR %'].str.replace('%', '')
df['Net NPA% for 5 years'] = df['Net NPA% for 5 years'].str.replace('%', '')
df['ROA % for 5 years'] = df['ROA % for 5 years'].str.replace('%', '')

df['NIM'] = pd.to_numeric(df['NIM'])
df['CAR %'] = pd.to_numeric(df['CAR %'])
df['Net NPA% for 5 years'] = pd.to_numeric(df['Net NPA% for 5 years'])
df['ROA % for 5 years'] = pd.to_numeric(df['ROA % for 5 years'])

##print(df)

df.to_excel('Bank.xlsx', sheet_name='Bank')
