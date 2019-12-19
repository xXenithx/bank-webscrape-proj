import numpy as np
import pandas as pd
import sqlite3 as lite
import uuid
import os
import sys
import csv


def add_vendors_to_database(vendors):

    if not os.path.isfile('vendors.db'):
        print('\nError, no file vendors.db found. Creating one instead')
        connection = lite.connect('vendors.db')
    
        with connection:
            cur = connection.cursor()
            cur.execute("CREATE TABLE Vendors(Guid TEXT, Vendor TEXT)")
            add_vendors_to_database(vendors)

    else:
        connection = lite.connect('vendors.db')
        cur = connection.cursor()

        with connection:
            for vend in vendors:
                data = (str(uuid.uuid4()), vend)
            
                print('\nInserting Vendor %s with uuid of %s\n' % (data[1],data[0]))

                cur.execute("INSERT INTO Vendors VALUES(?,?)", (data))
                connection.commit()
    
    connection.close()
        
        

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

# print(df)

# amt_debit_total = df['Amount Debit'].sum()
# amt_credit_total = df['Amount Credit'].sum()

# print('Amount Credit Total: %f\nAmount Debit Total: %f\nNet Profit: %f' % (amt_debit_total,amt_credit_total,(amt_debit_total+amt_credit_total)))
# largest = df.loc[df['Amount Debit'].idxmin()]
# print('\nLargest Transaction:\n')
# print(largest)

list_vendors = []

for index in range(df.shape[0]):
    if df.isnull().ix[index, 3]:
        vendor = df.ix[index, 2]
    else:
        vendor = df.ix[index, 3]

    vnd_str = vendor.split()
    vn1 = vnd_str[0]
    vn2 = vnd_str[1]

    list_vendors.append(vn1 + ' ' + vn2)

print(list_vendors)
print('\nRemoving Duplicates.\n')
list_vendors = list(set(list_vendors))
print(list_vendors)
add_vendors_to_database(list_vendors)