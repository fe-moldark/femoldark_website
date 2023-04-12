def newMap(SAVESLOT):
    if SAVESLOT=="_SAVESLOT_SUSPENDPOINT1":    
        Folder="C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/"+SAVESLOT+"/"
    elif SAVESLOT=="_NEWGAME":
        Folder="C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/"+SAVESLOT+"/"
    else:
        loadgotoFileA=open("C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/"+SAVESLOT+"/_LOAD.txt","r").read().split('\n')
        loadgotoFile=loadgotoFileA[0]
        Folder="C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/"+SAVESLOT+"/"
        
    all_sprites=pygame.sprite.Group()
    enemy_sprites=pygame.sprite.Group()
    ally_sprites=pygame.sprite.Group()
    
    #MONEY
    moneyFile = open(Folder+"EXTRA/"+"_MONEY.txt", "r")
    GOLD=int(moneyFile.readlines()[0])
    moneyFile.close()
    #TURN NUMBER
    turnFile = open(Folder+"EXTRA/"+"_TURNNUMBER.txt", "r")
    TurnNumber=int(turnFile.readlines()[0])
    turnFile.close()
    #CHAPTER
    chapterFile = open(Folder+"EXTRA/"+"_CHAPTER.txt", "r")
    CHAPTERlines=chapterFile.readlines()
    CHAPTER=[CHAPTERlines[0],CHAPTERlines[1],CHAPTERlines[2]]#"Chapter "+str(CHAPTERlines[0][:-1])+": "+str(CHAPTERlines[1][:-1])
    chapterFile.close()


########################################################
    """
    if SAVESLOT != "_NEWGAME":
        armoryInv=[]
        itemsInArmory=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/_ARMORY/')
        for item in itemsInArmory:

            lines=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/_ARMORY/'+str(item), "r").read().split('\n')
            itemName=str(lines[0])
            itemSupply=int(lines[1])

            toAdd=returnItem(itemName)

            armoryInv.append((toAdd,itemSupply))

        vendorInv=[]
        itemsInVendor=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/_VENDOR/')
        for item in itemsInVendor:

            lines=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/_VENDOR/'+str(item), "r").read().split('\n')
            itemName=str(lines[0])
            itemSupply=int(lines[1])

            toAdd=returnItem(itemName)

            vendorInv.append((toAdd,itemSupply))
    else:
        armoryInv=[]
        vendorInv=[]
        

    """
            
