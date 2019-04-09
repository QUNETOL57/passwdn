import sqlite3,os,time
# import getpass


def start(limit_start = 0,limit = 10):
	os.system('clear')
	print("—"*50)
	print("Service list: ")
	for row in cursor.execute("""SELECT * FROM data LIMIT {},{}""".format(limit_start,limit)):
		if row[0] < 10:
			print("",str(row[0])+"|", row[1])
		else:
			print(str(row[0])+"|", row[1])

def start_down(limit):
	global st
	cursor.execute("""SELECT * FROM data""")
	if st+limit < len(cursor.fetchall()):
		st+= limit

def start_up(limit):
	global st
	cursor.execute("""SELECT * FROM data""")
	if st-limit >= 0:
		st-=limit

def show(columns,show_num):
	os.system('clear')
	print("—"*50)
	lines = []
	for row in cursor.execute("""SELECT * FROM data WHERE service_num={}""".format(show_num)):
		for i in range(1,len(row)):
			lines.append(row[i])
	for key,value in columns.items():
		if len(value) != 18:
			value += " "* (18 - len(value))
		print(value + "|",lines[key])

	print("—"*50)
	print("edit [e] | delete [d] | back [b] |")
	print("—"*50)
	inp = input()
	if inp == 'back' or inp == 'b' or inp == 'BACK' or inp == 'B':
		os.system('clear')
	elif inp == 'edit' or inp == 'EDIT' or inp == 'ed' or inp == 'ED' or inp == 'e' or inp == 'E':
		edit(show_num)
	elif inp == 'delete' or inp == 'DELETE' or inp == 'del' or inp == 'DEL' or inp == 'd' or inp == 'D':
		delete(show_num)

def add():
	os.system('clear')
	cursor.execute("""SELECT * FROM data""")
	num = len(cursor.fetchall()) + 1
	name = input("Service name      |")
	adress = input("Service adress    |")
	telnumber = input("Service telnumber |")
	nickname = input("Service nickname  |")
	email = input("Service email     |")
	password = input("Service password  |")
	addlist = [(num,name,adress,telnumber,nickname,email,password)]
	cursor.executemany("""INSERT INTO data VALUES (?,?,?,?,?,?,?)""", addlist)
	conn.commit()

def edit(show_num):
	os.system('clear')
	print("—"*50)
	lines = []
	columns = {1:'service_name',2:'service_adress',3:'service_telnumber',4:'service_nickname',5:'service_email',6:'service_password'}
	for row in cursor.execute("""SELECT * FROM data WHERE service_num={}""".format(show_num)):
		for i in range(1,len(row)):
			lines.append(row[i])
	print("Parameters to change:")
	for key,value in columns.items():
		if len(value) != 18:
			value += " "* (18 - len(value))
		print(str(key)+"|",value + "|",lines[key-1])
	print("—"*50)
	inp = int(input())
	inp2 = input()
	cursor.execute("""UPDATE data SET {0} = '{2}' WHERE {0} = '{1}' AND service_num == {3} """.format(columns[inp],lines[inp-1],inp2,show_num))
	conn.commit()

def delete(show_num):
	os.system('clear')
	print("—"*50)
	for row in cursor.execute("""SELECT * FROM data WHERE service_num={}""".format(show_num)):
		for i in row:
			print(i)
	print("—"*50)
	print("[!] DELETE THIS? |",end=" ")
	inp = input()
	if inp == 'yes' or inp == 'y' or inp == 'YES' or inp == 'Y':
		cursor.execute("""DELETE FROM data WHERE service_num = {}""".format(show_num))
		conn.commit()

def logo():
	print("—"*50)
	print("______                         _ _   _ ".center(60))
	print("| ___ \\                       | | \\ | |".center(60))
	print("| |_/ /_ _ ___ _____      ____| |  \\| |".center(60))
	print("|  __/ _` / __/ __\\ \\ /\\ / / _` | . ` |".center(60))
	print("| | | (_| \\__ \\__ \\\\ V  V / (_| | |\\  |".center(60))
	print("\\_|  \\__,_|___/___/ \\_/\\_/ \\__,_\\_| \\_/".center(60))
	print("—"*50)

def en(s):
	sig  = sha224(s.encode()).hexdigest()
	return sig

def user(s):
	for row in cursor.execute("""SELECT * FROM user"""):
		for i in range(0,len(row)):
			s.append(row[i])

# def login_in(sms,s):
# 	user(s)
# 	while True:
# 		os.system('clear')
# 		logo()
# 		print("[!] Enter 'e' or 'exit' for exit.")
# 		print(sms)
# 		login = input("Login: ")
# 		if login == 'e' or login == 'exit':
# 			os.system('clear')
# 			quit()
# 		elif en(login) != s[0]:
# 			sms = "[X] Incorrect Login."
# 			continue
# 		password = getpass.getpass('Password:')
# 		if password == 'e' or password == 'exit':
# 			os.system('clear')
# 			quit()
# 		elif en(password) != s[1]:
# 			sms = "[X] Incorrect Password."
# 			continue
# 		print("—"*50)
# 		print("Welcome".center(60))
# 		print("—"*50)
# 		time.sleep(1)
# 		os.system('clear')
# 		break


def main_page(columns):
	global st,limit
	while True:
		try:
			start(st,limit)
			print("—"*50)
			print(" up [u] | down [d] | select | add [a] | help [h] | exit [e]")
			print("—"*50)
			inp = input()
			if inp == 'exit' or inp == 'e' or inp == 'EXIT' or inp == 'quit' or inp == 'q' or inp == 'Q' or inp == 'E':
				os.system('clear')
				break
			elif inp == 'add' or inp == 'ADD' or inp == 'a' or inp == 'ad' or inp == 'A':
				add()
			elif inp == 'd' or inp == 'D' or inp == 'down' or inp == 'DOWN':
				start_down(limit)
			elif inp == 'u' or inp == 'up'or inp == 'UP' or inp == 'U':
				start_up(limit)
			else:

				show(columns1,inp)
		except:
			continue
		conn.commit()


conn = sqlite3.connect("pswd.db")
cursor = conn.cursor()
user_log = []
sms= ''
st = 0
limit = 10
columns = {0:'Service number',1:'Service name',2:'Service adress',3:'Service telnumber',4:'Service nickname',5:'Service email',6:'Service password'}
columns1 = {0:'Service name',1:'Service adress',2:'Service telnumber',3:'Service nickname',4:'Service email',5:'Service password'}

if __name__ == '__main__':
	#login_in(sms,user_log)
	main_page(columns)
