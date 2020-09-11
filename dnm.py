import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'banka'
)

mycursor = mydb.cursor()

pno = ''
cash = 1000
mycursor.execute("UPDATE bot_sql Set Balance = Balance + {0} WHERE Phone_no ={1} ".format(cash, pno))
mycursor.fetchone()

mydb.commit()

mycursor.execute("SELECT * FROM bot_sql WHERE Phone_no = ''")
myresult = mycursor.fetchone()

for i in myresult:
    print(i)
#Testing for mysql database connection