########################################################
    
    ChpAsNum=str(CHAPTER[0])[:-1]                           
    if int(ChpAsNum)==0:
        writee="Prequel"
    else:
        writee="Chapter "+str(int(ChpAsNum))

    print ChpAsNum,"ChpAsNum"
        
    pygame.display.set_caption(str(writee)+": "+str(CHAPTERlines[1][:-1]))
    
    #SETTINGS-- grid,volume,fog
    settingsFile = open(Folder+"EXTRA/"+"_SETTINGS.txt", "r")
    settingsLines=settingsFile.readlines()
    GRID=int(str(settingsLines[0][:-1]))
    VOLUME=int(str(settingsLines[1][:-1]))
    fog_check=str(settingsLines[2])

    if fog_check == "False":
        fogOfWar=False
    elif fog_check == "True":
        fogOfWar=True
        
    if fogOfWar is True:
        FOG=0
    else:
        FOG=1
    settingsFile.close()

    #different ways to start - newgame, suspend or chapter save
    if SAVESLOT=='_NEWGAME':
        mapOpened="_LOAD.txt"
        File = open(Folder+"SAVEMAP/"+mapOpened, "r")
        lines2 = File.readlines()
        File.close()
        #
    elif SAVESLOT=="_SAVESLOT_SUSPENDPOINT1": 
        mapOpened="_LOAD.txt"
        File = open(Folder+"SAVEMAP/"+mapOpened, "r")
        lines2 = File.readlines()
        File.close()
    else:

        loadgotoFileA=open("C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/"+SAVESLOT+"/_LOAD.txt","r").read().split('\n')
        loadgotoFile=loadgotoFileA[0]
        Folder="C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/"+loadgotoFile

        mapOpened="_LOAD.txt"
        File = open("C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/"+SAVESLOT+"/"+mapOpened, "r")
        lines2 = File.readlines()
        File.close()

        
    File = open("C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/"+lines2[0]+"/MAP.txt", "r")
    lines = File.readlines()
    File.close()

    #WINCONDITIONS
    seizeFile = open("C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/"+lines2[0]+"/WINCONDITIONS.txt", "r").read().split('\n')
    win_how=(seizeFile[0],seizeFile[1],seizeFile[2])

    if win_how[0]=="SEIZE":
        WINCONDITIONS=["SEIZE",(win_how[1],win_how[2])]
    elif win_how[0]=="ESCAPE":
        WINCONDITIONS=["ESCAPE",(win_how[1],win_how[2])]
    elif win_how[0]=="KILL":
        WINCONDITIONS=["KILL",str(win_how[1])]#Just the name
    elif win_how[0]=="ROUT":
        WINCONDITIONS=["ROUT",[]]
    elif win_how[0]=="SURVIVE":
        WINCONDITIONS=["SURVIVE",int(win_how[1])]
    elif win_how[0]=="PROTECT":
        WINCONDITIONS=["PROTECT",str(win_how[1]),str(win_how[2])]#deathquote of the guy

    ii=0
    Retain=False
    temparray=[]
    for line in lines:
        templine=str(line)
        templine=templine[1:]
        templine=templine[:-1]

        badList=["[","]","(",")",","]#to remove characters surrounding the pic_name and rotation

        saveThis=""
        saveThisRotate=""
        tempLine=[]
        getRotate=False
        
        for letter in templine:
            letter=str(letter)
            if getRotate is False:
                if letter not in badList and Retain is True and str(letter) != "'":
                    if getRotate is False:
                        saveThis+=str(letter)
                    

                elif str(letter) == "'": #add new info

                    if Retain is True:
                        Retain = False

                        ii+=1
                        getRotate=True
                        
                    else:
                        Retain=True

            elif getRotate is True:
                
                if letter not in badList  and str(letter) != "," and str(letter) != " ":
                    if str(letter)=="-" or type(int(letter))==int:
                        saveThisRotate+=str(letter)

                elif str(letter)==")":
                    tempLine.append((str(saveThis),int(saveThisRotate)))

                    getRotate=False
                    saveThis=""
                    saveThisRotate=""

        temparray.append(tempLine)

    mapWidth = len(temparray[0])
    mapHeight = len(temparray)

    tilemap=[]
    blank_list=[]
    for row in range(mapHeight):
        blank_list=[]
        for column in range(mapWidth):
            myIMG=str(temparray[row][column][0])
            my_img=pygame.image.load(myIMG)
            my_img=pygame.transform.rotate(my_img,temparray[row][column][1])

            blank_list.append(my_img)
        tilemap.append(blank_list)

    #########################################################################################################
    #FENCELIST= ['tile housewall5.png','tile housewall5a.png','tile housewall2.png','tile housewall3.png','tile housewall4.png','tile housewall1.png','tile housewall7.png']
    #WALSLIST=['pillar_a.png','pillar column2.png','pillar column.png','wall_1.png','wall_2.png','wall_3.png','wall_4.png','roof_half5.png','roof_half6.png','roof_half7.png','roof_half8.png','roof_half9.png','roof_half10.png','roof_half10a.png','roof_half11.png','roof_half4.png','roof_half2a.png','roof_half2.png','roof_half1.png','roof_half3.png','roof_half.png']
    #WALSLIST2=[]
    #WATERLIST=['tile water1.png','tile water2.png','tile water3.png','tile water4.png','tile water5.png','tile water6.png','tile water7.png','tile water8.png',"water0.png","water1.png","water2.png","water3.png","water4.png","water5.png","water6.png","water7.png","water8.png","water8a.png","water9.png","water9a.png"]
    #########################################################################################################

    blueredmap = []#create the default gridmap for movement uses ONLY, not blitting
    for row in range(mapHeight):
        new_row = []
        for column in range(mapWidth):
            if temparray[row][column][0] in WALSLIST:# or temparray[row][column][0] in WATERLIST or temparray[row][column][0] == 'tile column.png' or temparray[row][column][0] == 'tile door2.png':
                new_row.append(1)
            else:
                new_row.append(0)
        blueredmap.append(new_row)

    grid = []
    for row in blueredmap:
        grid.append(row)

    if SAVESLOT == "_SAVESLOT_SUSPENDPOINT1":#
        _allDoors=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/SAVEMAP/_DOOR/')
        
        for _file in _allDoors:
            lines=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/SAVEMAP/_DOOR/'+str(_file), "r").read().split('\n')
            doorx=int(lines[0])
            doory=int(lines[1])

            #doorIMG=str(lines[2])

            saveRo=temparray[doory][doorx][1]#tile door3.png

            ######################################################################################################

            #intelligently choose what "open" door looks like based off surrounding tiles
            surroundingTiles=[temparray[doory+1][doorx][0],temparray[doory-1][doorx][0],temparray[doory][doorx+1][0],temparray[doory][doorx-1][0]]
            for _tilePos in range(len(surroundingTiles)):
                _tile_=surroundingTiles[_tilePos]
                if _tile_ in _ground_tiles:
                    indexed=_ground_tiles.index(_tile_)

                    newDoorway=_opened_door_tiles[indexed]

            #############################################################################

            rotation=temparray[doory][doorx][1]
            temparray[doory][doorx]=(str(newDoorway),rotation)

            ######################################################################################################

            blueredmap[doory][doorx]=0

            tilemap[doory][doorx]=pygame.image.load(str(newDoorway))

        for _file in _allDoors:#delete from suspend, will only be rewritten if saved again - THIS MEANS A SUSPEND POINT IS ONLY GOOD ONCE, WHICH IS INTENTIONAL - OTHERWISE YOU COULD TREAT A SUSPEND SAVE LIKE A NORMAL SAVE AND CHEAT
            path='C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/SAVEMAP/_DOOR/'+str(_file)
            os.remove(path)





    #armories locatoin
    class Armory:
        def __init__(self, location, listwhat):
            self.location=location
            self.armoryInv=listwhat

            Armory.location=self.location
            Armory.armoryInv=self.armoryInv

    class Vendor:
        def __init__(self, location, listwhat):
            self.location=location
            self.vendorInv=listwhat

            Vendor.location=self.location
            Vendor.vendorInv=self.vendorInv
