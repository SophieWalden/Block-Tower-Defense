import monsters, random
def genEnemies(wave, Images, mapName):
    """Outputs a list of all enemies based on a certain wave"""
    Monsters = []
    if wave == 1:
        for i in range(20):
            Monsters.append([monsters.Monster(1, wave, False, Images, mapName),30*i])
    elif wave == 2:
        for i in range(35):
            Monsters.append([monsters.Monster(1, wave, False, Images, mapName),15*i])
    elif wave == 3:
        for i in range(5):
            Monsters.append([monsters.Monster(2, wave, False, Images, mapName),60*i])
        for i in range(20):
            Monsters.append([monsters.Monster(1, wave, False, Images, mapName),30*(i+21)])
    elif wave == 4:
        for j in range(5):
            for i in range(2):
                Monsters.append([monsters.Monster(2, wave, False, Images, mapName),45*(i+j*10)])
            for i in range(8):
                Monsters.append([monsters.Monster(1, wave, False, Images, mapName),30*(i+j*10+2)])
    elif wave == 5:
        for j in range(3):
            Monsters.append([monsters.Monster(1, wave, False, Images, mapName),30*(1+j*10)])
            for i in range(9):
                Monsters.append([monsters.Monster(2, wave, False, Images, mapName),30*(i+1+j*10)])
    elif wave == 6:
        for j in range(3):
            for i in range(5):
                Monsters.append([monsters.Monster(1, wave, False, Images, mapName),30*(i*2+j*11)])
                Monsters.append([monsters.Monster(2, wave, False, Images, mapName),30*(i*2+1+j*11)])
            Monsters.append([monsters.Monster(3, wave, False, Images, mapName),30*(10+j*11)])
        Monsters.append([monsters.Monster(3, wave, False, Images, mapName),60*(18)])
    elif wave == 7:
        for j in range(5):
            for i in range(4):
                Monsters.append([monsters.Monster(1, wave, False, Images, mapName),30*(i*2+j*9)])
                Monsters.append([monsters.Monster(2, wave, False, Images, mapName),30*(i*2+1+j*9)])
            Monsters.append([monsters.Monster(3, wave, False, Images, mapName),30*(8+j*9)])
    elif wave == 8:
        for i in range(10):
            Monsters.append([monsters.Monster(1, wave, False, Images, mapName),30*i])
        for i in range(20):
            Monsters.append([monsters.Monster(2, wave, False, Images, mapName),30*(i+10)])
        for i in range(14):
            Monsters.append([monsters.Monster(3, wave, False, Images, mapName),30*(i+30)])
    elif wave == 9:
        for i in range(30):
            Monsters.append([monsters.Monster(3, wave, False, Images, mapName),45*i])
    elif wave == 10:
        for i in range(102):
            Monsters.append([monsters.Monster(2, wave, False, Images, mapName),20*i])
    elif wave == 11:
        for j in range(3):
            for i in range(2):
                Monsters.append([monsters.Monster(1, wave, False, Images, mapName),30*(i+j*11)])
            for i in range(4):
                Monsters.append([monsters.Monster(2, wave, False, Images, mapName),30*(i*2+j*11)])
                Monsters.append([monsters.Monster(3, wave, False, Images, mapName),30*(i*2+1+j*11)])
            Monsters.append([monsters.Monster(4, wave, False, Images, mapName),30*(10+j*11)])
    elif wave == 12:
        for j in range(5):
            for i in range(3):
                Monsters.append([monsters.Monster(2, wave, False, Images, mapName),30*(i+j*7)])
            for i in range(2):
                Monsters.append([monsters.Monster(3, wave, False, Images, mapName),30*(i+3+j*7)])
            Monsters.append([monsters.Monster(4, wave, False, Images, mapName),30*(6+j*7)])
    elif wave == 13:
        for i in range(50):
            Monsters.append([monsters.Monster(2, wave, False, Images, mapName),15*(i)])
        for i in range(23):
            Monsters.append([monsters.Monster(3, wave, False, Images, mapName),15*(i+50)])
    elif wave == 14:
        for i in range(10):
            Monsters.append([monsters.Monster(3, wave, False, Images, mapName),30*(i)])
        for i in range(20):
            Monsters.append([monsters.Monster(2, wave, False, Images, mapName),30*(i+10)])
        for i in range(8):
            Monsters.append([monsters.Monster(4, wave, False, Images, mapName),30*(i+30)])
    elif wave == 15:
        for j in range(5):
            Monsters.append([monsters.Monster(1, wave, False, Images, mapName),30*(1+j*5)])
            Monsters.append([monsters.Monster(2, wave, False, Images, mapName),30*(2+j*5)])
            Monsters.append([monsters.Monster(3, wave, False, Images, mapName),30*(3+j*5)])
            Monsters.append([monsters.Monster(4, wave, False, Images, mapName),30*(4+j*5)])
            Monsters.append([monsters.Monster(5, wave, False, Images, mapName),30*(5+j*5)])
    elif wave == 16:
        for j in range(8):
            for i in range(5):
                Monsters.append([monsters.Monster(3, wave, False, Images, mapName),30*(i+j*6)])
            Monsters.append([monsters.Monster(4, wave, False, Images, mapName),30*(5+j*6)])
    elif wave == 17:
        for i in range(12):
            Monsters.append([monsters.Monster(4, wave, False, Images, mapName),30*(i)])
    elif wave == 18:
        for i in range(80):
            Monsters.append([monsters.Monster(3, wave, False, Images, mapName),20*(i)])
    elif wave == 19:
        for i in range(5):
            Monsters.append([monsters.Monster(3, wave, False, Images, mapName),30*(i)])
        for i in range(7):
            Monsters.append([monsters.Monster(5, wave, False, Images, mapName),30*(i+5)])
        for i in range(10):
            Monsters.append([monsters.Monster(4, wave, False, Images, mapName),30*(i+12)])
    elif wave == 20:
        for i in range(5):
            Monsters.append([monsters.Monster(6, wave, False, Images, mapName),30*(i)])

        Monsters.append([monsters.Monster(7, wave, False, Images, mapName), 150])
    elif wave == 21:
        for j in range(7):
            for i in range(5):
                Monsters.append([monsters.Monster(4, wave, False, Images, mapName),30*(i+j*6)])
            Monsters.append([monsters.Monster(5, wave, False, Images, mapName),30*(5+j*6)])
    elif wave == 22:
        for i in range(16):
            Monsters.append([monsters.Monster(6, wave, False, Images, mapName),60*(i)])
    elif wave == 23:
        for i in range(7):
            Monsters.append([monsters.Monster(5, wave, False, Images, mapName),30*(i*2)])
            Monsters.append([monsters.Monster(6, wave, False, Images, mapName),30*(i*2+1)])
    elif wave == 24:
        for i in range(5):
            Monsters.append([monsters.Monster(3, wave, True, Images, mapName),30*(i)])
    elif wave % 25 == 0 and wave != 25:
        Monsters.append([monsters.Monster(10, wave, False, Images, mapName),30])
    else:
        for i in range(random.randint(5,15)):
            n = random.randint(1, 100)
            if n <= 40-wave:
                Monsters.append([monsters.Monster(1, wave, random.randint(1,10)==1, Images, mapName),random.randint(15,30)*(i)])
            elif n <= 50-wave:
                Monsters.append([monsters.Monster(2, wave, random.randint(1,10)==1, Images, mapName),random.randint(15,30)*(i)])
            elif n <= 65-wave:
                Monsters.append([monsters.Monster(3, wave, random.randint(1,10)==1, Images, mapName),random.randint(15,30)*(i)])
            elif n <= 75-wave:
                Monsters.append([monsters.Monster(4, wave, random.randint(1,10)==1, Images, mapName),random.randint(15,30)*(i)])
            elif n <= 85-wave:
                Monsters.append([monsters.Monster(5, wave, random.randint(1,10)==1, Images, mapName),random.randint(15,30)*(i)])
            elif n <= 100-wave:
                Monsters.append([monsters.Monster(6, wave, random.randint(1,10)==1, Images, mapName),random.randint(15,30)*(i)])
            elif n <= 125-wave:
                Monsters.append([monsters.Monster(7, wave, False, Images, mapName),random.randint(15,30)*(i)])
            elif n <= 130-wave:
                Monsters.append([monsters.Monster(8, wave, random.randint(1,10)==1, Images, mapName),random.randint(15,30)*(i)])
            elif n <= 175-wave: 
                Monsters.append([monsters.Monster(9, wave, random.randint(1,10)==1, Images, mapName),random.randint(15,30)*(i)])
            elif n <= 200-wave:
                Monsters.append([monsters.Monster(10, wave, False, Images, mapName),random.randint(15,30)*i])
    return Monsters
