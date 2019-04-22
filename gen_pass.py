import random
import settings

en_low=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
en_high=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
numb=[str(x) for x in range(10)]
onetwothree=[x for x in range(1,4)]
onetwo=onetwothree[:-1]

def gen_pass():
    settings.clear()
    print("—"*settings.LINE_WIDTH)
    size = int(input("Enter size        | "))
    caps = input("Caps ON?          | ")
    settings.clear()
    while True:
        print("—"*settings.LINE_WIDTH)
        print('Size              |',size)
        passwd = ""
        random.shuffle(en_low)
        random.shuffle(en_high)
        random.shuffle(numb)
        if caps == 'on' or caps == 'y' or caps == '1':
            print('Caps              | ON')
            for i in range(size):
                random.shuffle(onetwothree)
                if onetwothree[0] == 1:
                    passwd+=random.choice(en_low)
                elif onetwothree[0] ==2:
                    passwd+=random.choice(en_high)
                elif onetwothree[0] ==3:
                    passwd+=random.choice(numb)
        else:
            for i in range(size):
                print('Caps              | OFF')
                random.shuffle(onetwo)
                if onetwo[0] == 1:
                    passwd+=random.choice(en_low)
                elif onetwo[0] ==2:
                    passwd+=random.choice(numb)
        print("Password          |", passwd)
        print("—"*settings.LINE_WIDTH)
        print("again [a] | back [b] |")
        print("—"*settings.LINE_WIDTH)
        again = input()
        settings.clear()
        if again == 'b':
        	break