######################################################################
    AllArmories=[]
    try:
        lines=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/LOOT_VILLAGECHEST/ARMORY/LOCATION.txt', "r").read().split('\n')
        x_x=int(lines[0])
        y_y=int(lines[1])


        checkL=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/_ARMORY/')
        
        if checkL==[]:
            usePath='C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/LOOT_VILLAGECHEST/ARMORY/'
        else:
            usePath='C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/_ARMORY/'


        listArmory=os.listdir(usePath)
        listAll=[]
        for _file in listArmory:
            if _file != "LOCATION.txt":
                lines=open(usePath+_file, "r").read().split('\n')
                name=str(lines[0])
                num=int(lines[1])

                

                new=returnItem(name)
                listAll.append((new,num))

        AllArmories.append(Armory((x_x,y_y),listAll))

    except (WindowsError, IOError):
        #sys.exit()
        pass
        
        
    ########
    AllVendors=[]
    try:
        lines=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/LOOT_VILLAGECHEST/VENDOR/LOCATION.txt', "r").read().split('\n')
        x_x=int(lines[0])
        y_y=int(lines[1])

        if os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/_VENDOR/')==[]:
            usePath='C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/LOOT_VILLAGECHEST/VENDOR/'
        else:
            usePath='C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/_VENDOR/'

        listVendor=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/LOOT_VILLAGECHEST/VENDOR/')
        listAll=[]
        for _file in listVendor:
            if _file != "LOCATION.txt":
                lines=open(usePath+_file, "r").read().split('\n')
                name=str(lines[0])
                num=int(lines[1])

                new=returnItem(name)
                listAll.append((new,num))

        AllVendors.append(Vendor((x_x,y_y),listAll))

    except (IOError, WindowsError):
        pass

    newMap.AllArmories=AllArmories
    newMap.AllVendors=AllVendors
    newMap.armoryInv=[]
    newMap.vendorInv=[]
    
    try:
        
        newMap.armoryInv=AllArmories[0].armoryInv
        newMap.vendorInv=AllVendors[0].vendorInv
        
    except (IndexError,AttributeError) as error:
        pass
        #newMap.armoryInv
        #newMap.vendorInv
        
