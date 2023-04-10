from pygame.locals import *
import sys, time
import os
import os.path

import numpy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

import gc
import xlrd
import pygame
import itertools
import distutils.dir_util


tilesize = 30

array_addx,array_addy=(0,0)

Moving=False

array = []
empty = []


#C:\Users\User\AppData\Local\Programs\Python\Python310

v2="C:/Python27/"
v3="C:/Users/User/AppData/Local/Programs/Python/Python310/"

using_version=v3

base=using_version+"FIRE_EMBLEM_SAVE_FILES/"
base_backgrounds=using_version+"pics/backgrounds/"
base_extras=using_version+"pics/extras/"
base_tiles=using_version+"pics/tiles/"
base_unit_images=using_version+"pics/unit_images/"

green=pygame.image.load(base_extras+"greenoccupy2.png")
red=pygame.image.load(base_extras+"redTileFinalTry4.png")
blue=pygame.image.load(base_extras+"blue30x30.png")

pygame.init()

arrow=pygame.image.load(base_extras+"arrow5.png")

Font = pygame.font.SysFont(None, 16)
FontSmaller = pygame.font.SysFont(None, 15)
FontSmaller2 =pygame.font.SysFont(None, 12)
FontTiny=pygame.font.SysFont(None, 8)



_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, font, gfcolor=(255,255,255), ocolor=(0,0,0), opx=1):
    
    textsurface = font.render(str(text), True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(str(text), True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    
    return surf



def returnPic(className):
    toreturn=False
    for y in range(1,59):
        if str(sheet.cell_value(y,0))==className:
            try:
                toreturn=pygame.image.load(base_unit_images+str(sheet.cell_value(y,16).replace("\"", "")))
            except IOError:
                print('missing2: '+str(sheet.cell_value(y,16).replace("\"", "")))
                sys.exit()
            break
    return toreturn



def blitText(item,bg):
    Font=item.Font

    pygame.draw.rect(screen,bg,(item.x,item.y,item.width,item.height))
    pygame.draw.rect(screen,(0,0,0),(item.x,item.y,item.width,item.height),1)

    useFont=Font
    addX,addY=(0,0)
    TextMod = useFont.render(item.text, 1, (0,10,10))
    screen.blit(TextMod, (item.x+2,item.y+4))



mapwidth,mapheight=(720+200+300-10,640)

class TextE:
    def __init__(self,x,y,text,Font):
        self.Font=Font
        self.text = text
        self.size = Font.size(str(text))
        self.x,self.y = (x,y)
        self.width,self.height = (self.size[0]+4,self.size[1]+8)
        self.selected=False



saveCancel=[]
            

filename = base+"allClasses.xls" #this will be changing soon enough
workbook = xlrd.open_workbook(filename)
sheet = workbook.sheet_by_index(0)

class Button:
    def __init__(self,x,y,text,save="bs",main="main",one="one",two="two",three="three",four="four",five="five",empty="empty",pic="pic",whenenter="whenenter"):

        self.text = text
        self.size = Font.size(str(text))
        
        self.x,self.y = (x,y)
        if len(self.text)==1:
            #test=int(str(self.text))
            self.width,self.height = (12,20)
        elif str(self.text[:4]) in [" LVL"," PRE"]:
            self.width,self.height = (28,14)

        elif str(self.text[:5]) in [" Test"]:
            self.width,self.height = (55,14)
            
        else:
            self.width,self.height = (self.size[0],self.size[1]+8)

        self.save=save
        self.main=main
        self.one=one
        self.two=two
        self.three=three
        self.four=four
        self.five=five
        self.empty=empty
        self.whenenter=whenenter

        if str(pic)[:8]!="<Surface":#isinstance(pic,Surface):
            self.pic=returnPic(main[1])
            if returnPic(main[1]) is False:
                self.pic=2
        else:
            self.pic=pic
        Button.pic=self.pic
            

        try:
            self.num=int(str(text)[:-1])
        except ValueError:
            self.num=100



######################################################################

allClasses=[]

def returnClass(y):
    name=str(sheet.cell_value(y,1))

    saveWpnTypes=[]
    divide=str(sheet.cell_value(y,15))

    wpnTypes=divide.split(",")
    for weapon in wpnTypes:
        newW=weapon.replace("\"", "")
        saveWpnTypes.append(newW)
    
    addStats=[]
    for j in range(4,14):
        addStats.append(int(sheet.cell_value(y,j)))

    addLvl=[]
    for j in range(18,26):
        addLvl.append(int(sheet.cell_value(y,j)))

    try:
        pic=pygame.image.load(base_unit_images+str(sheet.cell_value(y,16).replace("\"", "")))
    except IOError:
        print('missing0: '+name+'  '+base_unit_images+str(sheet.cell_value(y,16).replace("\"", "")))
        sys.exit()
    try:
        pic_grey=pygame.image.load(base_unit_images+str(sheet.cell_value(y,17).replace("\"", "")))
    except IOError:
        print('missing1: '+name+'  '+base_unit_images+str(sheet.cell_value(y,17).replace("\"", "")))
        sys.exit()

        
    actualName=str(sheet.cell_value(y,0))
        
    return [name,saveWpnTypes,addStats,addLvl,pic,pic_grey,actualName,y]


######################################################################
        
class EnemyClass:
    def __init__(self,theList):
        name=theList[0]
        WeaponTypes=theList[1]
        stats=theList[2]
        newLvl=theList[3]
        pic=theList[4]
        pic_grey=theList[5]
        actualName=theList[6]

        self.saveNum=int(theList[7])
        EnemyClass.saveNum=self.saveNum
        
        #well this was a stupid way to do this
        self.name=name
        self.actualName=actualName
        self.WeaponTypes=WeaponTypes
        self.stats=stats
        self.newLvl=newLvl
        self.pic=pic
        self.pic_grey=pic_grey

        EnemyClass.name=self.name
        EnemyClass.actualName=self.actualName
        EnemyClass.WeaponTypes=self.WeaponTypes
        EnemyClass.stats=self.stats
        EnemyClass.newLvl=self.newLvl
        EnemyClass.pic=self.pic
        EnemyClass.pic_grey=self.pic_grey


#"there has to be a better way" -Wesley Kent, circa 2018, RIP
Brute=EnemyClass(returnClass(1))
Savage=EnemyClass(returnClass(2))
BeineSword=EnemyClass(returnClass(3))
BeineLance=EnemyClass(returnClass(4))
BeineBow=EnemyClass(returnClass(5))
WightSword=EnemyClass(returnClass(6))
WightLance=EnemyClass(returnClass(7))
WightBow=EnemyClass(returnClass(8))
Rotaur=EnemyClass(returnClass(9))
Vong=EnemyClass(returnClass(10))
ArchVong=EnemyClass(returnClass(11))
Farlan=EnemyClass(returnClass(12))
Kevros=EnemyClass(returnClass(13))
Rokian=EnemyClass(returnClass(14))
Darrak=EnemyClass(returnClass(15))
Oqriid=EnemyClass(returnClass(16))
Cyphiis=EnemyClass(returnClass(17))
Vraeld=EnemyClass(returnClass(18))
ElderVraeld=EnemyClass(returnClass(19))
Elmaer=EnemyClass(returnClass(20))
Elmaeve=EnemyClass(returnClass(21))
Oricael=EnemyClass(returnClass(22))
Nightmorph=EnemyClass(returnClass(23))

Lord2=EnemyClass(returnClass(24))
StormLord2=EnemyClass(returnClass(25))
Mercenary2=EnemyClass(returnClass(26))
Champion2=EnemyClass(returnClass(27))
Swordsman2=EnemyClass(returnClass(28))
BladeLord2=EnemyClass(returnClass(29))
Thief2=EnemyClass(returnClass(30))
Assassin2=EnemyClass(returnClass(31))
DarkKnight2=EnemyClass(returnClass(32))
DeathKnight2=EnemyClass(returnClass(33))
Soldier2=EnemyClass(returnClass(34))
Sentinel2=EnemyClass(returnClass(35))
Fighter2=EnemyClass(returnClass(36))
Warrior2=EnemyClass(returnClass(37))
Marauder2=EnemyClass(returnClass(38))
Pirate2=EnemyClass(returnClass(39))
Archer2=EnemyClass(returnClass(40))
Ranger2=EnemyClass(returnClass(41))
Cavalier2=EnemyClass(returnClass(42))
Paladin2=EnemyClass(returnClass(43))
PegasusKnight2=EnemyClass(returnClass(44))
WyvernKnight2=EnemyClass(returnClass(45))
Manakete2=EnemyClass(returnClass(46))
Mage2=EnemyClass(returnClass(47))
BattleMage2=EnemyClass(returnClass(48))
Shaman2=EnemyClass(returnClass(49))
ArchShaman2=EnemyClass(returnClass(50))
Druid2=EnemyClass(returnClass(51))
Necromancer2=EnemyClass(returnClass(52))
Priest2=EnemyClass(returnClass(53))
BattlePriest2=EnemyClass(returnClass(54))
Healer2=EnemyClass(returnClass(55))
WhiteMage2=EnemyClass(returnClass(56))
Knight2=EnemyClass(returnClass(57))
General2=EnemyClass(returnClass(58))

allClasses2=[]
allClasses=[]


other=[]

#collect above classes into groups by their class type
for obj in gc.get_objects():
    if isinstance(obj, EnemyClass):
        allClasses.append(obj)



factionList2=[('Dasmein',(110,10,10)),('Infernal',(20,20,20)),('Caniel',(50,55,115)),('Thayrn',(50,115,55)),('Ushein',(130,130,130)),('Koswor',(114,50,114))]
factionList=[]

class otherButton:
    def __init__(self,name,color):
        self.name=name
        self.surf_1=pygame.Surface((30,30),pygame.SRCALPHA,32)
        self.surf_1.fill(color)
        self.pic=self.surf_1
class otherButton2:
    def __init__(self,name,pic):
        self.name=name
        self.pic=pic
            
for item in factionList2:
    factionList.append(otherButton(item[0],item[1]))


#########################################################################################################

class Weapon:
    def __init__(self,name,rank,rang,uses,max_uses,weight,dmg,hit,wpnType,value,crit):
        self.name = name
        self.hit=hit
        self.wpnType=wpnType
        self.rang = rang
        self.rank=rank
        self.dmg = dmg
        self.crit=crit
        self.value = value
        self.weight = weight
        self.uses=uses
        self.max_uses=max_uses

        Weapon.name=self.name
        Weapon.hit=self.hit
        Weapon.wpnType=self.wpnType
        Weapon.rang=self.rang
        Weapon.rank=self.rank
        Weapon.dmg=self.dmg
        Weapon.crit=self.crit
        Weapon.value=self.value
        Weapon.weight=self.weight
        Weapon.uses=self.uses
        Weapon.max_uses=self.max_uses


class Item:
    def __init__(self,name,value,uses,max_uses):
        self.name = name
        self.value = value
        self.uses=uses
        self.max_uses=max_uses

        Item.name=self.name
        Item.value=self.value
        Item.uses=self.uses
        Item.max_uses=self.max_uses

class UsableItem:#ie master seal or dracoshield
    def __init__(self,name,value,uses,max_uses,bonusWhat):
        self.name = name
        self.value = value
        self.uses=uses
        self.max_uses=max_uses
        self.bonusWhat=bonusWhat

        Item.name=self.name
        Item.value=self.value
        Item.uses=self.uses
        Item.max_uses=self.max_uses
        Item.bonusWhat=self.bonusWhat



class Staff:
    def __init__(self,name,rank,rang,uses,max_uses,addHeal,addXP,wpnType,value):
        self.name = name
        self.wpnType=wpnType
        self.rang = rang
        self.rank=rank
        self.addHeal = addHeal
        self.addXP = addXP
        self.value = value
        self.uses=uses#1
        self.max_uses=max_uses

        Staff.name=self.name
        Staff.wpnType=self.wpnType
        Staff.rang=self.rang
        Staff.rank=self.rank
        Staff.addHeal=self.addHeal
        Staff.addXP=self.addXP
        Staff.value=self.value
        Staff.uses=self.uses
        Staff.max_uses=self.max_uses




Vulnerary=Item("Vulnerary",150,3,3)
Elixir=Item("Elixir",1500,3,3)
DoorKey=Item("Door Key",50,1,1)
ChestKey=Item("Chest Key",150,3,3)
Empty=Item("------",0,0,0)

DivineBlessing=UsableItem("Divine Blessing",1200,1,1,"Luck")#
Dragonskin=UsableItem("Dragonskin",1200,1,1,"Defense")#
Speedwing=UsableItem("Speedwing",1200,1,1,"Speed")#
SecretTome=UsableItem("Secret Tome",1200,1,1,"Skill")
CelestialHelm=UsableItem("Celestial Helm",1200,1,1,"Health")#
SpiritTome=UsableItem("Spirit Tome",1200,1,1,"Magic")#
EnergyBand=UsableItem("Energy Band",1200,1,1,"Strength")#

#YellowJewel=Item("Yellow Gem",2000,1,1)
RedJewel=Item("Red Gem",4000,1,1)
BlueJewel=Item("Blue Gem",6000,1,1)
GreenJewel=Item("Green Gem",8000,1,1)
PurpleJewel=Item("Purple Gem",12000,1,1)
WhiteJewel=Item("White Gem",20000,1,1)

ReserveS=Item("Darik Reserve (S)",20000,1,1)
ReserveM=Item("Darik Reserve (M)",30000,1,1)
ReserveL=Item("Darik Reserve (L)",40000,1,1)
ReserveXL=Item("Darik Reserve (XL)",60000,1,1)

ALL_ITEMS2=[ReserveS,ReserveM,ReserveL,ReserveXL,RedJewel,BlueJewel,PurpleJewel,GreenJewel,WhiteJewel,Vulnerary,Elixir,DoorKey,ChestKey,DivineBlessing,Dragonskin,Speedwing,SecretTome,CelestialHelm,SpiritTome,EnergyBand]#Empty
ALL_ITEMS=[]


keypic=pygame.image.load(base_extras+"key.png")
coinspic=pygame.image.load(base_extras+"coins.png")
vulnpic=pygame.image.load(base_extras+"lesserSpecialPotion.png")
jewelpic=pygame.image.load(base_extras+"ring.png")
tomepic=pygame.image.load(base_extras+"try8.png")


#for i in range(len(ALL_ITEMS2)):
for item in ALL_ITEMS2:
    if item.name[0:5]=='Darik':
        Pic=coinspic
    elif item.name[-3:]=="Key":
        Pic=keypic
    elif item.name[-3:]=="Gem":
        Pic=jewelpic
    elif item.name in ["Vulnerary","Elixir"]:
        Pic=vulnpic
    elif item.__class__.__name__=="UsableItem":
        Pic=tomepic
    else:
        Pic=red

    ALL_ITEMS.append(otherButton2(item.name,Pic))













DISPLAY_OPTIONS=False
DISPLAY_LIST=[]

filename2 = base+"allWpns.xls"
workbook2 = xlrd.open_workbook(filename2)
sheet2 = workbook2.sheet_by_index(0)


def returnWpnType(i):
    #how this info is stored
    if i in [0,1,2]:
        wpnType="Magic"
    elif i == 3:
        wpnType="Sword"
    elif i == 4:
        wpnType="Lance"
    elif i == 5:
        wpnType="Axe"
    elif i == 6:
        wpnType="Bow"
    elif i == 7:
        wpnType="Claw"
    elif i == 8:
        wpnType="Fang"
    elif i == 9:
        wpnType="Darkness"
    elif i == 10:
        wpnType="Dragon Fire"
    elif i == 11:
        wpnType="Stave"
    return wpnType


weaponsList=[]

lightMagic=[]
elementalMagic=[]
darkMagic=[]
allMagic=[]

allBows=[]
allLances=[]
allSwords=[]
allAxes=[]

allStaves=[]
allGear=[]

enemyWeapons=[]

allClaws=[]
allFangs=[]
allEvilMagic=[]
dragonFire=[]
allMelee=[]


#for loading in weapons by rows --> this will also be changing: reference new files for example
allSpots=[(1,10),(17,26),(34,43),(53,70),(81,97),(107,124),(132,143),(152,157),(157,159),(159,162),(162,164),(164,165)]
for i in range(len(allSpots)):
    setx=allSpots[i]
    for y in range(setx[0],setx[1]):
        name=str(sheet2.cell_value(y,0))
        rank=str(sheet2.cell_value(y,1))
        rang=float(sheet2.cell_value(y,2))
        uses=int(sheet2.cell_value(y,3))
        max_uses=int(sheet2.cell_value(y,4))
        weight=int(sheet2.cell_value(y,5))
        dmg=int(sheet2.cell_value(y,6))
        hit=int(sheet2.cell_value(y,7))
        wpnType=returnWpnType(i)
        value=int(sheet2.cell_value(y,8))
        crit=int(sheet2.cell_value(y,9))

        W=Weapon(name,rank,rang,uses,max_uses,weight,dmg,hit,wpnType,value,crit)

        if i==0:
            darkMagic.append(W)
        elif i==1:
            elementalMagic.append(W)
        elif i==2:
            lightMagic.append(W)
        elif i==3:
            allSwords.append(W)
        elif i==4:
            allLances.append(W)
        elif i==5:
            allAxes.append(W)
        elif i==6:
            allBows.append(W)
        elif i==7:
            allClaws.append(W)
        elif i==8:
            allFangs.append(W)
        elif i==9:
            allEvilMagic.append(W)
        elif i==10:
            dragonFire.append(W)
        elif i==11:
            allMelee.append(W)
            

#initially these were manually defined, this will need to change to the updated ods file format
Heal=Staff("Heal","E",1,20,20,5,10,"Staff",600)
Mend=Staff("Mend","D",1,16,16,15,20,"Staff",1000)
Warp=Staff("Warp","C",1,5,5,10,50,"Staff",2000)
Recover=Staff("Recover","C",1,15,15,100,25,"Staff",2250)
Physic=Staff("Physic","B",1,15,15,10,30,"Staff",3750)
Fortify=Staff("Fortify","A",1,8,8,10,50,"Staff",8000)
Latona=Staff("Latona","S",1,3,3,100,60,"Staff",8000)

allStaves=[Heal,Mend,Warp,Recover,Physic,Fortify,Latona]


ALL_WEAPONS2=[allStaves,lightMagic,elementalMagic,darkMagic,allBows,allLances,allSwords,allAxes,allClaws,allFangs,allEvilMagic,dragonFire,allMelee]
ALL_WEAPONS=[]





#basic images for when choosing an enemy's weapon
BW=pygame.transform.scale(pygame.image.load(base_extras+"bowski.png"),(30,30))
SW=pygame.transform.scale(pygame.image.load(base_extras+"swordski.png"),(30,30))
AX=pygame.transform.scale(pygame.image.load(base_extras+"axie.png"),(30,30))
LC=pygame.transform.scale(pygame.image.load(base_extras+"lanceski.png"),(30,30))
LG=pygame.transform.scale(pygame.image.load(base_extras+"lightski.png"),(30,30))
EL=pygame.transform.scale(pygame.image.load(base_extras+"eleski.png"),(30,30))
DK=pygame.transform.scale(pygame.image.load(base_extras+"darkski.png"),(30,30))
ST=pygame.transform.scale(pygame.image.load(base_extras+"staffski.png"),(30,30))

CLAW=pygame.transform.scale(pygame.image.load(base_extras+"clawsImg.png"),(30,30))
FANG=pygame.transform.scale(pygame.image.load(base_unit_images+"dog_grey.png"),(30,30))
MAGIC=pygame.transform.scale(pygame.image.load(base_unit_images+"MageManGrey.png"),(30,30))
FIRE=pygame.transform.scale(pygame.image.load(base_extras+"Fire01.png"),(30,30))
STAFF=pygame.transform.scale(pygame.image.load(base_unit_images+"bonewalker_imggreyL.png"),(30,30))


for i in range(len(ALL_WEAPONS2)):
    for item in ALL_WEAPONS2[i]:

        list_call_i=[ST,LG,EL,DK,BW,LC,SW,AX,CLAW,FANG,MAGIC,FIRE,STAFF]

        Pic=list_call_i[i]

        ALL_WEAPONS.append(otherButton2(item.rank+"--"+item.name,Pic))



#IN TIME EXPAND THIS TO INCLUDE NEUTRAL UNITS
ALL_ALLIES=[]
get_people=os.listdir(base+'SUPPLEMENTARY FILES/ALL_ALLIES/')
for _folder in get_people:
    get_info=open(base+'SUPPLEMENTARY FILES/ALL_ALLIES/'+_folder+'/1_.txt','r').read().split('\n')

    #okay, get all friendly units from folder
    try:
        ALL_ALLIES.append(otherButton2(get_info[1],pygame.image.load(base_unit_images+get_info[0])))
    except IOError:
        print('missing3: '+get_info[0])
        sys.exit()


NumOneThruThirty=[]
for i in range(1,31):
    NumOneThruThirty.append(otherButton2(str(i),pygame.image.load(base_extras+'empty_tile.png')))


#used when a new map is loaded
def reset(filename):
    
    temparray=[]

    File = open(base+"_ALLMAPS/"+str(filename)+"/MAP.txt", "r")

        
    lines = File.readlines()

    print("---------------------------------------------")

    ii=0
    Retain=False
    temparray=[]
    for line in lines:
        templine=str(line)
        templine=templine[1:]
        templine=templine[:-1]

        badList=["[","]","(",")",","]

        saveThis=""
        saveThisRotate=""
        tempLine=[]
        getRotate=False
        
        for letter in templine:
            letter=str(letter)
            if getRotate is False:
                if letter not in badList and Retain is True and str(letter) != "'":
                    saveThis+=str(letter)
                    

                elif str(letter) == "'": #add new info
                    if Retain is True:
                        Retain = False
                        ii+=1
                        getRotate=True
                    else:
                        Retain=True
                        

            #try out for numbers
            elif getRotate is True:
                
                if letter not in badList  and str(letter) != "," and str(letter) != " ":
                    #try:
                    if str(letter)=="-" or type(int(letter))==int:
                        saveThisRotate+=str(letter)
                    #except ValueError:
                        #print "wtf but why"
                elif str(letter)==")":
                    tempLine.append((str(saveThis),int(saveThisRotate)))

                    getRotate=False
                    saveThis=""
                    saveThisRotate=""

        temparray.append(tempLine)


    mapWidth=len(temparray[0])
    mapHeight=len(temparray)



    array=[]
    blank_list=[]
    for row in range(mapHeight):
        blank_list=[]
        for column in range(mapWidth):
            myIMG=str(temparray[row][column][0])

            try:#
                my_img=pygame.image.load(base_tiles+myIMG)
            except:
                my_img=pygame.image.load(base_extras+'redTileFinalTry5.png') #image no longer exists or something is corrupted
                print('I better not be reading this: '+ str(myIMG))
                #sys.exit()

            my_img=pygame.transform.rotate(my_img,temparray[row][column][1])

            blank_list.append((my_img,temparray[row][column][1],temparray[row][column][0]))

        array.append(blank_list)

    reset.array=array
    reset.temparray=temparray
    reset.mapWidth=mapWidth
    reset.mapheight=mapHeight


    #################################################################

    allyStartList=[]

    
    fileLocal = base+"_ALLMAPS/"+str(filename)+"/"
    allySTART=os.listdir(fileLocal+'ALLYSTART/')
    
    for _file_ in allySTART:
        um=open(base+"_ALLMAPS/"+str(filename)+"/ALLYSTART/"+_file_,'r').read().split('\n')

        TOADD=(int(um[0]),int(um[1]),_file_[:-4])
        allyStartList.append(TOADD)
        
        
    reset.allyStartList=allyStartList

    friendlyPos=[]
    for i in range(len(allyStartList)):
        item=allyStartList[i]
        friendlyPos.append(Button(50+(25*(i+1)),580,str(item[2]),[item[0],item[1]]))

    #################################################################################

    enemyPos=[]
    enemyPos2=[]
        
    enemyStartList=[]
    
    fileLocal = base+"_ALLMAPS/"+str(filename)+"/"
    enemySTART=os.listdir(fileLocal+'ENEMYSTART/')

    print(filename, fileLocal)


    ALL_ENEMIES_IN_PLAY=[]
    callEnemyUnitsSpawnTurns=[]

    
    for i in range(len(enemySTART)):

        _file_=enemySTART[i]
        
        main=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_.txt','r').read().split('\n')
        empty=open(fileLocal+"/ENEMYSTART/"+_file_+'/empty.txt','r').read().split('\n')
        whenentercheckonly=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_whenenter.txt','r').read().split('\n')


        #conduct check here for new format real quick
        try:
            #print whenentercheckonly[5]
            whenentercheckonlyCHECK=whenentercheckonly[1] #exception will occur if this file is not in the new format
            #print whenentercheckonlyCHECK, whenentercheckonly
            #print len(whenentercheckonly),'len'
        except IndexError: #older save type, fix it automatically
            #reset._WATERORLAVA="Water"
            amend=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_whenenter.txt','w')
            whenentercheckonly=['1','NA']# #other values are 'N', 'S', 'W', 'E'
            for line in whenentercheckonly:
                amend.writelines(line+'\n')
            amend.close()
        #whenenter=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_whenmove.txt','r').read().split('\n')[0]

        
        if empty[0]=="False":#if not in play, why should I care

            buildList=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_whenenter.txt','r').read().split('\n')[0]
            if buildList not in callEnemyUnitsSpawnTurns:
                callEnemyUnitsSpawnTurns.append(buildList)

            #below Line is ONLY for the WIN CONDITIONS
            #print 'main[0]: ',main[0]
            ALL_ENEMIES_IN_PLAY.append(otherButton2(main[0],pygame.image.load(base_extras+'empty_tile.png')))
            
            #print 'countme',item.text
            #print 'before: ',main

            groupedAll=main[9:len(main)]#get all units in their move group

            #below two lines for testing - delete after
            #to_edit=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+item.text+'/1_.txt','r').read().split('\n')
            #print item.text, 'before: ',to_edit


            #okay we gonna fix it here
            to_edit=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_.txt','r').read().split('\n')
            to_edit=to_edit[:9]
            tempnewMoveGroup=groupedAll[:]
            if _file_ not in tempnewMoveGroup:
                tempnewMoveGroup.append(_file_)

            newMoveGroup=[]
            for _temp_ in tempnewMoveGroup:
                if open(fileLocal+"/ENEMYSTART/"+_temp_+'/empty.txt','r').read().split('\n')[0]=="False":#means IS in play
                    newMoveGroup.append(_temp_)


            to_edit=to_edit+newMoveGroup            
            to_edit2=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_.txt','w')


            for _j in range(len(to_edit)):
                jj=to_edit[_j]
                addd=""
                if _j+1!=len(to_edit):
                    addd="\n"
                to_edit2.write(str(jj)+addd)
            
            to_edit2.close()


    reset._callEnemyUnitsSpawnTurns=callEnemyUnitsSpawnTurns
    reset.ALL_ENEMIES_IN_PLAY=ALL_ENEMIES_IN_PLAY[:]
    

    for i in range(len(enemySTART)):#should be 54

        if i >= 0 and  i<27:#was 20, changed it
            thisYY=580
            thisXX=i
        else:
            thisYY=610
            thisXX=i-27#was 20, changed it
    
        _file_=enemySTART[i]
        
        main=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_.txt','r').read().split('\n')
        spot1=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_spot1(weapon).txt','r').read().split('\n')
        spot2=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_spot2.txt','r').read().split('\n')
        spot3=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_spot3.txt','r').read().split('\n')
        spot4=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_spot4.txt','r').read().split('\n')
        spot5=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_spot5.txt','r').read().split('\n')
        empty=open(fileLocal+"/ENEMYSTART/"+_file_+'/empty.txt','r').read().split('\n')

        #print fileLocal

        whenenter=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_whenenter.txt','r').read().split('\n')#[0]

        try:
            #if _file_=='1_':
                #enemyPos.append(Button(50+((thisXX+1)*25),thisYY,str(_file_),False,main,spot1,spot2,spot3,spot4,spot5,empty,main[1],whenenter))
            #else: #the hell was this here for again?
            enemyPos2.append(Button(50+((thisXX+1)*25),thisYY,str(_file_),False,main,spot1,spot2,spot3,spot4,spot5,empty,main[1],whenenter))
        except IndexError:
            print(fileLocal+"/ENEMYSTART/"+_file_)
            

    for item in enemyPos2:
        startZero=0
        
        try:
            while int(enemyPos[startZero].num)<int(item.num):
                startZero+=1
        except IndexError:
            pass
        
        enemyPos.insert(startZero,item)

    for i in range(len(enemyPos)):
        if i >= 0 and  i<27:#was 20, changed it
            thisYY=580
            thisXX=i
        else:
            thisYY=610
            thisXX=i-27#was 20, changed it

        enemyPos[i].x,enemyPos[i].y=(50+((thisXX+1)*25),thisYY)

        


###################################################################################################################################
        
    reset.enemyPos=enemyPos
    reset.friendlyPos=friendlyPos


    fileLocal = base+"_ALLMAPS/"+str(filename)+"/"
#WINCONDITIONS
    howWin=open(fileLocal+'WINCONDITIONS.txt','r').read().split('\n')
    reset._WINCONDITIONS=howWin

    
    if howWin[0]=="KILL":
        gotHim="Could not find on map."
        for i in range(len(enemySTART)):#should be 54
        
            _file_=enemySTART[i]
            
            main=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_.txt','r').read().split('\n')
            #empty=open(fileLocal+"/ENEMYSTART/"+_file_+'/1_.txt','r').read().split('\n')
            if main[0]==howWin[1]:
                gotHim=str(_file_)

                if open(fileLocal+"/ENEMYSTART/"+_file_+'/empty.txt','r').read().split('\n')[0]=="True":
                    gotHim=" Unit exists, not in play: "+str(_file_)
                break

        reset._killWho=gotHim

            
#EXTRA-CHAPTER NUMBER
    chpNUM=open(fileLocal+'EXTRA.txt','r').read().split('\n')
    reset._CHPNUM=int(chpNUM[0])
#EXTRA-CHAPTER NAME
    reset._CHPNAME=str(chpNUM[1])
#EXTRA-WATER OR LAVA
    try:
        reset._WATERORLAVA=str(chpNUM[3])
        
    except IndexError: #older save type, fix it
        reset._WATERORLAVA="Water"
        amend=open(fileLocal+'EXTRA.txt','w')

        chpNUM.append('Water')
        for line in chpNUM:
            amend.writelines(line+"\n")
        amend.close()
        

#RECRUITABLE
    getAllRecruits=os.listdir(fileLocal+'RECRUITABLE/')
    allRecruits=[]
    
    for i in range(int(len(getAllRecruits)/2)):#there are two files per person
        
        
        recruit1=open(fileLocal+'RECRUITABLE/'+str(i+1)+'_.txt','r').read().split('\n')
        recruit1_convo=open(fileLocal+'RECRUITABLE/'+str(i+1)+'_convo.txt','r').read().split('\n')
        recruit_mod=[recruit1[0],recruit1[1:len(recruit1)],recruit1_convo]
        #recruit2=open(fileLocal+'RECRUITABLE/'+str(i)+'_convo.txt','r').read().split('\n')

        print(recruit_mod)

        allRecruits.append(recruit_mod)

                     

    reset._RECRUITABLE=allRecruits


        
#CHESTS
    _CHESTS=[]

    openChests=os.listdir(fileLocal+'LOOT_VILLAGECHEST/CHEST/')#,'r').read().split('\n')
    for _file in openChests:
        openedChest=open(fileLocal+'LOOT_VILLAGECHEST/CHEST/'+_file,'r').read().split('\n')
        _CHESTS.append([int(openedChest[1]),int(openedChest[2]),str(openedChest[3]),str(_file)])
    reset._CHESTS=_CHESTS


#VILLAGE
    _VILLAGES=[]

    openVillages=os.listdir(fileLocal+'LOOT_VILLAGECHEST/VILLAGE/')#,'r').read().split('\n')
    for _file in openVillages:
        openedVillage=open(fileLocal+'LOOT_VILLAGECHEST/VILLAGE/'+_file,'r').read().split('\n')
        _VILLAGES.append([int(openedVillage[1]),int(openedVillage[2]),str(openedVillage[3]),str(_file)])#openedVillage[4:]])
    reset._VILLAGES=_VILLAGES


#ARMORY
    _ARMORIES=[]
    reset._ARMORIES=[]

    allArmories=os.listdir(fileLocal+'LOOT_VILLAGECHEST/ARMORY/')

    for _file in allArmories:
        openedArmory=open(fileLocal+'LOOT_VILLAGECHEST/ARMORY/'+_file,'r').read().split('\n')
        print(openedArmory)
        modifiedArmory=[_file[0:2],openedArmory[0],openedArmory[1],openedArmory[2]]
        for i in range(len(openedArmory)-3): #first two=x,y
            #modifiedArmory.appen
            getLine=openedArmory[i+3] #this omits the last one (see above -3) since that is secret shop
            getIndex=getLine.find(":")
            getName=getLine[0:getIndex]
            getCount=getLine[getIndex+1:len(getLine)]

            if getName!="":#accidental blank line in file
                modifiedArmory.append([getName,getCount])

        #print modifiedArmory
            
        reset._ARMORIES.append(modifiedArmory)




    _VENDORS=[]
    reset._VENDORS=[]

    allVendors=os.listdir(fileLocal+'LOOT_VILLAGECHEST/VENDOR/')

    for _file in allVendors:
        openedVendor=open(fileLocal+'LOOT_VILLAGECHEST/VENDOR/'+_file,'r').read().split('\n')
        print(openedVendor)
        modifiedVendor=[_file[0:2],openedVendor[0],openedVendor[1],openedVendor[2]]
        for i in range(len(openedVendor)-3): #first two=x,y
            getLine=openedVendor[i+3]
            getIndex=getLine.find(":")
            getName=getLine[0:getIndex]
            getCount=getLine[getIndex+1:len(getLine)]

            if getName!="":#accidental blank line in file
                modifiedVendor.append([getName,getCount])
            
        reset._VENDORS.append(modifiedVendor)


    #OLD way - remove this later with updated version
    convo_map_1=open(fileLocal+'1_conversation_intro/MAP_BG.txt','r').read().split('\n')
    convo_map_2=open(fileLocal+'2_conversation_intro2/MAP_BG.txt','r').read().split('\n')
    convo_map_4=open(fileLocal+'4_conversation_end1/MAP_BG.txt','r').read().split('\n')

    if len(convo_map_1)<4:#mean ellipse
        reset.convo_map_1_type=convo_map_1#(convo_map_1[0],convo_map_1,[1]) #should be ellipse, followed by a number
    else:
        reset.convo_map_1_type=('MAP')

    if len(convo_map_2)<4:#mean ellipse
        reset.convo_map_2_type=convo_map_2#(convo_map_2[0],convo_map_2,[1]) #should be ellipse, followed by a number
    else:
        reset.convo_map_2_type=('MAP')

    if len(convo_map_4)<4:#mean ellipse
        reset.convo_map_4_type=convo_map_4#(convo_map_4[0],convo_map_4,[1]) #should be ellipse, followed by a number
    else:
        reset.convo_map_4_type=('MAP')
    

    

def getLevelInfo(levelName=" LVL 1"): #irrelevant (I think)

    if levelName[-1] in [str(i) for i in range(0,10)]:
        if levelName[-2] in [str(i) for i in range(0,10)]:
            if levelName[1]=="L":#level, not test
                folderName_partOne="LEVEL_"
            elif levelName[1]=="T":
                folderName_partOne="TEST_"
            else:
                print(levelName, 'error')
                pygamequit()#something seriously wrong with the folder structure
                sys.exit()
            atChapter=folderName_partOne+str(levelName[-2]+levelName[-1])
        else:
            if levelName[1]=="L":#level, not test
                folderName_partOne="LEVEL_"
            elif levelName[1]=="T":
                folderName_partOne="TEST_"
            else:
                print(levelName, 'error')
                pygamequit()#something seriously wrong with the folder structure
                sys.exit()
            atChapter=folderName_partOne+str(levelName[-1])
            
    elif levelName[-1]=="Q":
        atChapter="PREQUEL"


    return atChapter


#default to chapter one at startup
filename="LEVEL_1"
filename2=" LVL 1"

currentFile=getLevelInfo(filename2)

reset(filename)
array=reset.array
temparray=reset.temparray
mapWidth=reset.mapWidth
mapHeight=reset.mapheight
friendlyPos=reset.friendlyPos
enemyPos=reset.enemyPos



timer=0

OptionGroup = pygame.sprite.Group() #why did I do it this way again??

gridStatus=False

#buttons' hover bg color AND click recognition is dependant solely on their location denoted below
#the height and width is dictated by the length of the text on the screen for simplicity's sake
Button0 = Button((7),8," Save tile map ")
Button1 = Button((7),32," Full Backup to Z: ")
Button2 = Button((7),56," Quit ")
Button3 = Button((9),512,"  <<  ")
Button4 = Button((9),542,"  <<  ")
Button5 = Button((9)+68,512,"  >>  ")
Button6 = Button((9)+68,542,"  >>  ")
Button7 = Button(10,449," Fill map w/ img ")
Button8= Button(10,476," Grid on/off ")
Button9 = Button(862,30,"Edit")
Button10= Button(888,30,"Move")
Button11= Button(895,106,"Rot")


#I don't want to hear about this. It works. Ignore the copy / paste.
ButtonMap0=Button(862,185," PREQ")
ButtonMap1=Button(891,185," LVL 1")
ButtonMap2=Button(862,200," LVL 2")
ButtonMap3=Button(891,200," LVL 3")
ButtonMap4=Button(862,215," LVL 4")
ButtonMap5=Button(891,215," LVL 5")
ButtonMap6=Button(862,230," LVL 6")
ButtonMap7=Button(891,230," LVL 7")
ButtonMap8=Button(862,245," LVL 8")
ButtonMap9=Button(891,245," LVL 9")
ButtonMap10=Button(862,260," LVL 10")
ButtonMap11=Button(891,260," LVL 11")
ButtonMap12=Button(862,275," LVL 12")
ButtonMap13=Button(891,275," LVL 13")
ButtonMap14=Button(862,290," LVL 14")
ButtonMap15=Button(891,290," LVL 15")
ButtonMap16=Button(862,305," LVL 16")
ButtonMap17=Button(891,305," LVL 17")
ButtonMap18=Button(862,320," LVL 18")
ButtonMap19=Button(891,320," LVL 19")
ButtonMap20=Button(862,335," LVL 20")
ButtonMap21=Button(891,335," LVL 21")
ButtonMap22=Button(862,350," LVL 22")
ButtonMap23=Button(891,350," LVL 23")
ButtonMap24=Button(862,365," LVL 24")
ButtonMap25=Button(891,365," LVL 25")

ButtonMap26=Button(862,380," Test Map 1")
ButtonMap27=Button(862,395," Test Map 2")
ButtonMap28=Button(862,410," Test Map 3")
ButtonMap29=Button(862,425," Test Map 4")


Turn1=Button(862,473,"1")
Turn2=Button(876,473,"2")
Turn3=Button(890,473,"3")
Turn4=Button(904,473,"4")

Turn5=Button(862,493,"5")
Turn6=Button(876,493,"6")
Turn7=Button(890,493,"7")
Turn8=Button(904,493,"8")

Turn9=Button(862,513,"9")
Turn10=Button(876,513,"10")
Turn11=Button(890,513,"11")
Turn12=Button(904,513,"12")

Turn13=Button(862,533,"13")
Turn14=Button(876,533,"14")
Turn15=Button(890,533,"15")
Turn16=Button(904,533,"16")
TurnAll=Button(862,552," All Turns ")


ButtonMoveLeft=Button(32,418,"     <    ")
ButtonMoveRight=Button(68,418,"    >     ")

alphaList=[ButtonMoveLeft,ButtonMoveRight]



ButtonsMaps=[ButtonMap0,ButtonMap1,ButtonMap2,ButtonMap3,ButtonMap4,ButtonMap5,ButtonMap6,ButtonMap7,ButtonMap8,ButtonMap9,ButtonMap10,ButtonMap11,ButtonMap12,ButtonMap13,ButtonMap14,ButtonMap15,ButtonMap16,ButtonMap17,ButtonMap18,ButtonMap19,ButtonMap20,ButtonMap21,ButtonMap22,ButtonMap23,ButtonMap24,ButtonMap25,ButtonMap26,ButtonMap27,ButtonMap28,ButtonMap29]#,ButtonMap7,ButtonMap8,ButtonMap9]

TurnNumbers=[Turn1,Turn2,Turn3,Turn4,Turn5,Turn6,Turn7,Turn8,Turn9,Turn10,Turn11,Turn12,Turn13,Turn14,Turn15,Turn16,TurnAll]
TurnNumber=" All Turns "

OptionGroup = alphaList+ButtonsMaps+[Button0,Button1,Button2,Button3,Button4,Button5,Button6,Button7,Button8,Button9,Button10,Button11]#+alphaList


screen = pygame.display.set_mode((720+200+290,640),RESIZABLE)#(,570)#,, 750,570
newScreen=pygame.Surface((300,640),pygame.SRCALPHA, 32)

clock = pygame.time.Clock()


Font1 = pygame.font.SysFont(None, 16)
def optionsEnter(group,Font=Font1):
    for item in group:
        if mouse_x >= item.x and mouse_x <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height) and str(item.__class__.__name__)!="Text":# and item.text in [str(currentDirectory),"Current Directory"]:
            bg = (220,220,220)
        elif item.text in ["Exit","[empty folder]","<Back>","Cancel","Save","Del"," Don't Save Changes "]:
            bg = (230,230,230)
        elif item.text in [" Add "]:
            bg = (20,240,20)
        elif item.text in [" Cancel "]:
            bg=(250,20,20)
        else:
            if item.text=="Current Directory":
                bg = (166,84,84)
            else:
                if str(item.text[-4:])==".txt":
                    bg = (180,180,180)
                else:
                    bg = (220,206,167)

        pygame.draw.rect(screen,bg,(item.x,item.y,item.width,item.height))
 
        pygame.draw.rect(screen,(0,0,0),(item.x,item.y,item.width,item.height),1)

        useFont=Font
        addX,addY=(0,0)
        
        Text = useFont.render(item.text, 1, (0,10,10))

        if item.text in [' Add ', ' Cancel ']:
            useX=item.x

        screen.blit(Text, (useX,item.y+4))



def printToTxtFile():
    mapWidth=len(array[0])
    mapHeight=len(array)

    tempArray=[]
    for row in range(mapHeight):
        temp=[]
        for column in range(mapWidth):
            addAtEnd=True
            for item in OptionGroupTileB:
                need3=array[row][column]
                try:
                    if str(item.name)==str(need3[2]):#
                        temp.append((item.name,array[row][column][1]))
                        addAtEnd=False
                        break
                except IndexError:
                    addAtEnd=True
                
            if addAtEnd is True: #failed for tile, still save something tho
                temp.append(("redTileFinalTry5.png",0))
        
        tempArray.append(temp)

    print('fn: ',filename)
    createFile=open(base+"_ALLMAPS/"+str(filename)+"/MAP.txt", "w")

    for jj in range(mapHeight):

        theLine=tempArray[jj]
        addd=""
        if jj+1!=mapHeight:
            addd="\n"
        createFile.write(str(theLine)+addd)
    createFile.close()


def backupToTxtFile():#usefilename=filename):
    mapWidth=len(array[0])
    mapHeight=len(array)

    adjtempArray=[]
    for row in range(mapHeight):
        temp=[]
        for column in range(mapWidth):
            addAtEnd=True
            for item in OptionGroupTileB:
                need3=array[row][column]
                try:
                    if str(item.name)==str(need3[2]):#
                        temp.append((item.name,array[row][column][1]))
                        addAtEnd=False
                        break
                except IndexError:
                    addAtEnd=True
                
            if addAtEnd is True: #failed, still save something tho
                temp.append(("redTileFinalTry5.png",0))
        
        adjtempArray.append(temp)

    createFile=open(base+"_ALLMAPS/BACKUP_SAVE/MAP.txt", "w")

    for jj in range(mapHeight):
        theLine=adjtempArray[jj]
        addd=""
        if jj+1!=mapHeight:
            addd="\n"
        createFile.write(str(theLine)+addd)
    createFile.close()
    



newWin1=['ROUT','SEIZE','ESCAPE','PROTECT','KILL','SURVIVE']

chooseWhenEnter=[]
onlyOneOption=[]

def options(group,screen=screen):
    for item in group:
        if screen==newScreen:
            addBonus=920
        else:
            addBonus=0

        TurnNumbersCheck=reset._callEnemyUnitsSpawnTurns

            
        if mouse_x-addBonus >= item.x and mouse_x-addBonus <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
            bg=(176,80,80)
        elif item.text in ["Friendly",' NEW ']:
            if Friendly is True or item.text == "Friendly":
                bg=(50,50,220)
            else:
                bg=(206,29,29)
        elif item.text in ["Add new enemy or neutral player to recruit"]:#Add New Recruiter'
            bg=(208,200,76)
        elif item.text[0:17] in ['Add New Recruiter']:
            bg=(75,150,75)
        elif item.text[0:4] in ['Open'] and VILLAGES is True:
            #print 'open'
            bg=(26,141,122)
        elif item.text[0:4] in ['Open'] and RECRUITABLE is True:
            #print 'open'
            bg=(185,185,185)
        elif item.text in [' Add new armory ',' Add new vendor ',' Add new weapon chest ',' Add new item chest ',' Add new weapon village ',' Add new item village ']:
            bg=(20,175,175)
        elif item.text[0:8] in [' Delete '," DEL "]:#,' Delete village / house ']:
            bg=(220,50,50)
        elif item.text[0:13] in [" New item for"," New weapon f"]:
            bg=(45,180,45)
        elif group==chooseWhenEnter:
            
            if mouse_x-addBonus >= item.x and mouse_x-addBonus <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                print(item.text,'here for whatever reason')
                bg=(176,80,80)
            elif item.text==" "+str(showEnemy.whenenter[0])+" ":
                bg=(71,162,125)
            elif str(item.text)==" "+str(showEnemy.whenenter[1])+" ":#check this
                bg=(71,162,125)
            else:
                bg = (195,195,195)
        
        elif item.text==str(TurnNumber):
            bg=(255,230,98)
            
        elif str(item.text) in TurnNumbersCheck:
            bg=(125,125,125)
        
            
        elif item.text in ["Enemy",' DEL  ']:
            bg=(220,50,50)
        elif item.text in ['Show Units','Show Water']:
            bg=(35,180,153)
        elif item.text=='Save & Close':
            bg=(73,150,57)
        elif item.text in ['Delete']:
            bg=(150,150,150)
        elif item.text[0:14] in ['Remove Recruit']:#'Remove Recruiter']:
            bg=(142,33,33)
        elif item.text in newWin1:
            bg=(86,208,222)
        elif item.text in ["     <    ","    >     "]:
            bg=(0,215,200)
        else:
            bg = (195,195,195)

            if item.text in alll:
                try:
                    if item.text==clickedRightSide:
                        if showEnemyInfo is False:
                            bg=(100,100,100)
                except:
                    pass

        if group==onlyOneOption:
            if mouse_x-addBonus >= item.x and mouse_x-addBonus <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                bg=(176,80,80)
            elif item.text==" Water " and reset._WATERORLAVA=="Water":
                bg=(22,243,240)
            elif item.text==" Lava " and reset._WATERORLAVA=="Lava":
                bg=(213,142,35)
            elif str(item.text)[-6:]=="convo ":
                bg=(240,240,240)
            elif str(item.text)[:5]==" MAP_":
                if str(item.text)[5]=="1" and reset.convo_map_1_type[0]!='Ellipse': #(" Open 1_convo ") (" MAP_1 ") (" COLOR_1 ")
                    bg=(0,200,40)
                if str(item.text)[5]=="2" and reset.convo_map_2_type[0]!='Ellipse':
                    bg=(0,200,40)
                if str(item.text)[5]=="4" and reset.convo_map_4_type[0]!='Ellipse':
                    bg=(0,200,40)
            elif str(item.text)[:7]==" COLOR_":
                if str(item.text)[7]=="1" and reset.convo_map_1_type[0]=='Ellipse': #(" Open 1_convo ") (" MAP_1 ") (" COLOR_1 ")
                    bg=(0,200,40)
                if str(item.text)[7]=="2" and reset.convo_map_2_type[0]=='Ellipse':
                    bg=(0,200,40)
                if str(item.text)[7]=="4" and reset.convo_map_4_type[0]=='Ellipse':
                    bg=(0,200,40)
                    
            elif str(item.text)[:12]==" Cycle Color":#g,b,r for ellipse 0,1,2
                def returnRGBColor(nummber):
                    if str(nummber)=="0":
                        return (40,240,40)
                    elif str(nummber)=="1":
                        return (40,40,240)
                    elif str(nummber)=="2":
                        return (240,40,40)
                    
                if str(item.text)[12]=="1":
                    bg=returnRGBColor(reset.convo_map_1_type[1])
                    #print 'called at one'
                elif str(item.text)[12]=="2":
                    bg=returnRGBColor(reset.convo_map_2_type[1])
                    #print 'called at two'
                elif str(item.text)[12]=="4":
                    bg=returnRGBColor(reset.convo_map_4_type[1])
                    #print 'called at three'
                else:
                    bg=(0,0,0)
                    print(str(item.text), 'why failed here?')
            elif str(item.text)[:11]==" Update MAP":
                bg=(255,191,110)
            else:
                bg=(195,195,195)
        try:
            if group==newArmories:
                if item.text[0:2]==" x" or item.text[0:4] in [" New"," DEL"," Del"," Add"] or item.text[3:len(item.text)]==" Choose new location " or item.text[4:12] in ["is a sec","is not a"]:
                    pass
                else:
                    bg=(120,120,120)
                    
        except NameError:
            pass

        try: #yes, these 'trys' need to be separate
            if group==newVendors:
                if item.text[0:2]==" x" or item.text[0:4] in [" New"," DEL"," Del"," Add"] or item.text[3:len(item.text)]==" Choose new location " or item.text[4:12] in ["is a sec","is not a"]:
                    pass
                else:
                    bg=(120,120,120)
        except NameError:
            pass


        if showEnemyInfo is True:#
            if item.text==showEnemy.text:
                bg=(0,230,255)
        try:
            if item.text[-1]=="_":
                item.width=20
        except IndexError:
            pass
        
        if (item.text,editMap) == ("Edit Map",True) or (item.text,editUnits) == ("Edit Units",True):
            pygame.draw.rect(screen,(80,190,70),(item.x-1,item.y-1,item.width+2,item.height+2),3)
            bg=(80,120,70)

            
        if Enemy is True:
            if item in enemyPos:
                if item.empty==["False"]:
                    pygame.draw.rect(screen,(255,190,70),(item.x-1,item.y-1,item.width+2,item.height+2),3)
        if Friendly is True:
            if item in friendlyPos:
                if item.text==saveClick:
                    pygame.draw.rect(screen,(255,190,70),(item.x-1,item.y-1,item.width+2,item.height+2),3)

        numbersonlyW=0
        numbersonlyH=0
        if DISPLAY_OPTIONS is True and DISPLAY_LIST==NumOneThruThirty:
            numbersonlyW+=10
            numbersonlyH+=10

        pygame.draw.rect(screen,bg,(item.x-(numbersonlyW/2),item.y-(numbersonlyW/2),item.width+numbersonlyW,item.height+numbersonlyH))

        if editMap is True and item.text=="Edit Units":
            pygame.draw.rect(screen,(40,120,50),(item.x,item.y,item.width,item.height),1)
        elif editUnits is True and item.text=="Edit Map":
            pygame.draw.rect(screen,(40,120,50),(item.x,item.y,item.width,item.height),1)
        
        if item.text not in ["Edit Map","Edit Units"]:# DISPLAY_OPTIONS is False:#latter removes the border for WINCONDITIONS SURVIVE
            if DISPLAY_OPTIONS is True and DISPLAY_LIST==NumOneThruThirty:
                pass
            else:
                pygame.draw.rect(screen,(0,0,0),(item.x,item.y,item.width,item.height),1)

        if (item.text,Friendly)==("Friendly",True) or (item.text,Enemy)==("Enemy",True):
            pygame.draw.rect(screen,(235,140,50),(item.x-1,item.y-1,item.width+2,item.height+2),3)
        
        if item.text in newWin1:
            if item.text==TOWIN:
                pygame.draw.rect(screen,(230,230,100),(item.x-1,item.y-1,item.width+2,item.height+2),3)

        
        useFont=Font
        addX,addY=(0,0)
        if item.width==12:
            useFont=FontSmaller

            #useFont.size(item.text)
            addX,addY=(useFont.size(item.text)[0]/2,useFont.size(item.text)[1]/2)
            addY-=2
            addX-=6
            #addX-=2
        if item.width==20:
            addX,addY=(useFont.size(item.text)[0]/2,useFont.size(item.text)[1]/2)
            addY-=5
            addX-=10
        elif str(item.text[:4]) in [" LVL"," PRE"," Tes"]:
            useFont=FontSmaller2

        if DISPLAY_OPTIONS is True and DISPLAY_LIST==NumOneThruThirty:
            useFont=pygame.font.SysFont(None,20)

        
        #drop the numbers
        if item.text[0:17] in ['Add New Recruiter']:
            Text = useFont.render('Add New Recruiter', 1, (0,10,10))
        elif item.text[0:16] == 'Remove Recruiter':
            Text = useFont.render('Remove Recruiter', 1, (0,10,10))
        elif item.text[0:14] == 'Remove Recruit':
            Text = useFont.render('Remove Recruit', 1, (0,10,10))
        else:
            Text = useFont.render(item.text, 1, (0,10,10))

            
        if DISPLAY_OPTIONS is False and DISPLAY_LIST==NumOneThruThirty:#everything else
            screen.blit(Text, (item.x-addX,item.y+addY+4))
        else:
            width,height=useFont.size(item.text)
            screen.blit(Text, (item.x-addX,item.y+addY+2))

        if item.text in newWin1:
            if item.text==reset._WINCONDITIONS[0] and reset._WINCONDITIONS!="ROUT":
                if item.text in ["SEIZE","ESCAPE"]:
                    text("  "+str(reset._WINCONDITIONS[1])+", "+ str(reset._WINCONDITIONS[2])+"  ",item.x-addX+item.width+10,item.y+addY,screen,Font)
                elif item.text in ["PROTECT"]:
                    text("  "+str(reset._WINCONDITIONS[1])+"  ",item.x-addX+item.width+10,item.y+addY,screen,Font)
                elif item.text in ["KILL"]:
                    text("  "+str(reset._WINCONDITIONS[1])+" , "+str(reset._killWho)+"  ",item.x-addX+item.width+10,item.y+addY,screen,Font)
                elif item.text in ["SURVIVE"]:
                    text("  "+str(reset._WINCONDITIONS[1])+" Turns  ",item.x-addX+item.width+10,item.y+addY,screen,Font)

        elif item.text=="CHAPTER INFO":
            try:
                if clickedRightSide=="CHAPTER INFO":
                    pass
            except NameError:
                pass


chooseNewLocation=False
chooseNewLocationWasJustTrue=False

displayChapterName=False


alll=['CHAPTER INFO','WINCONDITIONS','RECRUITABLE','ARMORY','VENDOR','CHESTS','VILLAGES']

def resetRightSide(): #lmao why did I do it this way
    RECRUITABLE=False
    ARMORY=False
    VENDOR=False
    CHESTS=False
    VILLAGES=False
    CHAPTERNAME=False
    WINCONDITIONS=False
    showEnemyInfo=False
    displayChapterName=False
    
    print('resetrightside')
    
    return RECRUITABLE,ARMORY,VENDOR,CHESTS,VILLAGES,CHAPTERNAME,WINCONDITIONS,showEnemyInfo,displayChapterName


RECRUITABLE,ARMORY,VENDOR,CHESTS,VILLAGES,CHAPTERNAME,WINCONDITIONS,showEnemyInfo,displayChapterName=resetRightSide()



rightSide=[]
adds=0
addsy=0
for i in range(len(alll)):
    item=alll[i]
    if i ==0:
        adds=0
        addsy=0
    else:
        adds+=Font.size(alll[i-1])[0]+4

    if i>2:
        addsy=25
    if i==3:
        adds=0
        
    rightSide.append(Button(5+adds,7+addsy,item))


def text(text,x,y,screen=screen,Font=Font):
    text = text
    size = Font.size(text)
        
    width,height = (size[0],size[1]+10)
    bg = (51,130,200)

    if text in ["Potential Recruit: ","Who can recruit them: "]:
        bg=(8,163,148)
    elif text in ["Recruiters: "]:#,"Who can recruit them: "]:
        bg=(78,163,148)
    elif text[0:9]=='Chest at:' or text[0:19]=='Village / house at:' or text=='Loot: ':
        bg=(150,150,150)

    pygame.draw.rect(screen,bg,(x,y,width,height))
    pygame.draw.rect(screen,(0,0,0),(x,y,width,height),1)
    
    Text = Font.render(text, 1, (0,10,10))
    screen.blit(Text, (x,y+5))

def text2(text,x,y):
    Font2 = pygame.font.SysFont(None, 12)
    text = text
    size = Font2.size(text)
        
    width,height = (size[0],size[1])
    bg = (0,100,200)

    pygame.draw.rect(screen,bg,(x,y,width,height))

            
    Text = Font2.render(text, 1, (0,10,10))
    screen.blit(Text, (x,y))

def text4(text,x,y):
    FontPNG = pygame.font.SysFont(None, 12)
    text = text
    size = FontPNG.size(text)

    width,height = (size[0],size[1]+2)
    bg = (200,200,200)

    pygame.draw.rect(screen,bg,(x,y,width,height))
    pygame.draw.rect(screen,(30,30,30),(x-1,y-1,width+2,height+2),1)
            
    Text = FontPNG.render(text, 1, (0,10,10))
    screen.blit(Text, (x,y+1))


class image_button:
    def __init__(self,img,x,y,chosen):
        self.img=img[0]
        self.name=img[1]

        self.width,self.height=(tilesize,tilesize)
        self.x,self.y=(x,y)
        
        self.chosen=chosen


def returnActualName():
    for person in allClasses:
        if person.name==str(item.text):
            USE=person.actualName
            return USE
        

def checkMagicType(oneWeaponType,enemyClass,magicName):
    if oneWeaponType!="Magic":
        return None
    else:
        if enemyClass in ['Mage2','BattleMage2']:
            for magicWpn in elementalMagic:
                if magicName==magicWpn.name:
                    toReturn=True
                    break
                else:
                    toReturn=False

        elif enemyClass in ['Shaman2','ArchShaman2','Druid2','Necromancer2']:
            for magicWpn in darkMagic:
                if magicName==magicWpn.name:
                    toReturn=True
                    break
                else:
                    toReturn=False

        elif enemyClass in ['BattlePriest2','WhiteMage2','Priest2']:
            for magicWpn in lightMagic:
                if magicName==magicWpn.name:
                    toReturn=True
                    break
                else:
                    toReturn=False
            
            return toReturn


def returnNext(file_location):
    newLIST=os.listdir(file_location)
    SORT=[]
    for item in newLIST:
        SORT.append(int(item[:-5]))
    SORT=sorted(SORT)

    if SORT[0]!=1:
        indx=1
    else:
        indx=2
        while True:
            try:
                if SORT[indx-1]==indx:
                    indx+=1
                else:
                    print(indx,"stop here?")
                    break
            except IndexError:
                if len(SORT)==1:
                    if SORT[0]!=1:
                        indx=1
                    else:
                        indx=2
                print(indx,"stop here2?")
                break

    return indx


#why in the hell did I ever do it this way?? clean this up eventually
armory='armory1.png'
vendor='vendor1.png'

new1='grass_1.png'
new2='grass_2.png'
new3='grass_3.png'
new4='grass_4.png'
new5='grass_5.png'
new6='grass_6.png'
new13='grass_13.png'
new14='grass_14.png'
new15='grass_15.png'
new16='grass_16.png'
new17='grass_17.png'
new18='grass_18.png'
new19='grass_19.png'
new20='grass_20.png'
new21='grass_21.png'
new22='grass_22.png'

new40='grass_40.png'
new41='grass_41.png'
new42='grass_42.png'
new43='grass_43.png'
new44='grass_44.png'

new50='grass_50.png'
new53='grass_53.png'
new55='grass_55.png'

#dark below
new23='grass_23.png'
new24='grass_24.png'
new25='grass_25.png'
new26='grass_26.png'
new27='grass_27.png'
new28='grass_28.png'
new29='grass_29.png'
new30='grass_30.png'
new31='grass_31.png'
new32='grass_32.png'

new34='grass_34.png'
new35='grass_35.png'
new36='grass_36.png'
new37='grass_37.png'
new38='grass_38.png'
new39='grass_39.png'

new51='grass_51.png'
new52='grass_52.png'
new54='grass_54.png'

#sand
new7='grass_7.png'
new8='grass_8.png'
new9='grass_9.png'
new10='grass_10.png'
new11='grass_11.png'
new12='grass_12.png'
new45='grass_45.png'
new46='grass_46.png'
new47='grass_47.png'
new48='grass_48.png'
new49='grass_49.png'

sand1='sand_1.png'
sand2='sand_2.png'
sand3='sand_3.png'
sand4='sand_4.png'

boat1='boat1.png'
boat2='boat2.png'
boat3='boat3.png'

test6='save_tileset2.png'
test4='testcurrent.png'
test5='test45.png'
test3="test3.png"
dirttest="dirttest.png"
dirttest2="dirttest2.png"
dirttest3="dirttest3.png"
dirttest4="dirttest4.png"
dirttest5="dirttest5.png"
dirttest6="dirttest6.png"
dirttest7="dirttest7.png"

test_a="ground_tiles.png"
test_b="ground_tiles2.png"
LAVA2="LAVA2.png"

#this section is all the old, non-moving water bg parts
water00="water0.png"
water01="water1.png"
water02="water2.png"
water03="water3.png"
water04="water4.png"
water05="water5.png"
water06="water6.png"
water07="water7.png"
water08="water8.png"
water08a="water8a.png"
water09="water9.png"
water09a="water9a.png"

waters_1=["water4.png"]


river1='river1.png'
river8='river1b.png'
river2='river2a.png'
river9='river2b.png'
river3='river3a.png'
river10='river3b.png'
river4='river4a.png'
river11='river4b.png'
river12='river5a.png'
river5='river5b.png'
river6='river6a.png'
river13='river6b.png'
river7='river7a.png'
river14='river7b.png'

waters_2=['river1.png','river1b.png']+[str("river"+str(i)+"a.png") for i in range(2,8)]+[str("river"+str(i)+"b.png") for i in range(1,8)]
print(waters_2)

water0="tile water1.png"
water1="tile water2.png"
water2="tile water3.png"
water3="tile water4.png"
water4="tile water5.png"
water5="tile water6.png"
water6="tile water7.png"
water7="tile water8.png"
water8="tile bridge.png"
water9="tile docks1.png"
water10="tile docks2.png"
water11="tile docks3.png"
water12="tile docks4.png"
water13="tile docks5.png"

waters_3=[]
#waters_3=['river1.png','river1b.png']+[str("river"+str(i)+"a.png") for i in range(2,8)]+[str("river"+str(i)+"b.png") for i in range(1,8)]


waters_4=['docks_b.png','docks_c.png']

grass0="grass0.png"
grass1="grass1.png"
grass2="grass2.png"
grass3="grass3.png"
grass4="grass4.png"
grass5="grass5.png"
grass6="grass6.png"
grass7="grass7.png"
grass8="grass8.png"

carpet0="tile carpet1.png"
carpet1="tile carpet2.png"
carpet2="tile carpet3.png"
carpet3="tile throne.png"
carpet4="tile carpet4.png"

carpet0b="tile carpetblue.png"
carpet1b="tile carpet2blue.png"
carpet2b="tile carpet3blue.png"
carpet3b="tile throneblue.png"
carpet4b="tile carpet4blue.png"

carpet0p="tile carpetp.png"
carpet1p="tile carpet2p.png"
carpet2p="tile carpet3p.png"
carpet3p="tile thronep.png"
carpet4p="tile carpet4p.png"

castle0="roof_half1.png"
castle1="roof_half2.png"
castle2="roof_half2a.png"
castle3="roof_half3.png"
castle4="roof_half4.png"
castle5="roof_half5.png"
castle6="roof_half6.png"
castle7="roof_half7.png"
castle8="roof_half8.png"
castle9="roof_half9.png"
castle10="roof_half10.png"
castle10a="roof_half10a.png"
castle11="roof_half11.png"
castle12="wall_1.png"
castle13="wall_2.png"
castle14="wall_3.png"
castle15="wall_4.png"
castle17="tile roof.png"
castle18="tile floor.png"

tan0="roof_half1tan.png"
tan1="roof_half2tan.png"
tan2="roof_half2atan.png"
tan3="roof_half3tan.png"
tan4="roof_half4tan.png"
tan5="roof_half5tan.png"
tan6="roof_half6tan.png"
tan7="roof_half7tan.png"
tan8="roof_half8tan.png"
tan9="roof_half9tan.png"
tan10="roof_half10tan.png"
tan11="roof_half11tan.png"
tan12="wall_1tan.png"
tan13="wall_2tan.png"
tan14="wall_3tan.png"
tan15="wall_4tan.png"
tan16="tile wall.png"
tan18="tile floortan.png"

other1='save_tileset.png'
other2="tile cobblestone2.png"

door0="tile door2.png"
door1="tile door3.png"
door2="tile door2_b.png"
door3="tile door3_b.png"

chest1='chest1.png'
chest2='chest2.png'
chest3='chest1b.png'
chest4='chest2b.png'
chest5='chest1r.png'
chest6='chest2r.png'
chest7='chest1p.png'
chest8='chest2p.png'

##################################################################

stairs01='stairsBC.png'
stairs02='stairsCD.png'
stairs03='stairsEF.png'
stairs04='stairsBCtan.png'
stairs05='stairsCDtan.png'
stairs06='stairsEFtan.png'

stairs0="tile stairs1.png"
stairs1="tile stairs2.png"
stairs2="tile stairs3.png"
stairs3="tile stairs4.png"
stairs4="tile stairs5.png"
stairs8="tile stairs6.png"
stairs9="tile stairs7.png"
stairs10="tile stairs8.png"
stairs11="tile stairs9.png"
stairs12="tile stairs.png"
stairs13="tile stairs down.png"
stairs14="tile stairs down2.png"

pillarA1="pillar_a.png"
pillarA2 ="pillar column.png"
pillarA3 ="pillar column2.png"
pillarB1="pillarB1.png"
pillarB2 ="pillarB2.png"
pillarB3 ="pillarB3.png"
pillarC1="pillarC1.png"
pillarC2 ="pillarC2.png"
pillarC3 ="pillarC3.png"
pillarD1="pillarD1.png"
pillarD2 ="pillarD2.png"
pillarD3 ="pillarD3.png"

house0="house30.png"
house1="tile housewall1.png"
house2="tile housewall2.png"
house3="tile housewall3.png"
house4="tile housewall4.png"
house5="tile housewall5.png"
house6="tile housewall5a.png"
house7="tile housewall6.png"
house8="tile housewall7.png"
house0b="house30b.png"
house1b="tile housewall1b.png"
house2b="tile housewall2b.png"
house3b="tile housewall3b.png"
house4b="tile housewall4b.png"
house5b="tile housewall5b.png"
house6b="tile housewall5ab.png"
house7b="tile housewall6b.png"
house8b="tile housewall7b.png"

hill1='hill1.png'
hill2='hill2.png'
hill1b='hill1b.png'
hill2b='hill2b.png'
hill3='hill3.png'
hill4='hill4.png'

tree0="tree0.png"
#other00="blackk.png"

boat1a="boat1a.png"
boat1b="boat1b.png"
boat2a="boat2a.png"
boat2b="boat2b.png"
boat3a="boat3a.png"
boat3b="boat3b.png"

ground1='dirttest.png'
ground2='dirttest4.png'
ground3='dirttest2.png'
ground4='dirttest3.png'
ground5='dirttest5.png'
ground6='dirttest6.png'
ground7='dirttest7.png'

door_1='door_1.png'
door_2='door_2.png'
door_3='door_3.png'
door_4='door_4.png'
door_5='door_5.png'
door_6='door_6.png'

t34='tesst.png'
t35='tesst2.png'
t36='docks_a.png'
t37='docks_b.png'
t38='docks_c.png'
t2="hill3.png"

lava1="lava_1.png"
dirt_1a="dirt_1a.png"
dirt_1b="dirt_1b.png"
dirt_2="dirt_2.png"
dirt_3="dirt_3.png"
dirt_4="dirt_4.png"
dirt_5="dirt_5.png"
dirt_6="dirt_6.png"

waters_5=[dirt_4,dirt_5,LAVA2] #lava tiles

pond1='pond1.png'
pond2='pond2.png'
pond3='pond3.png'
pond4='pond4.png'
pond5='pond5.png'
pond6='pond6.png'

tracking1,tracking2=(0,30)
rateWater=0.1

waterIMG=pygame.image.load(base_tiles+'waterTest.png')
lavaIMG=pygame.image.load(base_tiles+'LAVA2.png')



waterAcceptFormer=['sand_1.png','sand_2.png','sand_3.png','sand_4.png','water4.png','grass_14.png','grass_15.png','grass_16.png','grass_21.png','grass_22.png','grass_23.png','grass_24.png','grass_28.png','grass_29.png','grass_30.png','grass_31.png','grass_32.png','grass_33.png','grass_34.png','grass_52.png','grass_53.png','boat1a.png','boat1b.png','boat2a.png','boat2b.png','boat3a.png','boat3b.png','river1.png','river2.png','river3.png','river4.png','river5.png','river6.png','river7.png','river8.png','river9.png','river10.png','river11.png','river12.png','river13.png','river14.png','river7b.png','river7a.png']
waterAccept=waters_1+waters_2+waters_3+waters_4+waters_5

for item in waterAcceptFormer:
    if item not in waterAccept:
        waterAccept.append(item)
        

#these option groups were an old way to sort these, fix it later
OptionGroupTilea=[t34,t35,t36,t37,t38,water04,river1,river2,river3,river4,river5,river6,river7,river8,river9,river10,river11,river12,river13,river14,boat1a,boat1b,boat2a,boat2b,boat3a,boat3b]#,castle11,castle58,castle59,castle60,castle61]#castle8
OptionGroupTileb=[water9,water10,water11,water12,water13]
OptionGroupTilec=[castle0,castle1,castle2,castle3,castle4,castle5,castle6,castle7,castle8,castle9,castle10,castle10a,castle11,castle12,castle13,castle14,castle15]#,castle16,castle17,castle18]
OptionGroupTiled=[stairs01,stairs02,stairs03,stairs04,stairs05,stairs06,stairs0,stairs13,stairs14,pillarA1,pillarA2,pillarA3,pillarB1,pillarB2,pillarB3,pillarC1,pillarC2,pillarC3,pillarD1,pillarD2,pillarD3]
OptionGroupTilee=[other2,carpet0,carpet1,carpet2,carpet3,carpet4,carpet0b,carpet1b,carpet2b,carpet3b,carpet4b,carpet0p,carpet1p,carpet2p,carpet3p,carpet4p]#,chest0,chest1,tree0]
OptionGroupTilef=[new1,new2,new3,new5,new13,new14,new15,new16,new17,new18,new19,new20,new21,new22,new31,new40,new41,new42,new43,new44,new50,new53,new55]
OptionGroupTileg=[new1,new2,new3,new6,new23,new24,new25,new26,new27,new28,new29,new30,new32,new34,new35,new36,new37,new38,new39,new51,new52,new54]
OptionGroupTileh=[new7,new8,new9,new10,new11,new12,new45,new46,new47,new48,new49,sand1,sand2,sand3,sand4]
OptionGroupTilei=[]#mon1,mon2]
OptionGroupTilej=[ground1,ground2,ground3,ground4,ground5,ground6,ground7,door0,door2,door_1,door_2,door_3,door_4,door_5,door_6]
OptionGroupTilek=[tan0,tan1,tan2,tan3,tan4,tan5,tan6,tan7,tan8,tan9,tan10,tan11,tan12,tan13,tan14,tan15,tan16,tan18]#tan10a
OptionGroupTilel=[hill1,hill2,hill1b,hill2b,hill3,hill4,house0,house1,house2,house3,house4,house5,house6,house7,house8,house0b,house1b,house2b,house3b,house4b,house5b,house6b,house7b,house8b]
OptionGroupTilem=[chest1,chest2,chest3,chest4,chest5,chest6,chest7,chest8,armory,vendor]
OptionGroupTilen=["blue30x30.png"]
OptionGroupTileo=[pond1,pond2,pond3,pond4,pond5,pond6]
OptionGroupTilep=[dirt_2,dirt_3,dirt_4,dirt_5,dirt_6]

revisedOptionGroup=OptionGroupTilea+OptionGroupTileb+OptionGroupTilec+OptionGroupTiled+OptionGroupTilee+OptionGroupTilef+OptionGroupTileg+OptionGroupTileh+OptionGroupTilei+OptionGroupTilej+OptionGroupTilek+OptionGroupTilel+OptionGroupTilem+OptionGroupTilen+OptionGroupTileo+OptionGroupTilep

print("Tileset total:", len(revisedOptionGroup))


bah_x=2
bah_y=3

#this list is ALL tiles in their button / image form
#DO NOT CONFUSE WITH OptionGroupTile (MISSING 'B')

#below isn't used anymore, look down a dozen or so lines
OptionGroupTileB=[]
for i in range(len(revisedOptionGroup)):#wait edit this too??
    item=revisedOptionGroup[i]
    try:
        TILE=image_button((pygame.image.load(base_tiles+str(item)),str(item)),bah_x,bah_y,False) #x / y locations menaingless here fyi
    except IOError:
        print('missing4: '+base_tiles+str(item))
        sys.exit()
    OptionGroupTileB.append(TILE)
    bah_x+=32
    if bah_x > 90:
        bah_y += 32
        bah_x=2


OptionGroupTile=[]

bah_x=2
bah_y=3

#if tiles per screen is 30, that means:

print('len(revisedOptionGroup): ',len(revisedOptionGroup))
max_track_tiles=int(math.ceil(float(len(revisedOptionGroup)) / float(30)))


track_tiles_index=0
for i in range(30):#column=3,row=10

    item=revisedOptionGroup[i] #grab first few here

    TILE=image_button((pygame.image.load(base_tiles+str(item)),str(item)),bah_x,bah_y,False)
    OptionGroupTile.append(TILE)

    bah_x+=32
    if bah_x > 90:
        bah_y += 32
        bah_x=2


identifyAZ=5


editMap=True
editUnits=False

Friendly=False
Enemy=True


editWho=[Button(16,580,"Friendly"),Button(16,610,"Enemy")]
chooseMapOrUnits=[Button(790,580,"Edit Map"),Button(790,610,"Edit Units"),Button(850,580,"Show Units"),Button(850,610,"Show Water")]


tellClick=False
saveClick="---"

showEnemyInfo=False
showEnemy=None

    
#x by 32, y by 34  
blue_tile=image_button((blue,0),66,3,False)

chosenTile=(blue,0,"other2.png")


mouseMove=True
mouseEdit=False
fullScreen=False

showUnits=True
entered_text=""
entering=False

posneg=4
modAlpha=0

posneg2=4
modAlpha2=0

posneg3=4
modAlpha3=0


WaterOn=True

backupSAVE=0



while True:

    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if entering is True:
                if event.key == K_BACKSPACE:
                    if len(entered_text) >= 1:
                        entered_text = entered_text[:-1]
                if str(pygame.key.name(event.key)) in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z","A","B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z","&","0","1","2","3","4","5","6","7","8","9",",",".","-"]:#,"_","*","#","@","(",")","[","]","+","=","?","!"]:
                    if pygame.key.name(event.key)=="space":
                        add_THIS=" "
                    elif pygame.key.get_pressed()[K_LSHIFT]:
                        add_THIS=pygame.key.name(event.key).upper() #surprisingly no errors trying this on special characters or numbers
                    else: #this is for normal lowercase letters
                        add_THIS=str(pygame.key.name(event.key))
                    entered_text+=add_THIS

                print("BAH: "+str(pygame.key.name(event.key)))

                        
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key==K_f and pygame.key.get_pressed()[K_LCTRL]:

                if fullScreen is False:
                    fullScreen=True

                    infoObject = pygame.display.Info()
                    screen = pygame.display.set_mode((720+200+290,640),FULLSCREEN,RESIZABLE)#(infoObject.current_w, infoObject.current_h),
                else:
                    fullScreen=False
                    screen = pygame.display.set_mode((720+200+290,640),RESIZABLE)#720+200+200,640


        elif event.type == MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()

            def filtered(name):
                end=""
                for letter in name:
                    if letter.isalpha():
                        end+=letter.upper()
                    else:
                        end+=letter
                return end

            if entering is True:
                for item in saveCancel:
                    if mouse_x >= item.x and mouse_x <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                        
                        if item.text==' Add ':
                            if enteringText=="Enter Name of Enemy:":

                                to_edit=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','r').read().split('\n')
                                to_edit[0]=str(entered_text)#only edit the name here
                                
                                to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','w')

                                for _j in range(len(to_edit)):
                                    jj=to_edit[_j]
                                    addd=""
                                    if _j+1!=len(to_edit):
                                        addd="\n"
                                    to_edit2.write(str(jj)+addd)
                                
                                to_edit2.close()

                            if enteringText=="Enter Name of Chapter:":

                                to_edit=open(base+"_ALLMAPS/"+str(filename)+'/EXTRA.txt','r').read().split('\n')
                                to_edit[1]=str(entered_text)
                                to_edit[2]="irrelevant now"
                                
                                to_edit2=open(base+"_ALLMAPS/"+str(filename)+'/EXTRA.txt','w')

                                for _j in range(len(to_edit)):
                                    jj=to_edit[_j]
                                    addd=""
                                    if _j+1!=len(to_edit):
                                        addd="\n"
                                    to_edit2.write(str(jj)+addd)
                                
                                to_edit2.close()



                            entered_text=""

                            
                            reset(filename)

                            array=reset.array
                            temparray=reset.temparray
                            mapWidth=reset.mapWidth
                            mapHeight=reset.mapheight
                            friendlyPos=reset.friendlyPos
                            enemyPos=reset.enemyPos

                            entering=False
                            chooseNewLocationWasJustTrue=True

                            try:
                                for item in enemyPos:
                                    if item.text==saveNum:
                                        showEnemy=item
                                        break

                            except NameError: #all good bro, if it's an error it aint meant to be
                                pass

                        elif item.text==' Cancel ':
                            entering=False
                            
                            
            if DISPLAY_OPTIONS is True:

                for item in displayedOptions:
                    if mouse_x >= item.x and mouse_x <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):

                        if DISPLAY_LIST==factionList:

                            to_edit=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','r').read().split('\n')
                            to_edit[2]=str(item.text)
                            
                            to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','w')
                            for _j in range(len(to_edit)):
                                jj=to_edit[_j]
                                addd=""
                                if _j+1!=len(to_edit):
                                    addd="\n"
                                to_edit2.write(str(jj)+addd)
                            
                            to_edit2.close()

                        elif DISPLAY_LIST==allClasses:

                            to_edit=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','r').read().split('\n')
                            for person in allClasses:
                                if person.actualName==str(item.text):#.actualName used to be .name, just go with it here
                                    useName=person.actualName
                                    break
                    
                            to_edit[1]=str(useName)                            
                            to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','w')

                            for _j in range(len(to_edit)):
                                jj=to_edit[_j]
                                addd=""
                                if _j+1!=len(to_edit):
                                    addd="\n"
                                to_edit2.write(str(jj)+addd)
                            
                            to_edit2.close()
                            
                        elif DISPLAY_LIST==ALL_WEAPONS and CHESTS is False and VILLAGES is False and ARMORY is False and VENDOR is False: #if ARMORY is True

                            to_edit=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','r').read().split('\n')
                            for person in allClasses:
                                if person.name==str(item.text):
                                    useName=person.actualName
                                    break
                    
                            to_edit[5]=str(item.text[3:])
                            #this here
                            
                            to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','w')
                            for _j in range(len(to_edit)):
                                jj=to_edit[_j]
                                addd=""
                                if _j+1!=len(to_edit):
                                    addd="\n"
                                to_edit2.write(str(jj)+addd)
                            
                            to_edit2.close()


                        elif DISPLAY_LIST==ALL_ALLIES and WINCONDITIONS is True:
                            print('()',filename)
                            to_edit=[str(TOWIN),str(item.text)]
                            to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/WINCONDITIONS.txt",'w')
                            for _j in range(len(to_edit)):
                                jj=to_edit[_j]
                                addd=""
                                if _j+1!=len(to_edit):
                                    addd="\n"
                                to_edit2.write(str(jj)+addd)
                            
                            to_edit2.close()


                        elif DISPLAY_LIST==ALL_ALLIES and RECRUITABLE is True:
                            print('>--<')
                            print(RecruitInfo[0][0:16])
                            print(RecruitInfo[0])
                            print(RecruitInfo)

                            if RecruitInfo[0][0:17]=="Add New Recruiter":#,str(item.text[-1])]#

                                useThisName=item.text

                                k=int(RecruitInfo[1])
                                print('called1')


                                allRecruitsRightNow=reset._RECRUITABLE


                                useK=k+1

                                def write_to(whichfile,whichlist):
                                    
                                    to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/RECRUITABLE/"+str(whichfile),'w')
                                    for _j in range(len(whichlist)):
                                        print('line')
                                        jj=whichlist[_j]
                                        addd=""
                                        if _j+1!=len(whichlist):
                                            addd="\n"
                                        to_edit2.write(str(jj)+addd)
                                    
                                    to_edit2.close()

                                writeNamesList=allRecruitsRightNow[k][1]
                                writeNamesList.insert(0,allRecruitsRightNow[k][0])
                                writeNamesList.append(useThisName)

                                write_to(str(useK)+"_.txt",writeNamesList)
                                print('called2')
                                    
                                reset(currentFile) #only this line requireed because only reset._ values are used


                        elif DISPLAY_LIST==reset.ALL_ENEMIES_IN_PLAY and WINCONDITIONS is True:
                            print('()',filename)
                            to_edit=[str(TOWIN),str(item.text)]
                            to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/WINCONDITIONS.txt",'w')
                            for _j in range(len(to_edit)):
                                jj=to_edit[_j]
                                addd=""
                                if _j+1!=len(to_edit):
                                    addd="\n"
                                to_edit2.write(str(jj)+addd)
                            
                            to_edit2.close()



                        elif DISPLAY_LIST==reset.ALL_ENEMIES_IN_PLAY and RECRUITABLE is True:

                            print('>--<',RecruitInfo[0]=="Add new enemy or neutral player to recruit")

                            if RecruitInfo[0]=="Add new enemy or neutral player to recruit":#,str(item.text[-1])]#

                                confirmNotExisting=True
                                for blah in reset._RECRUITABLE:
                                    if blah[0]==item.text:#recruit already exists
                                        confirmNotExisting=False

                                if confirmNotExisting is True:

                                    guyToRecruit=str(item.text)
                                    defaultRecruiter="Caedus"

                                    default_1=[guyToRecruit,defaultRecruiter]
                                    default_convo=[": Line1.",guyToRecruit+": okay i will join.",": and end line."]


                                    newFileNames=str((len(reset._RECRUITABLE))+1)


                                    def write_to(whichfile,whichlist):
                                        
                                        to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/RECRUITABLE/"+str(whichfile),'w')
                                        for _j in range(len(whichlist)):
                                            print('line')
                                            jj=whichlist[_j]
                                            addd=""
                                            if _j+1!=len(whichlist):
                                                addd="\n"
                                            to_edit2.write(str(jj)+addd)
                                        
                                        to_edit2.close()


                                    write_to(str(newFileNames)+"_.txt",default_1)
                                    write_to(str(newFileNames)+"_convo.txt",default_convo)
                                        
                                    reset(currentFile) #only this line required because only reset._ values are used
                                

                        elif DISPLAY_LIST==NumOneThruThirty: #SURVIVE
                            if ARMORY is True:

                                armoryLines=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/ARMORY/'+str(armoryToEdit)+'.txt',"r").read().split('\n')
                                print(armoryLines)
                                for linesIn in armoryLines:
                                    print(linesIn,len(getName))
                                    if linesIn[0:len(getName)]==getName:
                                        saveIndex=armoryLines.index(linesIn)
                                        break

                                armoryLines[saveIndex]=str(getName)+":"+str(item.text)
                                print(armoryLines)

                                modArmory=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/ARMORY/'+str(armoryToEdit)+'.txt',"w")

                                for j in range(len(armoryLines)):
                                    if j!=len(armoryLines)-1:
                                        addTo="\n"
                                    else:
                                        addTo=""
                                    modArmory.writelines(str(armoryLines[j])+addTo)
                                    
                                modArmory.close()
                                

                            elif VENDOR is True:
                                vendorLines=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VENDOR/'+str(vendorToEdit)+'.txt',"r").read().split('\n')
                                print(vendorLines)
                                for linesIn in vendorLines:
                                    print(linesIn,len(getName))
                                    if linesIn[0:len(getName)]==getName:
                                        saveIndex=vendorLines.index(linesIn)
                                        break

                                vendorLines[saveIndex]=str(getName)+":"+str(item.text)
                                print(vendorLines)

                                modVendor=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VENDOR/'+str(vendorToEdit)+'.txt',"w")

                                for j in range(len(vendorLines)):
                                    if j!=len(vendorLines)-1:
                                        addTo="\n"
                                    else:
                                        addTo=""
                                    modVendor.writelines(str(vendorLines[j])+addTo)
                                    
                                modVendor.close()
                                

                            else:
                                print('()',filename)
                                to_edit=[str(TOWIN),str(item.text)]
                                to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/WINCONDITIONS.txt",'w')
                                for _j in range(len(to_edit)):
                                    jj=to_edit[_j]
                                    addd=""
                                    if _j+1!=len(to_edit):
                                        addd="\n"
                                    to_edit2.write(str(jj)+addd)
                                
                                to_edit2.close()
                                

                        elif DISPLAY_LIST==ALL_ITEMS or DISPLAY_LIST==ALL_WEAPONS: #for chest or village works here

                            useThisNameInstead=''
                            if DISPLAY_LIST==ALL_ITEMS:
                                useThisNameInstead=str(item.text)
                            elif DISPLAY_LIST==ALL_WEAPONS:
                                useThisNameInstead=item.text[3:]#erases C-- (class name with two dashes)
                                
                            if CHESTS is True:                                

                                toWrite=["Closed",str(chestNewPos[0]),str(chestNewPos[1]),str(useThisNameInstead)]

                                startZero=0
                                while os.path.exists(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/CHEST/'+str(startZero)+'_.txt'):
                                    startZero+=1

                                writeFile=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/CHEST/'+str(startZero)+'_.txt',"w")
                                for items in toWrite:
                                    writeFile.writelines(items+'\n')
                                writeFile.close()
                                

                            elif VILLAGES is True:

                                toWrite=["NOTVISITED",str(villageNewPos[0]),str(villageNewPos[1]),str(useThisNameInstead),"Villager: NOT USING THIS LINE - BUT KEEP TO LOAD CORRECTLY.","Villager: Sample conversation text.","Villager: Here, take some money as a reward for xyz.",": Um, thanks. Bye."]

                                startZero=0
                                while os.path.exists(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VILLAGE/'+str(startZero)+'_.txt'):
                                    startZero+=1

                                writeFile=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VILLAGE/'+str(startZero)+'_.txt',"w")                                
                                for items in toWrite:
                                    writeFile.writelines(items+'\n')
                                writeFile.close()

                            elif ARMORY is True:
                                modArmory=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/ARMORY/'+str(whichOne)+'_.txt',"a")
                                modArmory.writelines("\n"+str(useThisNameInstead)+":15")
                                modArmory.close()

                                reset(filename)
                                

                            elif VENDOR is True:
                                modVendor=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VENDOR/'+str(whichOne)+'_.txt',"a")
                                modVendor.writelines("\n"+str(useThisNameInstead)+":15")  
                                modVendor.close()

                                reset(filename)
                            
                            else:
                                print("then something is wrong, I shouldn't be getting here")
                                sys.exit()
                            

                        printToTxtFile()

                        reset(filename)

                        array=reset.array
                        temparray=reset.temparray
                        mapWidth=reset.mapWidth
                        mapHeight=reset.mapheight
                        friendlyPos=reset.friendlyPos
                        enemyPos=reset.enemyPos

                        print('calling reset')

                        try:

                            for item in enemyPos:
                                if item.text==saveNum:
                                    showEnemy=item
                                    break
                        except NameError: #all good bro, if it's an error it aint meant to be
                            pass
                        
                        DISPLAY_OPTIONS=False
                                                

            else:
                if chooseNewLocation is True:
                    if pygame.mouse.get_pressed()[0]:

                        mouse_x,mouse_y = pygame.mouse.get_pos()
                        xx = int(mouse_x-110)
                        yy = int(mouse_y)
                        while float(float(xx)/tilesize) != int(float(xx)/tilesize):
                            xx -= 1
                        at_x = int(xx)/tilesize
                        while float(float(yy)/tilesize) != int(float(yy)/tilesize):
                            yy -= 1
                        at_y = int(yy)/tilesize

                        if float(at_x) >= 0 and float(at_x)<25 and float(at_y) >= 0 and float(at_y)<19:

                            if WINCONDITIONS is True: #

                                print('()',filename)
                                to_edit=[str(TOWIN),int(at_x+array_addx),int(at_y+array_addy)]#,"NotSecret"]
                                to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/WINCONDITIONS.txt",'w')
                                for _j in range(len(to_edit)):
                                    jj=to_edit[_j]
                                    addd=""
                                    if _j+1!=len(to_edit):
                                        addd="\n"
                                    to_edit2.write(str(jj)+addd)
                                
                                to_edit2.close()


                            elif CHESTS is True:

                                chooseNewLocation=False
                                chestNewPos=[int(at_x+array_addx),int(at_y+array_addy)]
                                DISPLAY_OPTIONS=True

                                if chestChoice==' Add new weapon chest ':
                                    DISPLAY_LIST=ALL_WEAPONS
                                elif chestChoice==' Add new item chest ':
                                    DISPLAY_LIST=ALL_ITEMS
                                
                            elif VILLAGES is True:

                                chooseNewLocation=False
                                villageNewPos=[int(at_x+array_addx),int(at_y+array_addy)]
                                DISPLAY_OPTIONS=True
                                
                                if villageChoice==' Add new weapon village ':
                                    DISPLAY_LIST=ALL_WEAPONS
                                elif villageChoice==' Add new item village ':
                                    DISPLAY_LIST=ALL_ITEMS


                            elif ARMORY is True:

                                chooseNewLocation=False

                                if locationArmoryType=="New":

                                    startZero=1
                                    while os.path.exists(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/ARMORY/'+str(startZero)+'_.txt'):
                                        startZero+=1

                                    newFileLines=[str(int(at_x+array_addx))+"\n",str(int(at_y+array_addy))+"\n","NotSecret\n","Iron lance:15"]
                                    freshArmory=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/ARMORY/'+str(startZero)+'_.txt',"w")
                                    freshArmory.writelines(newFileLines)
                                    freshArmory.close()

                                    
                                elif locationArmoryType[0:6]=="Change":
                                    
                                    newPosForArmory=(int(at_x+array_addx),int(at_y+array_addy))
                                    whichArmory=locationArmoryType[6]

                                    print('whichArmory: ', whichArmory)
                                    armoryLines=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/ARMORY/'+str(whichArmory)+'_.txt',"r").read().split('\n')
                                    print(armoryLines)

                                    armoryLines[0]=newPosForArmory[0]
                                    armoryLines[1]=newPosForArmory[1]
                                

                                    modArmory=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/ARMORY/'+str(whichArmory)+'_.txt',"w")

                                    for j in range(len(armoryLines)):
                                        if j!=len(armoryLines)-1:
                                            addTo="\n"
                                        else:
                                            addTo=""
                                        modArmory.writelines(str(armoryLines[j])+addTo)
                                        
                                    modArmory.close()
                                    

                            elif VENDOR is True:

                                chooseNewLocation=False


                                if locationVendorType=="New":

                                    startZero=1
                                    while os.path.exists(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VENDOR/'+str(startZero)+'_.txt'):
                                        startZero+=1

                                    newFileLines=[str(int(at_x+array_addx))+"\n",str(int(at_y+array_addy))+"\n","NotSecret\n","Heal:15"]
                                    freshVendor=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VENDOR/'+str(startZero)+'_.txt',"w")
                                    freshVendor.writelines(newFileLines)
                                    freshVendor.close()

                                    
                                elif locationVendorType[0:6]=="Change":
                                    
                                    newPosForVendor=(int(at_x+array_addx),int(at_y+array_addy))
                                    whichVendor=locationVendorType[6]

                                    print('whichArmory: ', whichVendor)
                                    
                                    vendorLines=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VENDOR/'+str(whichVendor)+'_.txt',"r").read().split('\n')

                                    print(vendorLines)

                                    vendorLines[0]=newPosForVendor[0]
                                    vendorLines[1]=newPosForVendor[1]
                                    
                                    modVendor=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VENDOR/'+str(whichVendor)+'_.txt',"w")

                                    for j in range(len(vendorLines)):
                                        if j!=len(vendorLines)-1:
                                            addTo="\n"
                                        else:
                                            addTo=""
                                        modVendor.writelines(str(vendorLines[j])+addTo)
                                        
                                    modVendor.close()

                                
                            else: #choose location for people on map

                                to_edit=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','r').read().split('\n')
                                for person in allClasses:
                                    if person.name==str(showEnemy.main[0]):
                                        useName=person.actualName
                                        break

                                showEnemyPos=[int(at_x+array_addx),int(at_y+array_addy)]
                        
                                to_edit[6]=int(at_x+array_addx)
                                to_edit[7]=int(at_y+array_addy)

                                print(to_edit)
                                
                                to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','w')
                                for _j in range(len(to_edit)):
                                    jj=to_edit[_j]
                                    addd=""
                                    if _j+1!=len(to_edit):
                                        addd="\n"
                                    to_edit2.write(str(jj)+addd)
                                
                                to_edit2.close()

                            
                            chooseNewLocation=False
                            chooseNewLocationWasJustTrue=True

                            printToTxtFile()

                            reset(filename)

                            array=reset.array
                            temparray=reset.temparray
                            mapWidth=reset.mapWidth
                            mapHeight=reset.mapheight
                            friendlyPos=reset.friendlyPos
                            enemyPos=reset.enemyPos

                            try:
                                for item in enemyPos:
                                    if item.text==saveNum:
                                        showEnemy=item
                                        break

                            except NameError:
                                pass

                    
                elif chooseNewLocation is False:
                    if showEnemyInfo is True and Enemy is True:

                        for item in chooseWhenEnter:
                            if mouse_x-920 >= item.x and mouse_x-920 <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                                adjustME=item.text[:-1]
                                adjustME=adjustME[1:]
                                print(adjustME)

                                jjj=[]

                                if adjustME in [str(o) for o in range(0,17)]: #line 1
                                    jjj=[adjustME+"\n",showEnemy.whenenter[1]]
                                elif adjustME in ['N','S','E','W','NA']:
                                    jjj=[showEnemy.whenenter[0]+"\n",adjustME]
                                else:
                                    #exit error - this needs fixing
                                    print("hooboy, this aint good. fix it.")
                                    sys.exit()

                                to_edit=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_whenenter.txt','w')
                                for j in jjj:
                                    to_edit.writelines(j)
                                to_edit.close()

                                reset(filename)

                                #reset
                                array=reset.array
                                temparray=reset.temparray
                                mapWidth=reset.mapWidth
                                mapHeight=reset.mapheight
                                friendlyPos=reset.friendlyPos
                                enemyPos=reset.enemyPos

                                try:
                                    for item in enemyPos:
                                        if item.text==saveNum:
                                            showEnemy=item
                                            break

                                except NameError: #all good bro, if it's an error it aint meant to be
                                    pass         

                        
                        for item in enemyMoveChoices:
                            if mouse_x-920 >= item.x and mouse_x-920 <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):

                                groupedAll=showEnemy.main[9:len(showEnemy.main)]
                                if item.text not in groupedAll:
                                    groupedAll.append(item.text)
                                elif item.text in groupedAll:
                                    if item.text!=showEnemy.text:
                                        groupedAll.remove(item.text)

                                to_edit=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','r').read().split('\n')
                                for person in allClasses:
                                    if person.name==str(item.text):
                                        useName=person.actualName
                                        break


                                groupedAll1=showEnemy.main[:9]#:len(showEnemy.main)]
                                for eh in groupedAll:
                                    if "False"==open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+eh+'/empty.txt','r').read().split('\n')[0]:                                        
                                        groupedAll1.append(eh)

                                
                                to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','w')
                                for _j in range(len(groupedAll1)):
                                    jj=groupedAll1[_j]
                                    addd=""
                                    if _j+1!=len(groupedAll1):
                                        addd="\n"
                                    to_edit2.write(str(jj)+addd)
                                
                                to_edit2.close()

                                printToTxtFile()

                                reset(filename)

                                array=reset.array
                                temparray=reset.temparray
                                mapWidth=reset.mapWidth
                                mapHeight=reset.mapheight
                                friendlyPos=reset.friendlyPos
                                enemyPos=reset.enemyPos

                                for item in enemyPos:
                                    if item.text==saveNum:
                                        showEnemy=item
                                        break
                                    
                                
                        for item in enemyChoices:
                            if mouse_x-920 >= item.x and mouse_x-920 <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                                if item.text=='Choose Faction':
                                    
                                    DISPLAY_OPTIONS=True
                                    DISPLAY_LIST=factionList

                                elif item.text=='Enter Name':
                                    entering=True
                                    enteringText="Enter Name of Enemy:"

                                elif item.text=='Make Class as Name':
                                    to_edit=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','r').read().split('\n')
                                    for person in allClasses:
                                        if person.name==str(item.text):
                                            useName=person.actualName
                                            break

                                    for y in range(1,59):
                                        print('..',str(sheet.cell_value(y,0)),str(to_edit[1]))
                                        if str(sheet.cell_value(y,0))==str(to_edit[1]):
                                            useClassName=str(sheet.cell_value(y,1))
                                            break
                                        
                                    to_edit[0]=useClassName                                    
                                    to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','w')

                                    for _j in range(len(to_edit)):
                                        jj=to_edit[_j]
                                        addd=""
                                        if _j+1!=len(to_edit):
                                            addd="\n"
                                        to_edit2.write(str(jj)+addd)
                                    
                                    to_edit2.close()
                                    
                                    
                                elif item.text=='Choose Weapon':
                                    DISPLAY_OPTIONS=True
                                    DISPLAY_LIST=ALL_WEAPONS

                                elif item.text=='Choose Class':
                                    DISPLAY_OPTIONS=True
                                    DISPLAY_LIST=allClasses
                                    
                                elif item.text in ['True','False','None']:
                                    to_edit=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','r').read().split('\n')
                                    for person in allClasses:
                                        if person.name==str(item.text):
                                            useName=person.actualName
                                            break
                            
                                    to_edit[8]=str(item.text)
                                    to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','w')

                                    for _j in range(len(to_edit)):
                                        jj=to_edit[_j]
                                        addd=""
                                        if _j+1!=len(to_edit):
                                            addd="\n"
                                        to_edit2.write(str(jj)+addd)
                                    
                                    to_edit2.close()

                                    
                                elif item.text=='Choose Location':
                                    chooseNewLocation=True

                                elif item.text=='Toggle Empty':
                                    if showEnemy.empty[0]=="False":
                                        printSave="True"
                                    else:
                                        printSave="False"

                                        
                                    to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/empty.txt','w')
                                    to_edit2.write(printSave)
                                    to_edit2.close()
                                        

                                elif item.text[0]=="-" and item.text[-1]=="-":

                                    new_level=item.text[1:]
                                    new_level=int(new_level[:-1])#3,4 lines

                                
                                    to_edit=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','r').read().split('\n')
                                    for person in allClasses:
                                        if person.name==str(item.text):
                                            useName=person.actualName
                                            break
                            

                                    to_edit[3]=str(new_level)
                                    to_edit[4]="0"
                                    #this here
                                    
                                    to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+showEnemy.text+'/1_.txt','w')
                                    for _j in range(len(to_edit)):
                                        jj=to_edit[_j]
                                        addd=""
                                        if _j+1!=len(to_edit):
                                            addd="\n"
                                        to_edit2.write(str(jj)+addd)
                                    
                                    to_edit2.close()


                                printToTxtFile()

                                reset(filename)

                                array=reset.array
                                temparray=reset.temparray
                                mapWidth=reset.mapWidth
                                mapHeight=reset.mapheight
                                friendlyPos=reset.friendlyPos
                                enemyPos=reset.enemyPos


                                for item in enemyPos:
                                    if item.text==saveNum:
                                        showEnemy=item
                                        break

                                    
                        
                    if CHESTS is True:
                        for item in newChests:
                            if mouse_x-920 >= item.x and mouse_x-920 <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                                if item.text[0:14]==' Delete Chest ':

                                    toDeleteNum=item.text[-7]
                                    os.remove(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/CHEST/'+str(toDeleteNum)+'_.txt')
                                    reset(currentFile)

                                elif item.text in [' Add new weapon chest ',' Add new item chest ']:
                                    showEnemy=enemyPos[0] #to avoid errors
                                    chooseNewLocation=True

                                chestChoice=item.text


                    if ARMORY is True:
                        
                        for item in newArmories:
                            if mouse_x-920 >= item.x and mouse_x-920 <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                                print(item.text[4:12])
                                if item.text[0:1]==" x":
                                    pass
                                elif item.text[4:12] in ["is a sec","is not a"]: #secret / not secret

                                    changeWhichOne=str(item.text[1:3])

                                    print(changeWhichOne)
                                    readSecret=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/ARMORY/'+str(changeWhichOne)+'.txt').read().split('\n')

                                    
                                    if item.text[4:12]=="is a sec":
                                        readSecret[2]="NotSecret"
                                    elif item.text[4:12]=="is not a":
                                        readSecret[2]="Secret"
                                    else:
                                        print('da hell?')
                                        sys.exit()

                                    print('readSecret',readSecret)


                                    changeSecret=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/ARMORY/'+str(changeWhichOne)+'.txt',"w")

                                    for j in range(len(readSecret)):
                                        if j!=len(readSecret)-1:
                                            addTo="\n"
                                        else:
                                            addTo=""
                                        changeSecret.writelines(str(readSecret[j])+addTo)
                                            
                                    changeSecret.close()
                                    reset(currentFile)
                                    
                                    
                                elif item.text[0:7]==" Delete":
                                    deleteWhichOne=str(item.text[-3])+str(item.text[-2])

                                    os.remove(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/ARMORY/'+str(deleteWhichOne)+'.txt')                                    
                                    reset(currentFile)


                                elif item.text==" Add new armory ":

                                    chooseNewLocation=True
                                    locationArmoryType="New"


                                elif item.text[3:]==" Choose new location ":

                                    chooseNewLocation=True
                                    locationArmoryType="Change"+str(item.text[1])

                                elif item.text==" DEL ":

                                    for aButton in newArmories:
                                        if item.text!=aButton.text and item.y==aButton.y and aButton.text[1]!="x":
                                            print("[]",aButton.text)

                                            armoryToEdit=aButton.text[1]+aButton.text[2]
                                            print('armoryToEdit: ',armoryToEdit)

                                            getIndex=aButton.text.find(":")
                                            getName=aButton.text[4:getIndex]

                                            print('getName: ',getName)

                                            armoryLines=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/ARMORY/'+str(armoryToEdit)+'.txt',"r").read().split('\n')
                                            print(armoryLines)
                                            for linesIn in armoryLines:
                                                print(linesIn,len(getName))
                                                if linesIn[0:len(getName)]==getName:
                                                    deleteIndex=armoryLines.index(linesIn)
                                                    break

                                            armoryLines.pop(deleteIndex)
                                            print(armoryLines)

                                            modArmory=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/ARMORY/'+str(armoryToEdit)+'.txt',"w")

                                            for j in range(len(armoryLines)):
                                                if j!=len(armoryLines)-1:
                                                    addTo="\n"
                                                else:
                                                    addTo=""
                                                modArmory.writelines(str(armoryLines[j])+addTo)
                                                
                                            modArmory.close()
                                            
                                            break
                                        
                                    reset(filename)

                                elif item.text[0:14]==" New item for ":

                                    showEnemy=enemyPos[0] #NEED this otherwise breaks stuff

                                    whichOne=item.text[14]
                                    print('whichOne: ',whichOne)

                                    DISPLAY_OPTIONS=True
                                    DISPLAY_LIST=ALL_ITEMS


                                elif item.text[0:16]==" New weapon for ":

                                    showEnemy=enemyPos[0] #NEED this otherwise breaks stuff

                                    whichOne=item.text[16]
                                    print('whichOne: ',whichOne)

                                    DISPLAY_OPTIONS=True
                                    DISPLAY_LIST=ALL_WEAPONS



                                elif item.text[1]=="x": #means count for that item
                                    
                                    for aButton in newArmories:
                                        if item.text!=aButton.text and item.y==aButton.y and aButton.text!=" DEL ":

                                            #show number selections
                                            DISPLAY_LIST=NumOneThruThirty
                                            DISPLAY_OPTIONS=True
                                            
                                            print("[]",aButton.text)

                                            armoryToEdit=aButton.text[1]+aButton.text[2]
                                            print('armoryToEdit: ',armoryToEdit)

                                            getIndex=aButton.text.find(":")
                                            getName=aButton.text[4:getIndex]

                                            print('getName: ',getName)
                                            
                                            break
                                        

                    if VENDOR is True:
                        for item in newVendors:
                            if mouse_x-920 >= item.x and mouse_x-920 <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                                if item.text[0:1]==" x":
                                    pass #for now
                                elif item.text[4:12] in ["is a sec","is not a"]: #secret / not secret

                                    changeWhichOne=str(item.text[1:3])

                                    print(changeWhichOne)
                                    readSecret=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VENDOR/'+str(changeWhichOne)+'.txt').read().split('\n')

                                    
                                    if item.text[4:12]=="is a sec":
                                        readSecret[2]="NotSecret"
                                    elif item.text[4:12]=="is not a":
                                        readSecret[2]="Secret"
                                    else:
                                        print('da hell?')
                                        sys.exit()

                                    print('readSecret',readSecret)

                                    changeSecret=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VENDOR/'+str(changeWhichOne)+'.txt',"w")

                                    for j in range(len(readSecret)):
                                        if j!=len(readSecret)-1:
                                            addTo="\n"
                                        else:
                                            addTo=""
                                        changeSecret.writelines(str(readSecret[j])+addTo)
                                            
                                    changeSecret.close()

                                    reset(currentFile)
                                elif item.text[0:7]==" Delete":
                                    deleteWhichOne=str(item.text[-3])+str(item.text[-2])

                                    os.remove(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VENDOR/'+str(deleteWhichOne)+'.txt')                                    

                                    reset(currentFile)


                                elif item.text==" Add new vendor ":

                                    chooseNewLocation=True
                                    locationVendorType="New"


                                elif item.text[3:]==" Choose new location ":

                                    chooseNewLocation=True
                                    locationVendorType="Change"+str(item.text[1])

                                elif item.text==" DEL ":

                                    for aButton in newVendors:
                                        if item.text!=aButton.text and item.y==aButton.y and aButton.text[1]!="x":
                                            print("[]",aButton.text)

                                            vendorToEdit=aButton.text[1]+aButton.text[2]
                                            print('vendorToEdit: ',vendorToEdit)

                                            getIndex=aButton.text.find(":")
                                            getName=aButton.text[4:getIndex]

                                            print('getName: ',getName)

                                            vendorLines=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VENDOR/'+str(vendorToEdit)+'.txt',"r").read().split('\n')
                                            print(vendorLines)
                                            for linesIn in vendorLines:
                                                print(linesIn,len(getName))
                                                if linesIn[0:len(getName)]==getName:
                                                    deleteIndex=vendorLines.index(linesIn)
                                                    break

                                            vendorLines.pop(deleteIndex)
                                            print(vendorLines)

                                            modVendor=open(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VENDOR/'+str(vendorToEdit)+'.txt',"w")

                                            for j in range(len(vendorLines)):
                                                if j!=len(vendorLines)-1:
                                                    addTo="\n"
                                                else:
                                                    addTo=""
                                                modVendor.writelines(str(vendorLines[j])+addTo)
                                                
                                            modVendor.close()
                                            
                                            break
                                        
                                    reset(filename)

                                elif item.text[0:14]==" New item for ":

                                    showEnemy=enemyPos[0] #NEED this otherwise breaks stuff

                                    whichOne=item.text[14]
                                    print('whichOne: ',whichOne)

                                    DISPLAY_OPTIONS=True
                                    DISPLAY_LIST=ALL_ITEMS


                                elif item.text[0:16]==" New weapon for ":

                                    showEnemy=enemyPos[0] #NEED this otherwise stuff breaks

                                    whichOne=item.text[16]
                                    print('whichOne: ',whichOne)

                                    DISPLAY_OPTIONS=True
                                    DISPLAY_LIST=ALL_WEAPONS



                                elif item.text[1]=="x": #means count for that item
                                    
                                    for aButton in newVendors:
                                        if item.text!=aButton.text and item.y==aButton.y and aButton.text!=" DEL ":

                                            #show number selections
                                            DISPLAY_LIST=NumOneThruThirty
                                            DISPLAY_OPTIONS=True
                                            
                                            print("[]",aButton.text)

                                            vendorToEdit=aButton.text[1]+aButton.text[2]
                                            print('armoryToEdit: ',vendorToEdit)

                                            getIndex=aButton.text.find(":")
                                            getName=aButton.text[4:getIndex]

                                            print('getName: ',getName)
                                            
                                            break

   

                    if VILLAGES is True:
                        for item in newVillages:
                            if mouse_x-920 >= item.x and mouse_x-920 <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                                if item.text[:4]=='Open':
                                    extrapolate=item.text[-6:]
                                    print(extrapolate)

                                    full_command='notepad.exe '+base+'/_ALLMAPS/'+str(filename)+'/LOOT_VILLAGECHEST/VILLAGE/'+str(extrapolate)
                                    os.system(full_command)


                                    
                                elif item.text[0:24]==' Delete village / house ':

                                    toDeleteNum=item.text[-7]

                                    os.remove(base+"_ALLMAPS/"+str(filename)+'/LOOT_VILLAGECHEST/VILLAGE/'+str(toDeleteNum)+'_.txt')

                                    reset(currentFile)

                                elif item.text in [' Add new weapon village ',' Add new item village ']:
                                    
                                    showEnemy=enemyPos[0] #to avoid errors

                                    chooseNewLocation=True
                                    

                                villageChoice=item.text



                    if RECRUITABLE is True:
                        for item in newRecruit:
                            if mouse_x-920 >= item.x and mouse_x-920 <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                                if item.text[:4]=='Open':# TXT':
                                    extrapolate=item.text[-11:]
                                    print(extrapolate)

                                    full_command='notepad.exe '+base+'/_ALLMAPS/'+str(filename)+'/RECRUITABLE/'+str(extrapolate)
                                    os.system(full_command)


                                    
                                elif item.text[0:17]=="Add New Recruiter":

                                    DISPLAY_OPTIONS=True
                                    DISPLAY_LIST=ALL_ALLIES

                                    RecruitInfo=["Add New Recruiter",str(item.text[-1])]
                                    

                                elif item.text=="Add new enemy or neutral player to recruit":
                                    DISPLAY_OPTIONS=True
                                    DISPLAY_LIST=reset.ALL_ENEMIES_IN_PLAY

                                    RecruitInfo=["Add new enemy or neutral player to recruit","99"]


                                elif item.text[0:14]=="Remove Recruit" and item.text[14]!="e" and str(item.text[-1]) in [str(i) for i in range(0,10)]:#
                                    #do the work here and remove, call reset()

                                    fileNumberToCall=int(item.text[-1])

                                    allRecruitsRightNow=reset._RECRUITABLE
                                    allRecruitsRightNow.pop(fileNumberToCall)

                                    deleteAllOfMe=os.listdir(base+"_ALLMAPS/"+str(filename)+'/RECRUITABLE/')
                                    for item in deleteAllOfMe:
                                        os.remove(base+"_ALLMAPS/"+str(filename)+'/RECRUITABLE/'+str(item))


                                    #resave everything with correct numbers
                                    for k in range(len(allRecruitsRightNow)):
                                        useK=k+1

                                        def write_to(whichfile,whichlist):
                                            
                                            to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/RECRUITABLE/"+str(whichfile),'w')
                                            for _j in range(len(whichlist)):
                                                jj=whichlist[_j]
                                                addd=""
                                                if _j+1!=len(whichlist):
                                                    addd="\n"
                                                to_edit2.write(str(jj)+addd)
                                            
                                            to_edit2.close()

                                        writeNamesList=allRecruitsRightNow[k][1]
                                        writeNamesList.insert(0,allRecruitsRightNow[k][0])
                                        print('writeNamesList: ',writeNamesList)
                                        writeConvo=allRecruitsRightNow[k][2]

                                        write_to(str(useK)+"_.txt",writeNamesList)
                                        write_to(str(useK)+"_convo.txt",writeConvo)
                                        
                                    reset(currentFile) #only this line requireed because only reset._ values are used
   

                                elif item.text[0:16]=="Remove Recruiter":# and str(item.text[-1]) in [str(i) for i in range(0,10)]:#

                                    getTHIS=reset._RECRUITABLE[int(item.text[-1])]
                                    if len(getTHIS[1])<=1:
                                        #print '%too few to delete'
                                        pass
                                    else:

                                        print('CALLING HERE')

                                        fileNumberToCall=str(int(item.text[-1])+1)
                                        indexNumberToCall=int(item.text[-1])
                                        recruiterNumberToCall=int(item.text[-2])


                                        updatedList=reset._RECRUITABLE[indexNumberToCall][1]
                                        print(updatedList)
                                        updatedList.pop(recruiterNumberToCall)
                                        print(updatedList)
                                        updatedList.insert(0,reset._RECRUITABLE[indexNumberToCall][0])
                                        print(updatedList)
                               
                                        def write_to(whichfile,whichlist):
                                            
                                            to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/RECRUITABLE/"+str(whichfile),'w')
                                            for _j in range(len(whichlist)):
                                                jj=whichlist[_j]
                                                addd=""
                                                if _j+1!=len(whichlist):
                                                    addd="\n"
                                                to_edit2.write(str(jj)+addd)
                                            
                                            to_edit2.close()

                                        write_to(str(fileNumberToCall)+"_.txt",updatedList)

                                        reset(currentFile)
             

                    #TOWIN
                    elif WINCONDITIONS is True:
                        for item in newWin:
                            if mouse_x-920 >= item.x and mouse_x-920 <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):

                                TOWIN=item.text

                                if item.text in ['SEIZE','ESCAPE']:
                                    chooseNewLocation=True
                                    
                                elif item.text=="ROUT":

                                    to_edit=[str(TOWIN)]
                                    to_edit2=open(base+"_ALLMAPS/"+str(filename)+"/WINCONDITIONS.txt",'w')
                                    for _j in range(len(to_edit)):
                                        jj=to_edit[_j]
                                        addd=""
                                        if _j+1!=len(to_edit):
                                            addd="\n"
                                        to_edit2.write(str(jj)+addd)
                                    
                                    to_edit2.close()


                                    reset(filename)

                                elif item.text in ['PROTECT']:#,'KILL']:
                                    DISPLAY_OPTIONS=True
                                    DISPLAY_LIST=ALL_ALLIES

                                elif item.text in ['KILL']:#,'KILL']:
                                    DISPLAY_OPTIONS=True
                                    DISPLAY_LIST=reset.ALL_ENEMIES_IN_PLAY

                                elif item.text in ['SURVIVE']:
                                    DISPLAY_OPTIONS=True
                                    DISPLAY_LIST=NumOneThruThirty

                                
                        
                    if displayChapterName is True:
                        for item in onlyOneOption:
                            if mouse_x-920 >= item.x and mouse_x-920 <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):

                                def return1or2or4files(numb):
                                    if str(numb)=="1":
                                        return (reset.convo_map_1_type,'/1_conversation_intro/')
                                    elif str(numb)=="2":
                                        return (reset.convo_map_2_type,'/2_conversation_intro2/')
                                    elif str(numb)=="4":
                                        return (reset.convo_map_4_type,'/4_conversation_end1/')
                                        
                                if item.text==reset._CHPNAME:
                                    #displayChapterName
                                    entering=True
                                    enteringText="Enter Name of Chapter:"
                                    
                                elif item.text==" Water ":

                                    getCurrent=open(base+"_ALLMAPS/"+str(filename)+"/EXTRA.txt",'r').read().split('\n')
                                    getCurrent[3]="Water"
                                    amend=open(base+"_ALLMAPS/"+str(filename)+"/EXTRA.txt",'w')
                                    for line in getCurrent:
                                        amend.writelines(line+"\n")
                                    amend.close()
                                    
                                elif item.text==" Lava ":

                                    getCurrent=open(base+"_ALLMAPS/"+str(filename)+"/EXTRA.txt",'r').read().split('\n')
                                    getCurrent[3]="Lava"
                                    amend=open(base+"_ALLMAPS/"+str(filename)+"/EXTRA.txt",'w')
                                    for line in getCurrent:#len=3, index=0,1,2
                                        if getCurrent.index(line)<len(getCurrent)-1:
                                            amend.writelines(line+"\n")
                                        else:
                                            amend.writelines(line)
                                        
                                    amend.close()

                                elif item.text==" Open 1_convo ":
                                    full_command='notepad.exe '+base+'/_ALLMAPS/'+str(filename)+'/1_conversation_intro/_convo.txt'
                                    os.system(full_command)
                                elif item.text==" Open 2_convo ":
                                    full_command='notepad.exe '+base+'/_ALLMAPS/'+str(filename)+'/2_conversation_intro2/_convo.txt'
                                    os.system(full_command)
                                elif item.text==" Open 4_convo ":
                                    full_command='notepad.exe '+base+'/_ALLMAPS/'+str(filename)+'/4_conversation_end1/_convo.txt'
                                    os.system(full_command)
                                    #onlyOneOption.append(Button(15+5+Font.size(" Open 1_convo ")[0]+5+Font.size(" 1_MAP ")[0],146," 1_COLOR "))


                                elif item.text[:5]==" MAP_":
                                    whichFileToEdit=return1or2or4files(item.text[5])[1]
                                    initialThis=return1or2or4files(item.text[5])[0]

                                    if initialThis[0]!='Ellipse':
                                        pass #already a map, skip
                                    else: #currently ellipse, default a copy of current map
                                        readHereOld=open(base+'/_ALLMAPS/'+str(filename)+'/MAP.txt',"r").read().split('\n')
                                        writeHere=open(base+'/_ALLMAPS/'+str(filename)+str(whichFileToEdit)+'MAP_BG.txt',"w")
                                        
                                        for j in range(len(readHereOld)):
                                            if j!=len(readHereOld)-1:
                                                addTo="\n"
                                            else:
                                                addTo=""
                                            writeHere.writelines(str(readHereOld[j])+addTo)

                                        writeHere.close()

                                elif item.text[:7]==" COLOR_":
                                    whichFileToEdit=return1or2or4files(item.text[7])[1]
                                    initialThis=return1or2or4files(item.text[7])[0]

                                    if initialThis[0]=='Ellipse':
                                        pass #already ellipse, pass
                                    else: #currently MAP, default to 'Ellipse' and '1'
                                        #readHereOld=open(base+'/_ALLMAPS/'+str(filename)+'/MAP.txt',"r").read().split('\n')
                                        writeHere=open(base+'/_ALLMAPS/'+str(filename)+str(whichFileToEdit)+'MAP_BG.txt',"w")

                                        writeMe=['Ellipse\n','1']
                                        for this_line in writeMe:
                                            writeHere.writelines(this_line)

                                        writeHere.close()
                                    

                                elif item.text[:11]==" Update MAP":
                                    whichFileToEdit=return1or2or4files(item.text[11])[1]
                                    initialThis=return1or2or4files(item.text[11])[0]

                                    readHereOld=open(base+'/_ALLMAPS/'+str(filename)+'/MAP.txt',"r").read().split('\n')
                                    writeHere=open(base+'/_ALLMAPS/'+str(filename)+str(whichFileToEdit)+'MAP_BG.txt',"w")
                                    
                                    for j in range(len(readHereOld)):
                                        if j!=len(readHereOld)-1:
                                            addTo="\n"
                                        else:
                                            addTo=""
                                        writeHere.writelines(str(readHereOld[j])+addTo)

                                    writeHere.close()


                                elif item.text[:12]==" Cycle Color":

                                    
                                    def returnResetForEllipseOrMap():
                                        pass

                                    whichFileToEdit=return1or2or4files(item.text[12])[1]
                                    initialThis=return1or2or4files(item.text[12])[0]
                                    adjustRGBbg=int(initialThis[1])+1
                                    if adjustRGBbg>2:
                                        adjustRGBbg=0

                                    toWrite=['Ellipse\n',str(adjustRGBbg)]

                                    print('toWrite: ',toWrite)
                                    

                                    writeHere=open(base+'/_ALLMAPS/'+str(filename)+str(whichFileToEdit)+'MAP_BG.txt',"w")
                                    writeHere.writelines(toWrite)
                                    writeHere.close()
                                    

                                reset(currentFile)

        
                                    
                    for item in rightSide:
                        if mouse_x-920 >= item.x and mouse_x-920 <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):

                            RECRUITABLE,ARMORY,VENDOR,CHESTS,VILLAGES,CHAPTERNAME,WINCONDITIONS,showEnemyInfo,displayChapterName=resetRightSide()
                            
                            clickedRightSide=str(item.text)
                            
                            if item.text=="RECRUITABLE":
                                if RECRUITABLE is True:
                                    RECRUITABLE=False
                                else:
                                    RECRUITABLE=True
                            elif item.text=="WINCONDITIONS":
                                if WINCONDITIONS is True:
                                    WINCONDITIONS=False
                                else:
                                    WINCONDITIONS=True

                                    howWin=open(base+"_ALLMAPS/"+str(filename)+'/WINCONDITIONS.txt','r').read().split('\n')
                                    TOWIN=howWin[0]

                                    newWin=[]
                                    
                                    for item1 in newWin1:
                                        newWin.append(Button(5,newWin1.index(item1)*30+80,item1))
                                        
                            elif item.text=="CHAPTER INFO":
                                displayChapterName=True


                            elif item.text=="CHESTS":
                                CHESTS=True

                            elif item.text=="VILLAGES":
                                VILLAGES=True


                            elif item.text=="ARMORY":
                                ARMORY=True

                            elif item.text=="VENDOR":
                                VENDOR=True

                    for item in TurnNumbers:
                        if mouse_x >= item.x and mouse_x <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                            if item.text!=" All Turns ":
                                TurnNumber=int(item.text)
                            else:#da hell?
                                TurnNumber=str(item.text)
                        

                    for item in chooseMapOrUnits:
                        if mouse_x >= item.x and mouse_x <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                            if item.text=="Edit Map":
                                editMap=True
                                editUnits=False
                                mouseEdit=False
                                mouseMove=True
                            elif item.text=="Edit Units":
                                editMap=False
                                editUnits=True
                                mouseEdit=False
                                mouseMove=True
                            elif item.text=='Show Units':
                                if showUnits is True:
                                    showUnits=False
                                else:
                                    showUnits=True
                            elif item.text=='Show Water':
                                if WaterOn is True:
                                    WaterOn=False
                                else:
                                    WaterOn=True


                    if mouseMove is True:
                        if mouse_x >= 110 and mouse_x <= mapWidth*tilesize+110 and mouse_y >= 0 and mouse_y <= mapHeight*tilesize:
                            Moving=True
                            MovingPos=(int(mouse_x),int(mouse_y))
                                

                    if editMap is True:
                        
                        for item in OptionGroup:
                            if mouse_x >= item.x and mouse_x <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                                if item.text == " Quit ":
                                    pygame.quit()
                                    sys.exit()
                                
                                elif item.text == " Save tile map ":
                                    printToTxtFile()#

                                    reset(currentFile)

                                    RECRUITABLE,ARMORY,VENDOR,CHESTS,VILLAGES,CHAPTERNAME,WINCONDITIONS,showEnemyInfo,displayChapterName=resetRightSide()
                                    
                                    array=reset.array
                                    temparray=reset.temparray
                                    mapWidth=reset.mapWidth
                                    mapHeight=reset.mapheight
                                    friendlyPos=reset.friendlyPos
                                    enemyPos=reset.enemyPos
                                    
                                    
                                elif item.text =="Edit":
                                    mouseMove=False
                                    mouseEdit=True

                                elif item.text=="Move":
                                    mouseMove=True
                                    mouseEdit=False

                                elif item.text == " >export image ": #old
                                    print("Not doing this function anymore bud")

                                elif item.text == " Full Backup to Z: ":


                                    #THIS IS NOT WORKING YET - still need to do some research

                                    #conduct full backup to Z: Drive
                                    src=base+'/testbackup/'

                                    dst='\\\\Z:\\BackupFireEmblemSaveFiles\\'

                                    """

                                    import shutil, errno

                                    def copyanything(src, dst):
                                        try:
                                            shutil.copytree(src, dst)
                                        except OSError as exc: # python >2.5
                                            if exc.errno in (errno.ENOTDIR, errno.EINVAL):
                                                shutil.copy(src, dst)
                                            else: raise

                                    #DEWIT=shutil.copytree(fromDir, toDir)
                                    #distutils.dir_util.copy_tree(fromDir, toDir)

                                    """
                                    

                                elif item.text == " Grid on/off ":
                                    if gridStatus is True:
                                        gridStatus = False
                                    else:
                                        gridStatus = True

                                elif item.text=="Rot":
                                    myRotation=chosenTile[1]
                                    myRotation-=90
                                    chosenTile=(pygame.transform.rotate(chosenTile[0],-90),myRotation,chosenTile[2])#.rotate
                                    if float(myRotation)==float(-360):
                                        chosenTile=(chosenTile[0],0,chosenTile[2])
                                        myRotation=0
                                        
                                elif item.text == " Fill map w/ img " and mouseEdit is True:
                                    array=[]
                                    temparray=[]
                                    empty=[]
                                    empty2=[]


                                    for i in range(mapHeight):#
                                        for j in range(mapWidth):
                                            empty.append(chosenTile)
                                            empty2.append((chosenTile[2],chosenTile[1]))
                                            
                                        array.append(empty)
                                        temparray.append(empty2)
                                        empty=[]
                                        empty2=[]
                                        
                                elif item == Button6:#y increase
                                    
                                    mapHeight+=1

                                    myX=[]
                                    myArray=[]
                                    for i in range(mapWidth):
                                        myX.append(("blue30x30.png",0)) #chosenTile=(item.img,0,item.name)
                                        myArray.append((blue,0,"blue30x30.png"))
                                        
                                    temparray.append(myX)
                                    array.append(myArray)

                                elif item == Button5:#x increase
                                    mapWidth+=1

                                    for i in range(mapHeight):
                                        temparray[i].append(("blue30x30.png",0))
                                        array[i].append((blue,0,"blue30x30.png"))
                                    
                                elif item == Button3:#x decrease
                                    if mapWidth >= 5:
                                        mapWidth-=1

                                        for i in range(mapHeight):
                                            temparray[i]=temparray[i][:-1]
                                            array[i]=array[i][:-1]

                                elif item == Button4:#y decrease
                                    if mapHeight >= 5:
                                        mapHeight-=1

                                        array = array[:-1]
                                        temparray = temparray[:-1]
                                elif item in ButtonsMaps:

                                    #print 'here'
                                    for button in ButtonsMaps:

                                        if item.text==button.text:
                                            currentFile=getLevelInfo(item.text)


                                            reset(currentFile)
                                            RECRUITABLE,ARMORY,VENDOR,CHESTS,VILLAGES,CHAPTERNAME,WINCONDITIONS,showEnemyInfo,displayChapterName=resetRightSide()
                                            
                                            array=reset.array
                                            temparray=reset.temparray
                                            mapWidth=reset.mapWidth
                                            mapHeight=reset.mapheight
                                            friendlyPos=reset.friendlyPos
                                            enemyPos=reset.enemyPos
                                            
                                            filename=currentFile


                                            array_addx,array_addy=(0,0)
                                            filename2=str(item.text)
                                            try:
                                                for item in enemyPos:
                                                    if item.text==saveNum:
                                                        showEnemy=item
                                                        break
                                            except NameError:
                                                pass


                                try:

                                    #tracking tile index
                                    #track_tiles_index=0
                                    if item.text in ["     <    ","    >     "]:
                                        if item.text=="     <    ":
                                            if track_tiles_index>=1:
                                                track_tiles_index-=1
                                            else:
                                                track_tiles_index=0

                                        if item.text=="    >     ":
                                            if track_tiles_index<=(max_track_tiles-2):
                                                track_tiles_index+=1
                                            else:
                                                track_tiles_index=max_track_tiles-1

                                        
                                        useIndex=track_tiles_index*30

                                        bah_x=2
                                        bah_y=2
                                        OptionGroupTile=[]
                                        
                                        for i in range(useIndex,useIndex+30):

                                            #print(len(revisedOptionGroup), i, useIndex)
                                            try:
                                                item=revisedOptionGroup[i]
                                                try:
                                                    TILE=image_button((pygame.image.load(base_tiles+str(item)),str(item)),bah_x,bah_y,False)
                                                except IOError:
                                                    print('missing5: '+base_extras+str(item))
                                                    sys.exit()
                                                OptionGroupTile.append(TILE)

                                                bah_x+=32
                                                if bah_x > 90:
                                                    bah_y += 32
                                                    bah_x=2
                                            except IndexError:
                                                pass #ie last page, not enough tiles (30) for one whole page
                                                
                                                    
                                except AttributeError:
                                    pass

                                    
                        for item in OptionGroupTile:
                            addx,addy=(5,82)

                            mouse_xx=mouse_x-addx
                            mouse_yy=mouse_y-addy

                            if mouse_xx >= item.x and mouse_xx <= (item.x+item.width) and mouse_yy >= item.y and mouse_yy <= (item.y+item.height):
                                tempDelete=[]
                                for item2 in OptionGroupTile:
                                    if item2!=item:
                                        tempDelete.append(item2)

                                for item2 in tempDelete:
                                    item2.chosen=False
                                    
                                item.chosen=True
                                chosenTile=(item.img,0,item.name)

                    elif editUnits is True and showUnits is True:
                        if tellClick is True:

                            mouse_x,mouse_y = pygame.mouse.get_pos()
                            xx = int(mouse_x-110)
                            yy = int(mouse_y)
                            while float(float(xx)/tilesize) != int(float(xx)/tilesize):
                                xx -= 1
                            at_x = int(xx)/tilesize
                            while float(float(yy)/tilesize) != int(float(yy)/tilesize):
                                yy -= 1
                            at_y = int(yy)/tilesize

                            at_x+=array_addx
                            at_y+=array_addy

                            if Friendly is True:
                                if mouse_x>=110 and mouse_x<=110+750 and mouse_y>=0 and mouse_y<=570:

                                    #pygame.quit()
                                    #sys.exit()
                                    um2=open(base+"_ALLMAPS/"+str(filename)+"/ALLYSTART/"+saveClick+'.txt','w')
                                    um2.write(str(at_x)+"\n"+str(at_y))

                                    um2.close()

                                    reset(currentFile)
                                    friendlyPos=reset.friendlyPos
                                    
                                    tellClick=False

                            elif Enemy is True:
                                pass #?

                        for item in deleteQ:
                            if mouse_x >= item.x and mouse_x <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                                if Friendly is True:
                                    if item.text==' DEL  ':
                                        path=base+"_ALLMAPS/"+str(filename)+"/ALLYSTART/"+saveClick+'.txt'
                                        os.remove(path)

                                        reset(currentFile)
                                        friendlyPos=reset.friendlyPos
                                        
                                        tellClick=False

                                    elif item.text==' NEW ':
                                        tellClick=True
                
                                        saveClick=str(returnNext(base+"_ALLMAPS/"+str(filename)+"/ALLYSTART/"))+"_"
                                        saveClickPos='new'
                                            
                            
                        for item in editWho:
                            if mouse_x >= item.x and mouse_x <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                                if item.text=="Enemy":
                                    Enemy=True
                                    Friendly=False
                                elif item.text=="Friendly":
                                    Enemy=False
                                    Friendly=True

                                    
                        if Friendly is True:
                            for item in friendlyPos:
                                if mouse_x >= item.x and mouse_x <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):
                                    tellClick=True
                                    saveClick=item.text
                                    saveClickPos=item.save
                        elif Enemy is True:
                            for item in enemyPos:
                                if mouse_x >= item.x and mouse_x <= (item.x+item.width) and mouse_y >= item.y and mouse_y <= (item.y+item.height):

                                    saveNum=item.text

                                    RECRUITABLE,ARMORY,VENDOR,CHESTS,VILLAGES,CHAPTERNAME,WINCONDITIONS,showEnemyInfo,displayChapterName=resetRightSide()

                                    showEnemyInfo=True
                                    showEnemy=item
                                    showEnemyPosOpened=open(base+"_ALLMAPS/"+str(filename)+"/ENEMYSTART/"+item.text+'/1_.txt','r').read().split('\n')
                                    showEnemyPos=[int(showEnemyPosOpened[6]),int(showEnemyPosOpened[7])]

                        
        elif event.type == MOUSEBUTTONUP:
            Moving=False

    if editMap is True:
        if mouseEdit is True and chooseNewLocationWasJustTrue is False:
            if pygame.mouse.get_pressed()[0]:
                try:
                    mouse_x,mouse_y = pygame.mouse.get_pos()
                    xx = int(mouse_x-110)
                    yy = int(mouse_y)
                    while float(float(xx)/tilesize) != int(float(xx)/tilesize):
                        xx -= 1
                    at_x = int(xx)/tilesize
                    while float(float(yy)/tilesize) != int(float(yy)/tilesize):
                        yy -= 1
                    at_y = int(yy)/tilesize

                    if float(at_x) >= 0 and float(at_x)<25 and float(at_y) >= 0 and float(at_y)<19:
                        
                        try:
                            print('change array')
                            array[at_y+array_addy][at_x+array_addx]=chosenTile

                        except IndexError:
                            pass

                except AttributeError:
                    pass
                
    if mouseMove is True:
        
        if Moving is True:

            if mouse_x>110 and mouse_x<110+((25-1)*tilesize) and mouse_y>0 and mouse_y<((19-1)*tilesize):
            
                if abs(abs(mouse_x)-abs(MovingPos[0]))>=5:#change in x
                    if (mouse_x)>(MovingPos[0]) and (array_addx-1)>=0:#this is my addition plus the new 1, plus the num of tiles on screen
                        array_addx-=1
                    elif (mouse_x)<(MovingPos[0]) and (array_addx+1+24)<mapWidth: #move left
                        array_addx+=1
                    MovingPos=(mouse_x,mouse_y)

                if abs(abs(mouse_y)-abs(MovingPos[1]))>=5:#change in y
                    if (mouse_y)>(MovingPos[1]) and (array_addy-1)>=0:#this is my addition plus the new 1, plus the num of tiles on screen
                        array_addy-=1
                    elif (mouse_y)<(MovingPos[1]) and (array_addy+1+19)<=mapHeight: #move left
                        array_addy+=1 
                    MovingPos=(mouse_x,mouse_y)

                
    screen.fill((0,0,0))
    
    pygame.draw.rect(screen,(230,230,230),[0,0,920,640])#(230,230,230))

    s2 = pygame.Surface((750,570),pygame.SRCALPHA, 32)#25,19 // 750,570
    s2 = s2.convert_alpha()
    s2.fill((120,120,120))
    

    mouse_x,mouse_y = pygame.mouse.get_pos()
    xx = int(mouse_x-110)
    yy = int(mouse_y)
    while float(float(xx)/tilesize) != int(float(xx)/tilesize):
        xx -= 1
    at_x = int(xx)/tilesize
    while float(float(yy)/tilesize) != int(float(yy)/tilesize):
        yy -= 1
    at_y = int(yy)/tilesize


    tracking1-=rateWater#0
    tracking2-=rateWater#30 start

    if tracking1<=-30:
        tracking1=30
    if tracking2<=-30:
        tracking2=30
        
    for row in range(mapHeight):
        for column in range(mapWidth):
            try:
                pic=array[row+array_addy][column+array_addx]

                if WaterOn is True and temparray[row+array_addy][column+array_addx][0] in waterAccept:#["grass_2.png"]:#waterAccept:

                    if reset._WATERORLAVA=="Water":
                        useWaterorLava=waterIMG
                    elif reset._WATERORLAVA=="Lava":
                        useWaterorLava=lavaIMG
                        
                    SurfaceW=pygame.Surface((30,30))
                    SurfaceW.blit(useWaterorLava,(int(tracking1),0))
                    SurfaceW.blit(useWaterorLava,(int(tracking2),0))
                    s2.blit(SurfaceW,((column)*tilesize,(row)*tilesize))
                s2.blit(pic[0], (column*tilesize,row*tilesize))
            except IndexError:
                #print 'error with: ',temparray[row+array_addy][column+array_addx]
                pass

    modAlpha+=posneg
    if modAlpha>=220:
        posneg=-6
    elif modAlpha<=14:
        posneg=6

            
    if showUnits is True:
        for item in friendlyPos:
            
            blueT=pygame.Surface((30,30),pygame.SRCALPHA,32)
            blueT.fill((0,0,200,100))
            pygame.draw.rect(blueT,(0,0,200,200),[0,0,30,30],1)
            Text = FontSmaller.render(item.text, 1, (255,255,255))
            blueT.blit(Text, (1,1))#((item.save[0]-array_addx)*tilesize,(item.save[1]-array_addy)*tilesize))

            s2.blit(blueT,((item.save[0]-array_addx)*tilesize,(item.save[1]-array_addy)*tilesize))
        
        
        for item in enemyPos:
            
            if item.empty[0]=="False":

                if item.whenenter[0]==str(TurnNumber) or TurnNumber==" All Turns ":
                    
                    at_pos=(item.main[6],item.main[7])

                    blueT=pygame.Surface((30,30),pygame.SRCALPHA,32)
                    blueT.fill((200,0,0,100))
                    pygame.draw.rect(blueT,(200,0,0),[0,0,30,30],1)

                    s2.blit(blueT,((int(at_pos[0])-array_addx)*tilesize,(int(at_pos[1])-array_addy)*tilesize))

                    s2.blit(item.pic,((int(at_pos[0])-array_addx)*tilesize,(int(at_pos[1])-array_addy)*tilesize))

                    Text = FontSmaller.render(item.text, 1, (255,255,255))
                    s2.blit(Text, ((int(at_pos[0])-array_addx)*tilesize+1,(int(at_pos[1])-array_addy)*tilesize+1))



                    #check for recruitable
                    for possibleRecruit in reset._RECRUITABLE:
                        #print str(possibleRecruit[0]),str(item.main[0])
                        if str(possibleRecruit[0])==str(item.main[0]):
                            s_wtf=pygame.Surface((30,30),pygame.SRCALPHA,32)
                            pygame.draw.rect(s_wtf,(15,15,255,modAlpha),[0,0,30,30])
                            s2.blit(s_wtf,((int(at_pos[0])-array_addx)*tilesize,(int(at_pos[1])-array_addy)*tilesize))
                        
            
    else: #refer to check_A.py file if want to reimplement this
        pass
    
        
    #second conditional is because it was bugging me, leave it there
    if reset._WINCONDITIONS[0] in ["SEIZE","ESCAPE"] and showUnits is True:

        print(reset._WINCONDITIONS)
        #print 'here',modAlpha,posneg
        
        s_wtf=pygame.Surface((30,30),pygame.SRCALPHA,32)
        pygame.draw.rect(s_wtf,(70,180,70,modAlpha),[0,0,mapwidth*tilesize,mapheight*tilesize])
        s2.blit(s_wtf,((int(reset._WINCONDITIONS[1])-array_addx)*tilesize,(int(reset._WINCONDITIONS[2])-array_addy)*tilesize))


    if showUnits is True:
            
        for item in reset._CHESTS:
                        
            s_wtf=pygame.Surface((30,30),pygame.SRCALPHA,32)
            pygame.draw.rect(s_wtf,(255,255,100,modAlpha),[0,0,mapwidth*tilesize,mapheight*tilesize])
            s2.blit(s_wtf,((int(item[0])-array_addx)*tilesize,(int(item[1])-array_addy)*tilesize))

        for item in reset._VILLAGES:
                        
            s_wtf=pygame.Surface((30,30),pygame.SRCALPHA,32)
            pygame.draw.rect(s_wtf,(255,145,51,modAlpha),[0,0,mapwidth*tilesize,mapheight*tilesize])
            s2.blit(s_wtf,((int(item[0])-array_addx)*tilesize,(int(item[1])-array_addy)*tilesize))

        for item in reset._ARMORIES:
                        
            s_wtf=pygame.Surface((30,30),pygame.SRCALPHA,32)
            pygame.draw.rect(s_wtf,(153,51,153,modAlpha),[0,0,mapwidth*tilesize,mapheight*tilesize])
            s2.blit(s_wtf,((int(item[1])-array_addx)*tilesize,(int(item[2])-array_addy)*tilesize))

        for item in reset._VENDORS:
                        
            s_wtf=pygame.Surface((30,30),pygame.SRCALPHA,32)
            pygame.draw.rect(s_wtf,(153,51,153,modAlpha),[0,0,mapwidth*tilesize,mapheight*tilesize])
            s2.blit(s_wtf,((int(item[1])-array_addx)*tilesize,(int(item[2])-array_addy)*tilesize))
            

    if gridStatus is True:
        for i in range(mapWidth+1):
            pygame.draw.line(s2,(0,0,0),(i*tilesize,0),(i*tilesize,mapHeight*tilesize),1)
        for j in range(mapHeight+1):
            pygame.draw.line(s2,(0,0,0),(0,j*tilesize),(mapWidth*tilesize,j*tilesize),1)
            
    if at_x < mapWidth and at_y < mapHeight:
        pygame.draw.rect(s2,(220,0,0),(at_x*tilesize,at_y*tilesize,tilesize,tilesize),2)

        Text = Font.render(str((at_x+array_addx))+","+str((at_y+array_addy)), 1, (0,10,10))
        s2.blit(Text, (at_x*tilesize+2,at_y*tilesize+31))

        
    if tellClick is False or (tellClick,saveClickPos)==(True,'new'):
        if Enemy is True:
            deleteQ=[]
        else:
            deleteQ=[Button(755,581,' NEW ')]
    else:
        if Enemy is True:
            deleteQ=[]
        else:
            deleteQ=[Button(755,581,' NEW '),Button(755,606,' DEL  ')]

    try:#for add position
        if tellClick is True and showUnits is True and Enemy is False and editUnits is True and editMap is False:
            
            yellowT=pygame.Surface((30,30),pygame.SRCALPHA,32)
            yellowT.fill((255,255,0,130))
            pygame.draw.rect(yellowT,(255,255,0),[0,0,30,30],2)
            s2.blit(yellowT,((saveClickPos[0]-array_addx)*tilesize,(saveClickPos[1]-array_addy)*tilesize))
    except TypeError:
        pass
    
    if editUnits is True and Friendly is True:
        options(deleteQ)
    elif editUnits is True and Enemy is True:
        options(deleteQ)

    
    screen.blit(s2,(110,0))

    #bottom part
    pygame.draw.rect(screen,(86,110,160),[5,444,100,60])
    pygame.draw.rect(screen,(0,0,0),[5,444,100,60],1)

    #center
    pygame.draw.rect(screen,(86,110,160),[5,82,100,360])
    pygame.draw.rect(screen,(0,0,0),[5,82,100,360],1)


    for item in OptionGroupTile:
        addx,addy=(5,82) #was 105
        mouse_xx=mouse_x+addx
        mouse_yy=mouse_y+addy

        screen.blit(item.img,(item.x+addx,item.y+addy))

        if item.chosen is False:
            if mouse_x >= item.x+addx and mouse_x <= (item.x+addx+item.width) and mouse_y >= item.y+addy and mouse_y <= (item.y+addy+item.height):
                pygame.draw.rect(screen,(0,0,0),(item.x+addx,item.y+addy,item.width,item.height),1)

        elif item.chosen is True:
            pygame.draw.rect(screen,(255,255,255),(item.x+addx,item.y+addy,item.width,item.height),2)


    pygame.draw.rect(screen,(86,110,160),[5,5,100,74])
    pygame.draw.rect(screen,(0,0,0),[5,5,100,74],1)

    pygame.draw.rect(screen,(86,110,160),[5,507,100,60])
    pygame.draw.rect(screen,(0,0,0),[5,507,100,60],1)


    options(OptionGroup)

    text('   Turn #:   ',861,450)
    options(TurnNumbers)
    
    if mouseEdit is True:
        s5=pygame.Surface((20,18),pygame.SRCALPHA,32)
        pygame.draw.rect(s5,(240,20,20,140),[0,0,20,18])
        screen.blit(s5,(862+1,30+1))
    if mouseMove is True:
        s5=pygame.Surface((27,18),pygame.SRCALPHA,32)
        pygame.draw.rect(s5,(240,20,20,140),[0,0,27,18])
        screen.blit(s5,(888+1,30+1))
    
    for button in ButtonsMaps:
        
        if str(filename2)==str(button.text):
            s5=pygame.Surface((button.width,18),pygame.SRCALPHA,32)
            pygame.draw.rect(s5,(240,20,20,140),[0,0,button.width-2,12])
            screen.blit(s5,(button.x+1,button.y+1))

    useIdentify=int(identifyAZ)
    usePlusY=0

    usePlusY+=21
    useIdentify=-3 #hoping this works out

    text(' '+str(track_tiles_index+1)+'/'+str(max_track_tiles)+' ',8,417)

    s5=pygame.Surface((10,18),pygame.SRCALPHA,32)
    screen.blit(s5,(alphaList[0].x+1+(useIdentify*12),alphaList[0].y+1+usePlusY))
    
    text(str(" X : "+str(mapWidth)+" "),54-Font.size(str(" X : "+str(mapWidth)+" "))[0]/2,511)
    text(str(" Y : " +str(mapHeight)+" "),54-Font.size(str(" X : "+str(mapHeight)+" "))[0]/2,541)
    text(str(" MAP : "),862,3)#Button9 = Button(867,45,"Edit")
    text(str(" Cur Tile : "),862,75)
    text(str(" Work On: "),862,155)#Button9 = Button(867,45,"Edit")
    

    pygame.draw.rect(screen,(0,0,0),[861,100,32,32],1)
    screen.blit(chosenTile[0], (862,101))
    text4(str(chosenTile[2]),862,135)

    pygame.draw.rect(screen,(100,100,100),[70,575,682,60])
    pygame.draw.rect(screen,(0,0,0),[70,575,682,60],1)

    
    options(editWho)
    if Friendly is True:
        yyyyy=580
        options(friendlyPos)
    elif Enemy is True:
        yyyyy=610#580,610
        options(enemyPos)

    screen.blit(arrow,(2,yyyyy))

    pygame.draw.rect(screen,(0,0,0),[0,0,920,570],2)#720+200+200,640

    newScreen=pygame.Surface((290,640),pygame.SRCALPHA, 32)
    newScreen=newScreen.convert_alpha()
    newScreen.fill((40,94,125))#24,68,93))
    pygame.draw.rect(newScreen,(11,38,49),[-2,0,290,638],2)


    if CHESTS is True:

        newChests=[]

        newChests.append(Button(5,75," Add new weapon chest "))
        newChests.append(Button(5+5+Font.size(" Add new weapon chest ")[0],75," Add new item chest "))

        startJ=115
        
        for j in range(len(reset._CHESTS)):#

            _chest_=reset._CHESTS[j]


            text("Chest at: ",5,startJ,newScreen)
            text("X:"+str(_chest_[0])+"  Y:"+str(_chest_[1]),5+5+Font.size("Chest at: ")[0],startJ,newScreen)
            startJ+=30
            text("Loot: ",5,startJ,newScreen)
            text(str(_chest_[2]),5+5+Font.size("Loot: ")[0],startJ,newScreen)
            startJ+=30
            newChests.append(Button(5,startJ,' Delete Chest '+str(reset._CHESTS[j][3])+' '))

            startJ+=40

        options(newChests,newScreen)

    if ARMORY is True:

        newArmories=[]

        newArmories.append(Button(5,75," Add new armory "))

        startJ=110
        for armory in reset._ARMORIES:
            text(" "+str(armory[0])+" Armory at: X:"+str(armory[1])+" Y:"+str(armory[2])+" ",5,startJ,newScreen)
            newArmories.append(Button(5+5+Font.size(" "+str(armory[0])+" Armory at: X:"+str(armory[1])+" Y:"+str(armory[2])+" ")[0],startJ+1," "+str(armory[0])+" Choose new location "))

            startJ+=27

            for i in range(len(armory)-4): #first two=x,y
                getLine=armory[i+4]
                
                text(" Item: ",5,startJ,newScreen)
                newArmories.append(Button(5+5+Font.size(" Item: ")[0],startJ+1," "+str(armory[0])+" "+str(getLine[0])+" "))
                text(" Count: ",5+5+Font.size(" Item: ")[0]+5+Font.size(" "+str(armory[0])+" "+str(getLine[0])+" ")[0],startJ,newScreen)

                newArmories.append(Button(5+5+Font.size(" Item: ")[0]+5+Font.size(str(armory[0])+" "+str(getLine[0]))[0]+5+5+Font.size(" Count: ")[0],startJ+1," x"+str(getLine[1])+" "))


                newArmories.append(Button(5+5+Font.size(" Item: ")[0]+5+Font.size(str(armory[0])+" "+str(getLine[0]))[0]+5+5+Font.size(" Count: ")[0]+Font.size(" x"+str(getLine[1])+" ")[0]+5,startJ+1," DEL "))

                startJ+=21

            startJ+=5

            newArmories.append(Button(5,startJ," New item for "+str(armory[0])+" "))
            newArmories.append(Button(5+5+Font.size(" New item for "+str(armory[0])+" ")[0],startJ," New weapon for "+str(armory[0])+" "))
            startJ+=22
            
            newArmories.append(Button(5,startJ," Delete armory "+str(armory[0])+" "))
            
            if str(armory[3])=="Secret":
                newArmories.append(Button(25+Font.size(" Delete armory ")[0],startJ," "+str(armory[0])+" is a secret shop "))
            elif str(armory[3])=="NotSecret":
                newArmories.append(Button(25+Font.size(" Delete armory ")[0],startJ," "+str(armory[0])+" is not a secret shop "))
            else:
                print('{}',str(armory[2]))
                                   
            startJ+=44


        options(newArmories,newScreen)
        

    elif VENDOR is True:

        newVendors=[]

        newVendors.append(Button(5,75," Add new vendor "))

        startJ=110
        for vendor in reset._VENDORS:
            text(" "+str(vendor[0])+" Vendor at: X:"+str(vendor[1])+" Y:"+str(vendor[2])+" ",5,startJ,newScreen)
            newVendors.append(Button(5+5+Font.size(" "+str(vendor[0])+" Vendor at: X:"+str(vendor[1])+" Y:"+str(vendor[2])+" ")[0],startJ+1," "+str(vendor[0])+" Choose new location "))

            startJ+=27

            for i in range(len(vendor)-4):
                getLine=vendor[i+4]
                text(" Item: ",5,startJ,newScreen)
                newVendors.append(Button(5+5+Font.size(" Item: ")[0],startJ+1," "+str(vendor[0])+" "+str(getLine[0])+" "))
                text(" Count: ",5+5+Font.size(" Item: ")[0]+5+Font.size(" "+str(vendor[0])+" "+str(getLine[0])+" ")[0],startJ,newScreen)
                newVendors.append(Button(5+5+Font.size(" Item: ")[0]+5+Font.size(str(vendor[0])+" "+str(getLine[0]))[0]+5+5+Font.size(" Count: ")[0],startJ+1," x"+str(getLine[1])+" "))

                newVendors.append(Button(5+5+Font.size(" Item: ")[0]+5+Font.size(str(vendor[0])+" "+str(getLine[0]))[0]+5+5+Font.size(" Count: ")[0]+Font.size(" x"+str(getLine[1])+" ")[0]+5,startJ+1," DEL "))

                startJ+=21

            startJ+=5

            newVendors.append(Button(5,startJ," New item for "+str(vendor[0])+" "))
            newVendors.append(Button(5+5+Font.size(" New item for "+str(vendor[0])+" ")[0],startJ," New weapon for "+str(vendor[0])+" "))
            startJ+=27
            
            newVendors.append(Button(5,startJ," Delete vendor "+str(vendor[0])+" "))

            if str(vendor[3])=="Secret":
                newVendors.append(Button(25+Font.size(" Delete vendor ")[0],startJ," "+str(vendor[0])+" is a secret shop "))
            elif str(vendor[3])=="NotSecret":
                newVendors.append(Button(25+Font.size(" Delete vendor ")[0],startJ," "+str(vendor[0])+" is not a secret shop "))
            else:
                print('{}',str(vendor[2]))
                
            startJ+=44
            
        options(newVendors,newScreen)

        
    elif VILLAGES is True:

        newVillages=[]

        newVillages.append(Button(5,75," Add new weapon village "))
        newVillages.append(Button(5+5+Font.size(" Add new weapon village ")[0],75," Add new item village "))

        startJ=115
        
        for j in range(len(reset._VILLAGES)):#

            _village_=reset._VILLAGES[j]

            text("Village / house at: ",5,startJ,newScreen)
            text("X:"+str(_village_[0])+"  Y:"+str(_village_[1]),5+5+Font.size("Village / house at: ")[0],startJ,newScreen)
            newVillages.append(Button(5+5+Font.size("Village / house at: ")[0]+5+Font.size("X:"+str(_village_[0])+"  Y:"+str(_village_[1]))[0],startJ,"Open "+str(j)+'_.txt'))
            startJ+=30
            text("Loot: ",5,startJ,newScreen)
            text(str(_village_[2]),5+5+Font.size("Loot: ")[0],startJ,newScreen)

            startJ+=30
            newVillages.append(Button(5,startJ,' Delete village / house '+str(reset._VILLAGES[j][3])+' '))
            startJ+=40

        options(newVillages,newScreen)
        

    elif RECRUITABLE is True:
        newRecruit=[]
        newRecruit.append(Button(5,85,"Add new enemy or neutral player to recruit"))

        startJ=115
        
        for j in range(len(reset._RECRUITABLE)):#
            thisRecruit=reset._RECRUITABLE[j]
            text("Potential Recruit: ",5,startJ,newScreen)
            text(str(thisRecruit[0]),5+5+Font.size("Potential Recruit: ")[0],startJ,newScreen)
            newRecruit.append(Button(5+5+Font.size("Potential Recruit: "+str(thisRecruit[0]))[0]+5,startJ,'Remove Recruit'+str(j)))
            startJ+=30
            newRecruit.append(Button(5,startJ,'Add New Recruiter'+str(j)))
            newRecruit.append(Button(5+10+Font.size('Add New Recruiter')[0],startJ,'Open '+str(j+1)+'_convo.txt'))

            for i in range(len(thisRecruit[1])):
                startJ+=30
                item=thisRecruit[1][i]
                text(item,5,startJ,newScreen)

                newRecruit.append(Button(5+4+Font.size(item)[0],startJ,'Remove Recruiter'+str(i)+str(j)))

            startJ+=40

        options(newRecruit,newScreen)


    elif WINCONDITIONS is True:
            
        options(newWin,newScreen)

    elif displayChapterName is True:
        onlyOneOption=[]

        text(" Chapter Name: ",5,80,newScreen,Font)
        onlyOneOption.append(Button(5+5+Font.size(" Chapter Name: ")[0],81,str(reset._CHPNAME)))      

        text(" Water or Lava: ",5,105,newScreen,Font)
        onlyOneOption.append(Button(5+5+Font.size(" Water or Lava: ")[0],106," Water "))
        onlyOneOption.append(Button(5+5+Font.size(" Water or Lava: ")[0]+5+Font.size(" Water ")[0],106," Lava "))


        onlyOneOption.append(Button(5,146," Open 1_convo "))
        onlyOneOption.append(Button(5,171," Open 2_convo "))
        onlyOneOption.append(Button(5,196," Open 4_convo "))

        #1_
        onlyOneOption.append(Button(6+5+Font.size(" Open 1_convo ")[0],146," MAP_1 "))
        onlyOneOption.append(Button(6+5+Font.size(" Open 1_convo ")[0]+5+Font.size(" MAP_1 ")[0],146," COLOR_1 "))#chnge back to 1_COLOR
        #2_
        onlyOneOption.append(Button(6+5+Font.size(" Open 2_convo ")[0],171," MAP_2 "))
        onlyOneOption.append(Button(6+5+Font.size(" Open 2_convo ")[0]+5+Font.size(" MAP_2 ")[0],171," COLOR_2 "))
        #4_
        onlyOneOption.append(Button(6+5+Font.size(" Open 4_convo ")[0],196," MAP_4 "))
        onlyOneOption.append(Button(6+5+Font.size(" Open 4_convo ")[0]+5+Font.size(" MAP_4 ")[0],196," COLOR_4 "))

        if reset.convo_map_1_type[0]!='Ellipse':
            updateThisMap1=' Update MAP1 '
        else:
            updateThisMap1=' Cycle Color1 '
        onlyOneOption.append(Button(10+5+Font.size(" Open 1_convo ")[0]+Font.size(" 1_MAP ")[0]+5+Font.size(" 1_COLOR ")[0]+2,146,str(updateThisMap1)))

        if reset.convo_map_2_type[0]!='Ellipse':
            updateThisMap2=' Update MAP2 '
        else:
            updateThisMap2=' Cycle Color2 '
        onlyOneOption.append(Button(10+5+Font.size(" Open 2_convo ")[0]+Font.size(" 2_MAP ")[0]+5+Font.size(" 2_COLOR ")[0]+2,171,str(updateThisMap2)))

        if reset.convo_map_4_type[0]!='Ellipse':
            updateThisMap4=' Update MAP4 '
        else:
            updateThisMap4=' Cycle Color4 '
        onlyOneOption.append(Button(10+5+Font.size(" Open 4_convo ")[0]+Font.size(" 4_MAP ")[0]+5+Font.size(" 4_COLOR ")[0]+2,196,str(updateThisMap4)))

        
        pygame.draw.line(newScreen,(0,0,0),(2+5+Font.size(" Open 1_convo ")[0],146),(2+5+Font.size(" Open 1_convo ")[0],214),2)
        pygame.draw.line(newScreen,(0,0,0),(6+5+Font.size(" Open 1_convo ")[0]+Font.size(" MAP_1 ")[0]+5+Font.size(" COLOR_1 ")[0]+2,146),(6+5+Font.size(" Open 1_convo ")[0]+Font.size(" MAP_1 ")[0]+5+Font.size(" COLOR_1 ")[0]+2,214),2)

        options(onlyOneOption,newScreen)
        

        pygame.draw.rect(newScreen,(255,255,255),[10,230,265,394])
        pygame.draw.line(newScreen,(0,0,0),(13,255),(270,255),2)


        optionsForConvos=['Options for the conversation files are as follows:','set-bg;filename;addx;addy','dialogue;color;name;sentence','move-action;unit;newx;newy','kill-action;unit;victim_unit_name','death;unit','gain-item;type;name','--types:item, weapon, money, or recruits','user-prompt;query1;query2','user-input;ans1=response1;ans2=response2','change-music;filename','black-screen-fade;time(seconds)','time-pause;time(sec)']
        
        ys=235
        for elem in optionsForConvos:
            Text = Font.render(elem, 1, (0,10,10))
            newScreen.blit(Text, (13,ys+5))
            ys+=30
        

    elif showEnemyInfo is True and Enemy is True:

        text("EDITING : "+showEnemy.text,5,60,newScreen)

        enemyChoices=[Button(5,361,'Enter Name'),Button(5,90,'Choose Faction'),Button(5+10+Font1.size('Enter Name'+str(showEnemy.main[0]))[0],361,'Make Class as Name'),Button(5,120,'Choose Class'),Button(5,150,'Choose Weapon'),Button(5,180,'Toggle Empty'),Button(5,321,'Choose Location'),Button(155+5,401,'True'),Button(155+5+Font1.size('True')[0]+5,401,'False'),Button(155+5+Font1.size('TrueFalse')[0]+10,401,'None')]
        text(str(showEnemy.main[0]),5+Font1.size('Enter Name')[0]+5,360,newScreen)

        for i in range(1,21):
            #print i
            if i>=1 and i<=10:
                adjY=250
                adjX=0
            else:
                adjY=280
                adjX=10

            if len(str(i))==1:
                addOne=" "
            else:
                addOne=""
                
            enemyChoices.append(Button(5+((i-adjX)*25)-25,adjY,"-"+addOne+str(i)+"-"))

        text(str(showEnemy.main[2]),5+Font1.size('Choose Faction')[0]+5,90,newScreen)
        text(str(showEnemy.main[1]),5+Font1.size('Choose Class')[0]+5,120,newScreen)
        text(str(showEnemy.main[5]),5+Font1.size('Choose Weapon')[0]+5,150,newScreen)
        if showEnemy.empty[0]=="False":
            _blit_="Enemy currently in Play"
        else:
            _blit_="Enemy currently NOT in Play"
        text(_blit_,5+Font1.size('Toggle Empty')[0]+5,180,newScreen)


        text('Choose Enemy Level Below',5,220,newScreen)

        text('Select People in Move Group:',5,440,newScreen)


        enemyMoveChoices=[]
        _ii=-1
        for enemy in enemyPos:
            if enemy.empty[0]=="False":
                _ii+=1

                if _ii <=13:
                    _yy=0
                    _iadd=0
                elif _ii > 13 and _ii <=27:
                    _yy=20
                    _iadd=14
                elif _ii > 27 and _ii <=41:
                    _yy=40
                    _iadd=28
                else:
                    _yy=60
                    _iadd=42

                enemyMoveChoices.append(Button(5+(20*(_ii-_iadd)),534-70+_yy,enemy.text))
                #else:
                #    _ii-=1


        text('When enemy enters battle: ',5,555,newScreen)
        text('And from which direction: ',5,610,newScreen)

        chooseWhenEnter=[]


        addLength=5+ Font.size('And from which direction: ')[0]

        directionOptions=['N','S','E','W','NA']
        for q in range(len(directionOptions)):
            
            chooseWhenEnter.append(Button(5+addLength,611," "+str(directionOptions[q])+" "))
            addLength+=Font.size(" "+str(directionOptions[q])+" ")[0]
            addLength+=1
        
        jk_x=0
        for jk in range(1,17):
            addLength=0
            for l in range(jk):
                addLength+=Font.size(" "+str(l)+" ")[0]
            addLength+=jk
            chooseWhenEnter.append(Button(-8+addLength,577," "+str(jk)+" "))

        options(chooseWhenEnter,newScreen)   
            
        options(enemyMoveChoices,newScreen)
        groupedList=showEnemy.main[9:len(showEnemy.main)]

        for item in groupedList:
            for button in enemyMoveChoices:
                if button.text==item:
                    pygame.draw.rect(newScreen,(14,215,0),[button.x,button.y,button.width,button.height],1)
                    pygame.draw.rect(newScreen,(50,160,45),[button.x+1,button.y+1,button.width-2,button.height-2],1)
                    break


        saveSquare=[]
        for button in enemyChoices:
            if button.text[0]=="-":
                #print button.text,"text"
                edit1=button.text[1:]
                edit1=int(edit1[:-1])

                if int(edit1)==int(showEnemy.main[3]):
                    saveSquare=[button.x,button.y,button.width,button.height]
                    #pygame.draw.rect(newScreen,(255,255,0),[button.x,button.y,button.width,button.height],2)
                    break
                                

        options(enemyChoices,newScreen)

        if saveSquare!=[]:
            pygame.draw.rect(newScreen,(255,255,0),saveSquare,2)
        
        for button in enemyChoices:

            if button.text in ['False','True','None']:
                if str(showEnemy.main[8])==button.text:
                    pygame.draw.rect(newScreen,(255,255,0),[button.x,button.y,button.width,button.height],2)
                    break
                    

        text(' X: '+showEnemy.main[6]+' // Y: '+showEnemy.main[7]+' ',5+Font1.size('Choose Location')[0]+5,320,newScreen)#Choose Location

        text('Choose WaitOnMove Status',5,400,newScreen)
                

        if showUnits is True:
            yellowT=pygame.Surface((30,30),pygame.SRCALPHA,32)

            pygame.draw.rect(yellowT,(255,255,0),[0,0,29,29],2)
            
            screen.blit(yellowT,(((showEnemyPos[0]-array_addx)*tilesize)+110,(showEnemyPos[1]-array_addy)*tilesize))
        

    options(rightSide,newScreen)

    screen.blit(newScreen,(920,0))


    options(chooseMapOrUnits)


    if entering is True:

        #darken bg
        s1a=pygame.Surface((mapwidth,mapheight),pygame.SRCALPHA,32)
        s1a.fill((0,0,0,140))
        screen.blit(s1a,(0,0))

        one=TextE((mapwidth/2)-Font1.size(enteringText)[0]/2,mapheight/2-70,enteringText,Font1)
        #two=Text((mapwidth/2)-Font1.size(createNewText)[0]/2,mapheight/2-37,createNewText,Font1)
        textDisplay=[(one,(130,140,160))]#,(two,(250,250,250))]
        for item in textDisplay:
            blitText(item[0],item[1])

        totalLen=Font1.size(" Add ")[0]+Font1.size(" Cancel ")[0]+6+4
        partLen=Font1.size(" Add ")[0]+2+3
        saveCancel=[Button((mapwidth/2)-totalLen/2,mapheight/2," Add ",Font1),Button((mapwidth/2)-totalLen/2+partLen,mapheight/2," Cancel ",Font1)]#,Text((mapwidth/2)-(Font1.size(currentDirectory)[0]/2),45,currentDirectory,Font1),Text((mapwidth/2)-(Font1.size("Current Directory")[0]/2),18,"Current Directory",Font1)]
        optionsEnter(saveCancel)#,Font1)
        
        blitText(TextE((mapwidth/2)-Font1.size(entered_text)[0]/2+2,mapheight/2-37,entered_text,Font1),(220,200,200))
        

    elif DISPLAY_OPTIONS is True:

        s1a=pygame.Surface((mapwidth,mapheight),pygame.SRCALPHA,32)
        s1a.fill((0,0,0,230))
        screen.blit(s1a,(0,0))

        displayedOptions=[]

        for i in range(len(DISPLAY_LIST)):

            item=DISPLAY_LIST[i]

            #dumb way to do this, but it works
            if i>15 and i<=31:
                xX=325
                yY=i-16
            elif i>31 and i<=47:
                xX=500
                yY=i-32
            elif i>47 and i<=63:
                xX=675
                yY=i-48
            elif i>63 and i<=79:
                xX=850
                yY=i-64
            elif i>79 and i<=95:
                xX=1025
                yY=i-80
            elif i>95:
                xX=1200
                yY=i-96
            else:
                xX=150
                yY=i

            if DISPLAY_OPTIONS is True and DISPLAY_LIST==allClasses:
                useAltName=item.actualName
            else:
                useAltName=item.name

            displayedOptions.append(Button(xX-110,(yY*39)+15,useAltName,"bs","main","one","two","three","four","five","empty",pygame.transform.scale(item.pic,(30,30))))
            


        options(displayedOptions)

        for item in displayedOptions:
            screen.blit(item.pic,(item.x-33,item.y-4))

            SI=False
                

            for listt in [lightMagic,elementalMagic,darkMagic,allBows,allLances,allSwords,allAxes,allStaves,allGear,allClaws,allFangs,allEvilMagic,dragonFire,allMelee]:#enemyWeapons]:#
                for wpn in listt:
                    #print item.text,wpn.name
                    if item.text[3:]==wpn.name:
                        #print "to get:",showEnemy.main[1]
                        for r in range(0,sheet.nrows):
                            #print sheet.cell_value(r,0)
                            if str(sheet.cell_value(r,0))==showEnemy.main[1]:

                                checkList=[]
                                divide=str(sheet.cell_value(r,15))

                                wpnTypes=divide.split(",")
                                for weaponss in wpnTypes:
                                    newW=weaponss.replace("\"", "")

                                    checkList.append(newW)
                                break
                            
                        #print "final:",wpn.wpnType,checkList
                        if wpn.wpnType in checkList:
                            SI=True
                            if wpn.wpnType=="Magic":
                                checkMagic=checkMagicType(newW,showEnemy.main[1],wpn.name)
                                #print checkMagic, wpn.name
                                if checkMagic is False:
                                    SI=False
                        break
                

            if SI is True and CHESTS is False and VILLAGES is False and ARMORY is False and VENDOR is False:
                
                pygame.draw.rect(screen,(255,255,0),[item.x-3,item.y-3,item.width+6,item.height+6],3)
                

        if DISPLAY_LIST==allClasses:
            for button in displayedOptions:
                if button.text==showEnemy.main[1]:
                    pygame.draw.rect(screen,(0,200,0,200),[button.x-3,button.y-3,button.width+6,button.height+6],3)           
                    break
        elif DISPLAY_LIST==factionList:
            for button in displayedOptions:
                if button.text==showEnemy.main[2]:
                    pygame.draw.rect(screen,(0,200,0,200),[button.x-3,button.y-3,button.width+6,button.height+6],3)           
                    break
        elif DISPLAY_LIST==ALL_WEAPONS and CHESTS is False and VILLAGES is False and ARMORY is False and VENDOR is False: #don't show border when selecting items
            for button in displayedOptions:
                if button.text[3:]==showEnemy.main[5]:
                    pygame.draw.rect(screen,(0,200,0,200),[button.x-3,button.y-3,button.width+6,button.height+6],3)           
                    break

    backupSAVE+=1
    if backupSAVE==2300: #just under every minute backup the map
        backupSAVE=0
        backupToTxtFile()
        
            
    if chooseNewLocation is True:

        s4=pygame.Surface((mapwidth,mapheight),pygame.SRCALPHA,32)
        pygame.draw.polygon(s4,(0,0,0,200),[(0,0),(110,0),(110,19*tilesize),(110+(25*tilesize),19*tilesize),(110+(25*tilesize),0),(1220,0),(1220,640),(0,640)])#(720+200+300,640)
        screen.blit(s4,(0,0))
    

    chooseNewLocationWasJustTrue=False
    
    pygame.display.update()
    
    clock.tick(40)

    
