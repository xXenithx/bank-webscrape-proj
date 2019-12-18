import numpy as np
import pandas as pd
import csv

lines = list()
with open('Export.csv', 'rb') as readFile:
    data = list(csv.reader(readFile))

with open('Bank_statement_cleaned.csv', 'wb') as writeFile:
    writer = csv.writer(writeFile)
    for row in data:
        if not data.index(row) < 3:
            writer.writerow(row)



df = pd.read_csv('Bank_statement_cleaned.csv', delimiter = ',')
df.dropna(axis=1, how='any', thresh=1, subset=None, inplace=True)

print(df)

amt_debit_total = df['Amount Debit'].sum()
amt_credit_total = df['Amount Credit'].sum()

print('Amount Credit Total: %f\nAmount Debit Total: %f\nNet Profit: %f' % (amt_debit_total,amt_credit_total,(amt_debit_total+amt_credit_total)))