#########################################################

        
    #GET CHESTS
    listChests=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/LOOT_VILLAGECHEST/CHEST/')
    listMyChests=[]
    for _file in listChests:
        lines=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/LOOT_VILLAGECHEST/CHEST/'+str(_file), "r").read().split('\n')
        chestx=int(lines[1])
        chesty=int(lines[2])









            
  
    #GET CHESTS
    listChests=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/LOOT_VILLAGECHEST/CHEST/')
    listMyChests=[]
    for _file in listChests:
        lines=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/LOOT_VILLAGECHEST/CHEST/'+str(_file), "r").read().split('\n')
        chestx=int(lines[1])
        chesty=int(lines[2])
        chestTreasure=lines[3]

        saveRo=temparray[chesty][chestx][1]
        #temparray[chesty][chestx]=("tile chest.png",saveRo)
        #tilemap[chesty][chestx]=pygame.image.load("tile chest.png")

        gotAWpn=False
        for item in allGear:
            if str(item.name)==str(chestTreasure):
                gotAWpn=True
                chest_treasure=returnItem(item.name)
                break
            
        if gotAWpn is False:
            chest_treasure=str(chestTreasure)
        else:
            pass

        myChest=Chest((chestx,chesty),chest_treasure)
        listMyChests.append(myChest)

        if SAVESLOT == "_SAVESLOT_SUSPENDPOINT1":
            adjustedChests=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/SAVEMAP/_CHEST/')
            for adjustedChest in adjustedChests:
                lines3=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/SAVEMAP/_CHEST/'+str(adjustedChest), "r").read().split('\n')

                saveRo=0#temparray[int(lines3[1]][int(lines3[0]][1]
                #imgStringChest=str(lines[2])
                
                temparray[int(lines3[1])][int(lines3[0])]=(str(lines3[2]),saveRo)
                tilemap[int(lines3[1])][int(lines3[0])]=pygame.image.load(str(lines3[2]))


            #delete chest in suspend
            for _file in adjustedChests:#
                path='C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/SAVEMAP/_CHEST/'+str(_file)
                os.remove(path)
                

    #GET VILLAGES
    listVillages=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/LOOT_VILLAGECHEST/VILLAGE/')
    listMyHouses=[]
    for _file in listVillages:
        lines=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/LOOT_VILLAGECHEST/VILLAGE/'+str(_file), "r").read().split('\n')
       
        houseVisited=str(lines[0])
        
        if houseVisited=="NOTVISITED":
            house_visited=False
        elif houseVisited=="VISITED":
            house_visited=True
            
        housex=int(lines[1])
        housey=int(lines[2])
        houseTreasure=lines[3]

        house_text=[]
        for i in range(4,len(lines)):
            house_text.append(str(lines[i]))
            
        notMoney=False
        for item in allGear:
            if str(item.name)==str(houseTreasure):
                notMoney=True
                house_treasure=returnItem(item.__class__.__name__)
                break

        if notMoney is False:
            house_treasure=int(houseTreasure)#means money

        myHouse=House((int(housex),int(housey)),house_visited,house_treasure,house_text)
        listMyHouses.append(myHouse)

        if SAVESLOT == "_SAVESLOT_SUSPENDPOINT1":
            adjustedHouses=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/SAVEMAP/_VILLAGE/')
            for adjustedHouse in adjustedHouses:
            
                lines3=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/SAVEMAP/_VILLAGE/'+str(adjustedHouse), "r").read().split('\n')
                for item in lines3:
                    if (housex,housey)==(int(lines3[0]),int(lines3[1])):
                        #create
                        saveRo=temparray[housey][housex][1]
                        temparray[housey][housex]=("tile housewall7.png",saveRo)
                        
                        tilemap[housey][housex]=pygame.image.load("tile housewall7.png")

                        blueredmap[housey][housex]=1#not free, village closed

                    else:
                        pass

            #delete chest in suspend
            for _file in adjustedHouses:#
                path='C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/SAVEMAP/_VILLAGE/'+str(_file)
                os.remove(path)


                

    listAllyToGo=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/ALLYSTART/')
    whereDoIGo=[]
    for _file in listAllyToGo:
        lines=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/ALLYSTART/'+str(_file), "r").read().split('\n')
        whereDoIGo.append((int(lines[0]),int(lines[1])))


    ###################################################
        
    allowedUnits=len(whereDoIGo)
    if SAVESLOT == "_SAVESLOT_SUSPENDPOINT1" or SAVESLOT=="_NEWGAME":
        templistALLIES=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/ALLIES/')
        listALLIES=[]
        for _file_ in templistALLIES:
            if SAVESLOT=="_NEWGAME":
                listALLIES.append(_file_)
            elif SAVESLOT=="_SAVESLOT_SUSPENDPOINT1":
                maybeFalse=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/ALLIES/'+_file_+'/empty.txt').read().split('\n')
                if "False" in maybeFalse:
                    listALLIES.append(_file_)
                    
    else:#means a save file
        templistALLIES=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/ALLIES/')
        listALLIES=[]
        for _file_ in templistALLIES:
            maybeFalse=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/ALLIES/'+_file_+'/empty.txt').read().split('\n')
            if "False" in maybeFalse:
                listALLIES.append(_file_)

    #
        
    listAlly=[]#SAVESLOT
    tempALLYlist=[]
    countAllyPos=-1
    addGreyAllies=[]
    #ally_sprites_no_edit=pygame.sprite.Group()

    neutral_sprites=pygame.sprite.Group()
    neutral_sprites_no_edit=pygame.sprite.Group()
    copy_neutral_sprites_no_edit=neutral_sprites_no_edit.copy()

    for _file in listALLIES:#LOAD UP ALL ALLIES
        countAllyPos+=1
        _main=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/ALLIES/'+_file+'/1_.txt').read().split('\n')
        
        _one=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/ALLIES/'+_file+'/1_spot1(weapon).txt').read().split('\n')
        _two=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/ALLIES/'+_file+'/1_spot2.txt').read().split('\n')
        _three=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/ALLIES/'+_file+'/1_spot3.txt').read().split('\n')
        _four=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/ALLIES/'+_file+'/1_spot4.txt').read().split('\n')
        _five=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/ALLIES/'+_file+'/1_spot5.txt').read().split('\n')

        _inv=[_one,_two,_three,_four,_five]

        myInv=[]
        for _invItems in _inv:
            cantfind=False
            for item in allGear:
                check=_invItems[0]
                if str(item.name)==str(check):
                    if str(item.__class__.__name__) == "Staff":
                        invItem=Staff(item.name,item.rank,item.rang,int(_invItems[1]),int(_invItems[2]),item.addHeal,item.addXP,item.wpnType,item.value)
                    elif str(item.__class__.__name__) == "Weapon":
                        invItem=Weapon(item.name,item.rank,item.rang,int(_invItems[1]),int(_invItems[2]),item.weight,item.dmg,item.hit,item.wpnType,item.value,item.crit)
                    elif str(item.__class__.__name__) == "Item":#class item
                        invItem=Item(item.name,item.value,int(_invItems[1]),int(_invItems[2]))
                    elif str(item.__class__.__name__) == "UsableItem":#,"UsableItem"]:#class item
                        invItem=UsableItem(item.name,item.value,int(_invItems[1]),int(_invItems[2]),str(_invItems[3]))
                    myInv.append(invItem)
                    cantfind=True
                    break
            if cantfind is False:
                print _invItems, "CANT FIND, CHECK THE EXCEL FOR THE NAME OF THE ITEM AND EITHER ADD IT THERE, OR IT'S AN OLD ITEM AND SHOULD BE DELETED DIRECTLY FROM THE FILE"#note: this SHOULD only appear when using old saves for testing

        pic=pygame.image.load(str(_main[0]))
        name=str(_main[1])
        CLAS=str(_main[2])
        
        for item in ALLCLASSES:
            
            if str(CLAS)==str(item.actualName):#
                clas=item
                
                break
        race=_main[3]
        lvl=int(_main[4])
        xp=int(_main[5])

        if SAVESLOT == "_SAVESLOT_SUSPENDPOINT1":
            x=int(_main[6])
            y=int(_main[7])
        else:
            x=int(_main[6])
            y=int(_main[7])

            if (x,y) in whereDoIGo:
                pass

            else:
                while whereDoIGo[countAllyPos]==(x,y):
                    countAllyPos+=1
                x=int(whereDoIGo[countAllyPos][0])#int(_main[6])
                y=int(whereDoIGo[countAllyPos][1])#int(_main[7])

            #

            #

        grey_pic=pygame.image.load(str(_main[8]))
        x4_pic=pygame.image.load(str(_main[9]))
        
        DEATH=_main[10]
        if DEATH=="True":
            death=True
        elif DEATH=="False":
            death=False
        deathQuote=_main[11]
        
        if SAVESLOT != "_SAVESLOT_SUSPENDPOINT1":
            if lvl==int(1):#set to class basics
                hppart=clas.stats[0]
                hpfull=clas.stats[0]
                strength=clas.stats[1]
                magic=clas.stats[2]
                skill=clas.stats[3]
                speed=clas.stats[4]
                luck=clas.stats[5]
                defense=clas.stats[6]
                resistance=clas.stats[7]
                move=clas.stats[8]
                constitution=clas.stats[9]
            else:
                hppart=_main[12]
                hpfull=_main[13]
                strength=_main[14]
                magic=_main[15]
                skill=_main[16]
                speed=_main[17]
                luck=_main[18]
                defense=_main[19]
                resistance=_main[20]
                move=_main[21]
                constitution=_main[22]
        elif SAVESLOT == "_SAVESLOT_SUSPENDPOINT1":
            hppart=_main[12]
            hpfull=_main[13]
            strength=_main[14]
            magic=_main[15]
            skill=_main[16]
            speed=_main[17]
            luck=_main[18]
            defense=_main[19]
            resistance=_main[20]
            move=_main[21]
            constitution=_main[22]

        #####################################
        _weapons=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/ALLIES/'+_file+'/WPN_PRO.txt').read().split('\n')
        #weapon experience laod
        SWD=int(_weapons[0])
        LNC=int(_weapons[1])
        AXE=int(_weapons[2])
        BOW=int(_weapons[3])
        LGT=int(_weapons[4])
        ELE=int(_weapons[5])
        DRK=int(_weapons[6])
        STF=int(_weapons[7])


        #save the strings of pictures
        mainPIC=_main[0]
        greyPIC=_main[8]
        x4PIC=_main[9]#for villages
        savePictures=[mainPIC,greyPIC,x4PIC]
        

        allyInstance=Ally(pic,name,clas,race,lvl,xp,myInv[0],x,y,grey_pic,pic,x4_pic,[myInv[1],myInv[2],myInv[3],myInv[4]],death,deathQuote,hppart,hpfull,strength,magic,skill,speed,luck,defense,resistance,move,constitution,savePictures,SWD,LNC,AXE,BOW,LGT,ELE,DRK,STF)

        if SAVESLOT == "_SAVESLOT_SUSPENDPOINT1":
            file1 = open("C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_SAVESLOT_SUSPENDPOINT1/EXTRA/_WHOMOVED.txt").read().split('\n')
        
            if str(name) in str(file1):
                all_sprites.add(allyInstance)

                addGreyAllies.append(allyInstance)

                allyInstance.picture=allyInstance.backup_grey

            else:
                all_sprites.add(allyInstance)
                ally_sprites.add(allyInstance)

            #
            

        else:
            all_sprites.add(allyInstance)
            ally_sprites.add(allyInstance)            

        if str(name)!=str("Cedrik"):
            tempALLYlist.append(allyInstance)

