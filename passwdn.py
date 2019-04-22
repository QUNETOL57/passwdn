import sqlite3,os,time
import qcli
import settings
import gen_pass
import cript

def start(limit_start = 0,limit = 10):
	settings.clear()
	print("—"*settings.LINE_WIDTH)
	print("Service list: ")
	for row in cursor.execute("""SELECT * FROM data LIMIT {},{}""".format(limit_start,limit)):
		if row[0] < 10:
			print("",str(row[0])+"|", cript.encryptDecrypt('D',row[1],settings.KEY))
		else:
			print(str(row[0])+"|", cript.encryptDecrypt('D',row[1],settings.KEY))

def start_down():
    global st
    global limit
    cursor.execute("""SELECT * FROM data""")
    if st+limit < len(cursor.fetchall()):
        st+= limit

def start_up():
    global st
    global limit
    cursor.execute("""SELECT * FROM data""")
    if st-limit >= 0:
        st-=limit

def show(columns,show_num):
	settings.clear()
	print("—"*settings.LINE_WIDTH)
	lines = []
	for row in cursor.execute("""SELECT * FROM data WHERE service_num={}""".format(show_num)):
		for i in range(1,len(row)):
			lines.append(row[i])
	for key,value in columns.items():
		if len(value) != 18:
			value += " "* (18 - len(value))
		print(value + "|",cript.encryptDecrypt('D',lines[key],settings.KEY))

	print("—"*settings.LINE_WIDTH)
	print("edit [e] | delete [d] | back [b] |")
	print("—"*settings.LINE_WIDTH)
	inp = input()
	if inp == 'back' or inp == 'b' or inp == 'BACK' or inp == 'B':
		settings.clear()
	elif inp == 'edit' or inp == 'EDIT' or inp == 'ed' or inp == 'ED' or inp == 'e' or inp == 'E':
		edit(show_num)
	elif inp == 'delete' or inp == 'DELETE' or inp == 'del' or inp == 'DEL' or inp == 'd' or inp == 'D':
		delete(show_num)

def add():
	settings.clear()
	cursor.execute("""SELECT * FROM data""")
	num = len(cursor.fetchall()) + 1
	name = input("Service name      |")
	adress = input("Service adress    |")
	telnumber = input("Service telnumber |")
	nickname = input("Service nickname  |")
	email = input("Service email     |")
	password = input("Service password  |")
	addlist = [(
		num,
	    cript.encryptDecrypt('E',name,settings.KEY),
	    cript.encryptDecrypt('E',adress,settings.KEY),
	    cript.encryptDecrypt('E',telnumber,settings.KEY),
	    cript.encryptDecrypt('E',nickname,settings.KEY),
	    cript.encryptDecrypt('E',email,settings.KEY),
	    cript.encryptDecrypt('E',password,settings.KEY),)]
	cursor.executemany("""INSERT INTO data VALUES (?,?,?,?,?,?,?)""", addlist)
	conn.commit()

def edit(show_num):
	settings.clear()
	print("—"*settings.LINE_WIDTH)
	lines = []
	columns = {1:'service_name',2:'service_adress',3:'service_telnumber',4:'service_nickname',5:'service_email',6:'service_password'}
	for row in cursor.execute("""SELECT * FROM data WHERE service_num={}""".format(show_num)):
		for i in range(1,len(row)):
			lines.append(row[i])
	print("Parameters to change:")
	for key,value in columns.items():
		if len(value) != 18:
			value += " "* (18 - len(value))
		print(str(key)+"|",value + "|",cript.encryptDecrypt('D',lines[key-1],settings.KEY))
	print("—"*settings.LINE_WIDTH)
	inp = int(input())
	inp2 = input()
	inp2 = cript.encryptDecrypt('E',inp2,settings.KEY)
	cursor.execute("""UPDATE data SET {0} = '{2}' WHERE {0} = '{1}' AND service_num == {3} """.format(columns[inp],lines[inp-1],inp2,show_num))
	conn.commit()

def delete(show_num):
	settings.clear()
	print("—"*settings.LINE_WIDTH)
	for row in cursor.execute("""SELECT * FROM data WHERE service_num={}""".format(show_num)):
		for i in row:
			print(i)
	print("—"*settings.LINE_WIDTH)
	print("[!] DELETE THIS? |",end=" ")
	inp = input()
	if inp == 'yes' or inp == 'y' or inp == 'YES' or inp == 'Y':
		cursor.execute("""DELETE FROM data WHERE service_num = {}""".format(show_num))
		conn.commit()

def gen():
    gen_pass.gen_pass()

def main_page(columns,actions):
    global st,limit
    while True:
        try:
            start(st,limit)
            print("—"*settings.LINE_WIDTH)
            print(" up [u] | down [d] | select | add [a] | help [h] | exit [e]")
            print("—"*settings.LINE_WIDTH)
            inp = input()
            if inp in actions:
                if actions[inp] == exit:
                    settings.clear()
                    break
                else:
                    actions[inp]()
            else:
                show(columns1,inp)
        except:
            continue
        conn.commit()

conn = sqlite3.connect(settings.NAME + ".db")
cursor = conn.cursor()
user_log = []
sms= ''
st = 0
limit = 10
columns = {0:'Service number',1:'Service name',2:'Service adress',3:'Service telnumber',4:'Service nickname',5:'Service email',6:'Service password'}
columns1 = {0:'Service name',1:'Service adress',2:'Service telnumber',3:'Service nickname',4:'Service email',5:'Service password'}
actions = {
    'q' : exit,'Q' : exit,'e' : exit,'E' : exit,
    'a' : add,'add' : add,'ad' : add,'A' : add,
    'd': start_down,'D': start_down,'down': start_down,'DOWN' : start_down,
    'u' : start_up,'U' : start_up,'up' : start_up,'UP' : start_up,
    'g' : gen,'gen' : gen,'G' : gen,'GEN' : gen
}

if __name__ == '__main__':
    # qcli.User_QCLI(settings.NAME)
    main_page(columns,actions)
