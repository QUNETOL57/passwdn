import random
en_low=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
en_high=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
numb=[str(x) for x in range(10)]
onetwothree=[x for x in range(1,4)]
onetwo=onetwothree[:-1]

print('Enter size'.center(11),end="| ")
size = 10#int(input())
print('Caps ON?'.center(11),end="| ")
caps = 0#int(input())
print('-'*20)
while True:
    passwd = ""
    random.shuffle(en_low)
    random.shuffle(en_high)
    random.shuffle(numb)
    if caps == 1:
        for i in range(size):
            random.shuffle(onetwothree)
            if onetwothree[0] == 1:
                passwd+=random.choice(en_low)
            elif onetwothree[0] ==2:
                passwd+=random.choice(en_high)
            elif onetwothree[0] ==3:
                passwd+=random.choice(numb)
    elif caps== 0:
        for i in range(size):
            random.shuffle(onetwo)
            if onetwo[0] == 1:
                passwd+=random.choice(en_low)
            elif onetwo[0] ==2:
                passwd+=random.choice(numb)
    print('Password'.center(11),end="| ")
    print(passwd)
    print('-'*20)
    print('Again?|'.center(11),end="| ")
    n = int(input())
    if n == 0:
    	print('-'*20)
    	break
    print('-'*20)
