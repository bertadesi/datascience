import smtplib
import time
import imaplib
import email
import traceback
import re
import mysql.connector

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
ORG_EMAIL = "@gmail.com" 
FROM_EMAIL = "shedron3" + ORG_EMAIL 
FROM_PWD = "qmwoeineescuotoi" 
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993


db=mysql.connector.connect(user="root",passwd="admin",host="localhost",database='datascience')

my_cursor=db.cursor()






def getEmail(srcEmail):
    reg=re.findall(r"[A-Za-z0-9_%+-.]+"r"@[A-Za-z0-9.-]+"r"\.[A-Za-z]{2,5}",srcEmail)
    return reg

def formatdate(email_receivedate):
    from email_receivedate import datetime
    formatted_date = email_receivedate.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date
    
def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        body=""

        for i in range(latest_email_id,first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    email_to= msg['to']
                    email_receivedate = msg['date']

##                    msgbody =email.message_from_bytes(arr[1])
##                    if msg.is_multipart():
##                        for part in msg.walk():
##                            content_type = part.get_content_type()
##                            content_disposition =str(part.get("Content-Disposition"))
##                            try:
##                                body = part.get_payload(decode=True).decode()
##                            except:
##                                pass
##                            if content_type =="text/plain" and "attachment" not in content_disposition:
##                                print(body)
##                            elif "attachment" in content_disposition:
##                                print("do nothing first")
##                    else:
##
##                        content_type =msg.get_content_type()
##                        body = msg.get_payload(decode=True).decode()
##                        if content_type=="text/plain":
##                            print(body)
##                            
##                        if content_type =="text/html":
##                            print ("skip html")
                            
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')
                    print(email_to)
                    print(email_receivedate)
                    # adding a common query to insert 
                    query = "INSERT INTO tbl_master_extract(from_email,to_email,subject,body,receive_date) VALUES(%s,%s,%s,%s,%s)" # adding a common query to insert all the v

                    stds = [(email_from,email_to,email_subject,'',email_receivedate)] 
 
                    my_cursor.executemany(query,stds)
                    db.commit()
                    print(my_cursor.rowcount, "records are inserted.")

    except Exception as e:
        traceback.print_exc() 
        print(str(e))

read_email_from_gmail()