###################################################
    #keep this around just in case, but an older method no longer in use

    """
    #def reset():
    dictStartPos={}#
    for spot in whereDoIGo:
        dictStartPos[(spot[0],spot[1])]=False

    dictStartPos[(whereDoIGo[0][0],whereDoIGo[0][1])]=hero_to_move
    tempunitsForMap=unitsForMap[:]#.remove(hero_to_move)
    tempunitsForMap2=[]
    for item in tempunitsForMap:
        if item.name!="Cedrik":
            tempunitsForMap2.append(item)
    for who in tempunitsForMap2:
        for item in dictStartPos:
            if dictStartPos[item] is False:# and not in :
                dictStartPos[item]=who
                break

    newMap.dictStartPos=dictStartPos
    """

#######################################################
                        

    ally_sprites_no_edit=ally_sprites.copy()

    copy_ally_sprites_no_edit=ally_sprites_no_edit.copy()

    for item in addGreyAllies:
        ally_sprites_no_edit.add(item)
    for ally in ally_sprites_no_edit:
        if ally.name=="Cedrik":
            MoveWho=ally
            hero_to_move=ally
            WhoOne=ally
            break

    newMap.addGreyAllies=addGreyAllies

    """
    if SAVESLOT=="_SAVESLOT_SUSPENDPOINT1":
    """ 

    ###############################
    #if SAVESLOT == "_NEWGAME":
        #convoyDir2=[]
    #else:
    convoyDir2=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/CONVOY')#.read().split('\n')

    #just for noe testing
    #convoyDir2=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_SAVESLOT_1/CONVOY')#.read().split('\n')

    #########
    #if SAVESLOT not in ['_SAVESLOT_SUSPENDPOINT1','_NEWGAME']:
    convoyDir=[]
    for _file in convoyDir2:
        convoyDir.append(open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+str(SAVESLOT)+'/CONVOY/'+_file).read().split('\n'))
    #elif SAVESLOT == '_SAVESLOT_SUSPENDPOINT1':
        #temp



            

    convoyInventory=[]
    #for i in range(2):#get more items with for loop
    for _invItems in convoyDir:
        for item in allGear:
            check=_invItems[0]
            if str(item.name)==str(check):
                try:
                    if str(item.__class__.__name__) == "Staff":
                        invItem=Staff(item.name,item.rank,item.rang,int(_invItems[1]),int(_invItems[2]),item.addHeal,item.addXP,item.wpnType,item.value)
                    elif str(item.__class__.__name__) == "Weapon":
                        invItem=Weapon(item.name,item.rank,item.rang,int(_invItems[1]),int(_invItems[2]),item.weight,item.dmg,item.hit,item.wpnType,item.value,item.crit)
                    elif str(item.__class__.__name__) == "Item":#,"UsableItem"]:#class item
                        invItem=Item(item.name,item.value,int(_invItems[1]),int(_invItems[2]))
                    elif str(item.__class__.__name__) == "UsableItem":#,"UsableItem"]:#class item
                        #
                        for item2 in allItems:
                            if item2.name==item.name:
                                addPart3=item2.bonusWhat
                        invItem=UsableItem(item.name,item.value,int(_invItems[1]),int(_invItems[2]),str(addPart3))
                except IndexError:
                    print check,"messed up name"
                convoyInventory.append(invItem)
                break



    newMap.convoyInventory=convoyInventory




    
      
    runPath=[(MoveWho.y,MoveWho.x)]
    mov_x,mov_y = (int(hero_to_move.x-array_addx),int(hero_to_move.y-array_addy))#hero_to_move.x,hero_to_move.y

    _dialogue1=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+'_ALLMAPS/'+lines2[0]+'/1_conversation_intro')#.read().split('\n')
    _dialogue2=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+'_ALLMAPS/'+lines2[0]+'/2_conversation_intro2')
    _dialogue3=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+'_ALLMAPS/'+lines2[0]+'/4_conversation_end1')
    
    def getDialogueAndBG(_directory,_dialogue,_map):#very similar to earlier function
        #
        _directoryB=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+'_ALLMAPS/'+lines2[0]+'/1_conversation_intro')
        for _file in _directoryB:
            
            #
            lines=open(_directory+'/'+_file).read().split('\n')
            #
            if str(_file)=="MAP_BG.txt":
                if lines[0]=="Ellipse":#used for generic, but moving, background when no map is wanted or needed
                    _map=['Ellipse',lines[1]]
                else:
                    
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
                                    if getRotate is False:
                                        saveThis+=str(letter)
                                    
                                elif str(letter) == "'": #add new info

                                    if Retain is True:
                                        Retain = False
                                            
                                        ii+=1
                                        getRotate=True
                                        
                                    else:
                                        Retain=True

                            elif getRotate is True:
                                
                                if letter not in badList  and str(letter) != "," and str(letter) != " ":
                                    if str(letter)=="-" or type(int(letter))==int:
                                        saveThisRotate+=str(letter)

                                elif str(letter)==")":
                                    tempLine.append((str(saveThis),int(saveThisRotate)))

                                    getRotate=False
                                    saveThis=""
                                    saveThisRotate=""

                        temparray.append(tempLine)

                    mapWidth = len(temparray[0])
                    mapHeight = len(temparray)

                    _map=[]
                    blank_list=[]
                    
                    for row in range(mapheight):
                        blank_list=[]
                        for column in range(mapwidth):
                            myIMG=str(temparray[row][column][0])
                            my_img=pygame.image.load(myIMG)
                            my_img=pygame.transform.rotate(my_img,temparray[row][column][1])

                            blank_list.append(my_img)
                        _map.append(blank_list)

            if str(_file)=="_convo.txt":
                _dialogue=[]
                for line in lines:
                    
                    line=str(line)

                    _dialogue.append(line)

        getDialogueAndBG._dialogue=_dialogue
        getDialogueAndBG._map=_map

    conversation1=[]
    map1=[]
    getDialogueAndBG('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+'_ALLMAPS/'+lines2[0]+'/1_conversation_intro',conversation1,map1)
    convo1=getDialogueAndBG._dialogue
    map1=getDialogueAndBG._map

    conversation2=[]
    map2=[]
    getDialogueAndBG('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+'_ALLMAPS/'+lines2[0]+'/2_conversation_intro2',conversation2,map2)
    convo2=getDialogueAndBG._dialogue
    map2=getDialogueAndBG._map

    conversation3=[]
    map3=[]
    getDialogueAndBG('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+'_ALLMAPS/'+lines2[0]+'/4_conversation_end1',conversation3,map3)
    convo3=getDialogueAndBG._dialogue
    map3=getDialogueAndBG._map


    if SAVESLOT == "_SAVESLOT_SUSPENDPOINT1":#here save file is: C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/ENEMYSTART/ .....lines2[0] is PREQUEL,LEVEL1,etc
        templistENEMIES=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_SAVESLOT_SUSPENDPOINT1/ENEMIES/')
    
        listENEMIES=[]
        for _file_ in templistENEMIES:
            testFalse=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_SAVESLOT_SUSPENDPOINT1/ENEMIES/'+_file_+'/empty.txt').read().split('\n')
            if testFalse[0]=="False":
                listENEMIES.append(_file_)

    else:
                                    #below is 'C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/ENEMYSTART/'
        templistENEMIES=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/ENEMYSTART/')#+_file_+'/')
        
        listENEMIES=[]
        for _file_ in templistENEMIES:
            #listENEMIES.append(_file_)
            testFalse=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/ENEMYSTART/'+_file_+'/empty.txt').read().split('\n')
            if testFalse[0]=="False":
                listENEMIES.append(_file_)


        ###############################################################

        #if SAVESLOT == "_NEWGAME":
          #  unitsForMapFromFile=[]
         #   
        #else:
        """
        unitsForMapList=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/UNITSFORMAP')
        for item in unitsForMapList:
            personName=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+SAVESLOT+'/UNITSFORMAP/'+str(item)).read().split('\n')
            person=personName[0]

            for ally in ally_sprites_no_edit:
                if ally.name==person:
                    unitsForMap.append(ally)
        """


    #if unitsForMap==[]:
        #unitsForMap.append(hero_to_move)

        #
            
        #templistENEMIES=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_SAVESLOT_SUSPENDPOINT1/ENEMIES/')
        

        

    SOLDIERSlist=[]
    #load up the enemies for the level
    for _file in listENEMIES:
        if SAVESLOT == "_SAVESLOT_SUSPENDPOINT1":#'C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_SAVESLOT_SUSPENDPOINT1/ENEMIES/
            _main=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_SAVESLOT_SUSPENDPOINT1/ENEMIES/'+_file+'/1_.txt').read().split('\n')
        else:
            _main=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/ENEMYSTART/'+_file+'/1_.txt').read().split('\n')
  
        name=_main[0]
        CLAS=_main[1]

        #CLAS WORK
        race=_main[2]
        level=int(_main[3])
        xp=int(_main[4])
        WEAPON=_main[5]
        #RIGHTHERE
        
        x=int(_main[6])
        y=int(_main[7])
        waitOnMOVE=str(_main[8])
        if waitOnMOVE=="True":
            waitOnMove=True
        elif waitOnMOVE=="False":
            waitOnMove=False
        elif waitOnMOVE=="None":
            waitOnMove=None
            
        listOthersMove=[]#_main[9]
        listOthersMove2=[]
        
        for i in range(9,len(_main)):
            listOthersMove.append(str(_main[i])+".txt")
            listOthersMove2.append(str(_main[i]))

        for item in allGear:
            if str(item.name)==str(WEAPON):
                weapon=Weapon(item.name,item.rank,item.rang,item.uses,item.max_uses,item.weight,item.dmg,item.hit,item.wpnType,item.value,item.crit)

        #onlyEnemy=True
        for item in ENEMYCLASSES:#ALLCLASSES:
            if str(CLAS)==str(item.actualName):
                clas=item
                break
        #
        enemyInstance=Enemy(name,clas,race,level,xp,weapon,x,y,waitOnMove,listOthersMove,listOthersMove2)
        all_sprites.add(enemyInstance)
        enemy_sprites.add(enemyInstance)
        
        SOLDIERSlist.append(enemyInstance)

    #ally_sprites_no_edit=ally_sprites.copy()
    enemy_sprites_no_edit=enemy_sprites.copy()

    for enemy in enemy_sprites:#listENEMIES:
        toRename=[]
        for _file in enemy.listOthersMove: #[1_.txt,2_.txt]
            _main=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/'+'_ALLMAPS/'+lines2[0]+'/ENEMYSTART/'+_file[:-4]+'/1_.txt').read().split('\n')
            for enemy2 in enemy_sprites_no_edit:

                x=_main[6]
                y=_main[7]

                if (int(x),int(y))==(enemy2.x,enemy2.y):
                    toRename.append(enemy2)
                    
        enemy.listOthersMove=[]
        for personn in toRename:
            enemy.listOthersMove.append(personn)


    Recruitable=[]
    atNumWhat=0

    try:
        namesDir=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/RECRUITABLE/')
        for _file in namesDir:
            if str(_file)[-5]=="_":
                atNumWhat=str(_file)[0]
                Names=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/RECRUITABLE/'+_file).read().split('\n')                

                Convo=open('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/RECRUITABLE/'+atNumWhat+"_convo.txt").read().split('\n')


                for enemy in enemy_sprites_no_edit:
                    if Names[0]==enemy.name:
                        rest=[]
                        for i in range(1,len(Names)):
                            rest.append(str(Names[i]))
                        Recruitable.append((enemy,rest,Convo))
                        break
            #elif str(_file)[0]==str(atNumWhat):
    except WindowsError:
        print '-no folder for recruitable characters-'
    newMap.Recruitable=Recruitable

    
    ii=0
    Retain=False
    temparray2=[]
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
                    if getRotate is False:
                        saveThis+=str(letter)
                    
                elif str(letter) == "'": #add new info

                    if Retain is True:
                        Retain = False
                        ii+=1
                        getRotate=True
                    else:
                        Retain=True

            elif getRotate is True:
                
                if letter not in badList  and str(letter) != "," and str(letter) != " ":
                    if str(letter)=="-" or type(int(letter))==int:
                        saveThisRotate+=str(letter)

                elif str(letter)==")":
                    tempLine.append((str(saveThis),int(saveThisRotate)))

                    getRotate=False
                    saveThis=""
                    saveThisRotate=""

        temparray2.append(tempLine)

    mapWidth2 = len(temparray2[0])
    mapHeight2 = len(temparray2)

    tilemap2=[]
    blank_list2=[]

    
    for row in range(mapHeight2):
        blank_list2=[]
        for column in range(mapWidth2):
            myIMG=str(temparray2[row][column][0])
            my_img=pygame.image.load(myIMG)
            my_img=pygame.transform.rotate(my_img,temparray2[row][column][1])

            blank_list2.append(my_img)
        tilemap2.append(blank_list2)


    blueredmap2 = []
    for row in range(mapHeight2):
        new_row = []
        for column in range(mapWidth2):
            if temparray2[row][column][0] in WALSLIST:# or temparray2[row][column][0] in WATERLIST or temparray2[row][column][0] == 'tile column.png' or temparray2[row][column][0] == 'tile door2.png':
                new_row.append(1)
            else:
                new_row.append(0)
        blueredmap2.append(new_row)

    grid2 = []
    for row in blueredmap2:
        grid2.append(row)

    templistENEMIES2=os.listdir('C:/PYTHON27/FIRE_EMBLEM_SAVE_FILES/_ALLMAPS/'+lines2[0]+'/ENEMYSTART/')
    listENEMIES2=[]
    for _file_ in templistENEMIES2:
        listENEMIES2.append(_file_)

    newMap.convo1=convo1
    newMap.map1=map1

    newMap.convo2=convo2
    newMap.map2=map2

    newMap.convo3=convo3
    newMap.map3=map3

    if SAVESLOT == "_SAVESLOT_SUSPENDPOINT1":
        PlayerSignCount = 0
        PlayerPhaseDisplay = True
        PlayerCountStart = True
        DoOnceForTheirTurn = True
        TheirTurn = False
    else:
        PlayerSignCount = 0
        PlayerPhaseDisplay = False
        PlayerCountStart = False
        DoOnceForTheirTurn = True
        TheirTurn = False
    
    newMap.PlayerSignCount=PlayerSignCount
    newMap.PlayerPhaseDisplay=PlayerPhaseDisplay
    newMap.PlayerCountStart=PlayerCountStart
    newMap.DoOnceForTheirTurn=DoOnceForTheirTurn
    newMap.TheirTurn=TheirTurn
    
    newMap.CHAPTER=CHAPTER
    newMap.CHAPTERlines=CHAPTERlines
    newMap.GOLD=GOLD
    newMap.TurnNumber=TurnNumber
    newMap.GRID=GRID
    newMap.VOLUME=VOLUME
    newMap.fogOfWar=fogOfWar
    newMap.FOG=FOG
    newMap.WINCONDITIONS=WINCONDITIONS
    newMap.temparray=temparray
    newMap.mapWidth=mapWidth
    newMap.mapHeight=mapHeight
    newMap.tilemap=tilemap
    #newMap.FENCELIST=FENCELIST
    #newMap.WALSLIST=WALSLIST
    #newMap.WATERLIST=WATERLIST
    newMap.blueredmap=blueredmap
    newMap.grid=grid
    newMap.listMyChests=listMyChests
    newMap.listMyHouses=listMyHouses
    newMap.all_sprites=all_sprites
    newMap.ally_sprites=ally_sprites
    newMap.ally_sprites_no_edit=ally_sprites_no_edit
    newMap.copy_ally_sprites_no_edit=copy_ally_sprites_no_edit
    newMap.enemy_sprites=enemy_sprites
    newMap.enemy_sprites_no_edit=enemy_sprites_no_edit

    newMap.neutral_sprites=neutral_sprites
    newMap.neutral_sprites_no_edit=neutral_sprites_no_edit
    newMap.copy_neutral_sprites_no_edit=copy_neutral_sprites_no_edit
    
    newMap.SOLDIERSlist=SOLDIERSlist
    newMap.MoveWho=MoveWho
    newMap.hero_to_move=hero_to_move
    newMap.mov_x=mov_x
    newMap.mov_y=mov_y

    newMap.allowedUnits=allowedUnits
    newMap.whereDoIGo=whereDoIGo

    #saveAccessed=checkSaveFile[_slots_count]
    #_slots_count=0

    newMap.saveAccessed=checkSaveFile[_slots_count]

    newMap._slots_count=_slots_count

    #EndChapter
