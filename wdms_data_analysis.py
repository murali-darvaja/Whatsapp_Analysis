import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

SQL_ADDRESS = "localhost"
SQL_PORT = "3306"
SQL_USER = "root"
SQL_PASSWORD = ""
SQL_DBNAME = "wdms"
connection_str = "mysql://{username}:{password}@{ip_address}:{port}/{dbname}".format(username=SQL_USER,
                                                                                     password=SQL_PASSWORD,
                                                                                     ip_address=SQL_ADDRESS,
                                                                                     port=SQL_PORT, dbname=SQL_DBNAME)
cnx = create_engine(connection_str)

query_to_fetch_all_data = """SELECT
    ud.pincode, iv.id, iv.date_ts, ivi.Quantity, bd.Price, 
    bd.Bottle_Category, bd.litre, bd.Available_Quantity
FROM
    userdetails ud
INNER JOIN invoice iv ON
    ud.user_id = iv.user_id
INNER JOIN invoice_items ivi ON
    iv.id = ivi.invoice_id
INNER JOIN bottles_details bd ON
    ivi.bid = bd.bid
"""
df = pd.read_sql_query(query_to_fetch_all_data, con=cnx, parse_dates=['date_ts'])
df.columns = [column.lower() for column in df.columns]

df['pincode'] = df['pincode'].astype('category')
df['date_ts'] = df['date_ts'].dt.date
df['bottle_category'] = df['bottle_category'].astype('category')
df['quantity'] = df['quantity'].astype('int')
df['price'] = df['price'].astype('float')
# print(df['date_ts'])

# Num of orders on each day from latest date
df.groupby('date_ts')['id'].count()[::-1].plot(kind='bar', x='date_ts', y='id', title='No Of Orders Each Day', rot=1)
plt.xlabel("Date")
plt.ylabel("No.Of Orders")
plt.show()

# Num of orders from each pincode
df.groupby('pincode')['id'].count().plot(kind='bar', x='pincode', y='id', title="No of Orders from each area", rot=1)
plt.xlabel("Pincode")
plt.ylabel("No.Of Orders")
plt.show()

# Total Sales amount for each day from latest date
df['total_sales'] = df['quantity'] * df['price']
df.groupby('date_ts')['total_sales'].sum()[::-1].plot(kind='pie', x='date_ts', y='order_total',
                                                      title="Total Sales Amount(Rs) each  day", rot=1)
plt.legend()
plt.show()

# Total Sales for each pincode
df.groupby('pincode')['total_sales'].sum().plot(kind='pie', x='pincode', y='order_total',
                                                title="Total Sales Amount(Rs) each area", rot=1)
plt.legend()
plt.show()

df['total_water_avail'] = (df['litre'] * df['available_quantity'])

# Total water available capacity of each brand
df.groupby('bottle_category')['total_water_avail'].sum().plot(kind='pie', x='bottle_category', y='total_water_avail',
                                                              title='Total Water Available of each Brand')
plt.ylabel('Total Available Water(Ltrs)')
plt.legend()
plt.show()

df['total_order_quantity'] = (df['litre'] * df['quantity'])
df.groupby('bottle_category')['total_order_quantity'].sum().plot(kind='pie', x='bottle_category',
                                                                 y='total_order_quantity',
                                                                 title='Total Water Ordered of each Brand')
plt.ylabel('Total Ordered Water(Ltrs)')
plt.legend()
plt.show()
