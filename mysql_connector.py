import mysql.connector



db=mysql.connector.connect(user="root",passwd="admin",host="localhost",database='datascience')

my_cursor=db.cursor()



# adding a common query to insert all the students
query = "INSERT INTO tbl_master_extract(from_email,to_email,subject,body,receive_date) VALUES(%s,%s,%s,%s,%s)" # adding a common query to insert all the v
#list containing the information about the students in tuple form

from datetime import datetime
now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
stds = [("shedron3@gmail.com","shedron3@gmail.com","Test Subject",'Body',formatted_date)] 
 
my_cursor.executemany(query,stds)
db.commit()
print(my_cursor.rowcount, "records are inserted.")
