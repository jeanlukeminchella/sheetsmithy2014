import featFunctions as feat
import globalFunctions as gf
import Entry as entry

sizeInfoString = gf.infoBullet + "Size: "
mediumString = "Medium"
smallString = "Small"

# we need darkvision everywhere

# ok to be a v human were looking for "human?feat-FEAT?attBoost-ATTRIBUTE?attBoost-ATTRIBUTE" and ATTRIBUTE has to be an int from 0 to 5
def human(c, args=[]):
    
    c.size="Medium"
    varHuman = False
    assignedBonuses = False
    c.speed = 30
    c.raceString = "Human"
    for a in args:
        if "feat-" in a:
            # uncivilised
            
            
            x = a.split("-")
            if x[1] in feat.featFunctions.keys():
                feat.featFunctions[x[1]](c)
                varHuman = True
            else:
                print("sorry that feat was not accepted", x[1])
        elif "attBoost1-" in a:
            x = a.split("-")
            attBoost1 = None
            try:
                attBoost1 = int(x[1])
                if not attBoost1 in range(5):
                    raise ValueError
                varHuman = True
                c.scores[attBoost1]+=1
                assignedBonuses = True
            except:
                print("ok i just tried to make this an int and it failed ",x[1])
        elif "attBoost2-" in a:
            x = a.split("-")
            attBoost2 = None
            try:
                attBoost2 = int(x[1])
                if not attBoost2 in range(5):
                    raise ValueError
                varHuman = True
                c.scores[attBoost2]+=1
                assignedBonuses = True
            except:
                print("ok i just tried to make this an int and it failed ",x[1])
                
    if varHuman and not assignedBonuses:
        
        #print("scores are ", c.scores, "for class ",c.classAsString)
        x = gf.chooseAttributesToIncreaseBy(c,1)[0]
        #print("weve chosen to increase", x)
        c.scores[x]+=1
        
        #print("scores are ", c.scores)
        x = gf.chooseAttributesToIncreaseBy(c,1)[0]
        #print("weve chosen to increase", x)
        c.scores[x]+=1
        
        #print("scores are ", c.scores)
        #print()
        
        
    if not varHuman:
        # this is a standard human
        for i in range(len(c.scores)):
            c.scores[i]+=1
    c.updateModifiers()
    print("c.hitDie,c.level,c.modifiers[2] is ",c.hitDie,c.level,c.modifiers[2])
    c.hp = c.getHp(c.hitDie,c.level,c.modifiers[2])
    print("c.hitDie,c.level,c.modifiers[2] is ",c.hitDie,c.level,c.modifiers[2])
    

# we need darkness and thaumaturgy here
def tiefling(c, arg=[]):
    
    c.size="Medium"
    c.raceString = "Tiefling"
    c.charInfos.append(entry.TextEntry("resFire"))
    if c.level>2:
        c.reactions.append(entry.SpellEntry("tieflingRebuke"))
    c.speed = 30
    gf.addScoreBonuses(c,arg,[0,0,0,1,0,2])
   
def halfling(c, arg=[]):
    
    c.size="Small"
    c.charInfos.append(entry.TextEntry("lucky"))
    c.charInfos.append(entry.TextEntry("haflingNimbleness"))
    c.saveNotes.append([4,"(adv. vs frightened)"])
    c.raceString = "Halfling"
    c.speed = 25

    subraces = ["stout", "lightfoot"]
    subrace = findSubrace(arg,subraces)


    if subrace == "stout":
        c.raceString = "Halfling (Stout)"
        c.addResistance("Poison")
        c.saveNotes.append([2,"(adv. vs poison)"])
        gf.addScoreBonuses(c,arg,[0,2,1,0,0,0])
        
    elif subrace == "lightfoot":
        c.raceString = "Halfling (Lightfoot)"
        c.charInfos.append(entry.TextEntry("naturallyStealthy"))
        gf.addScoreBonuses(c,arg,[0,2,0,0,0,1])

# add stonecunning
def dwarf(c, arg=[]):
    
    c.size="Small"
    c.raceString = "Dwarf"
    c.speed = 25

    subraces = ["hill", "mountain"]
    subrace = findSubrace(arg,subraces)

    c.addResistance("Poison")
    c.saveNotes.append([2,"(adv. vs poison)"])

    if subrace == "hill":
        c.raceString = "Dwarf (Hill)"
        gf.addScoreBonuses(c,arg,[0,0,2,0,1,0])
        c.hpBoost+=c.level
        c.hp = c.getHp(c.hitDie,c.level,c.modifiers[2])
        
    elif subrace == "mountain":
        c.raceString = "Dwarf (Mountain)"
        c.charInfos.append(entry.TextEntry("naturallyStealthy"))
        gf.addScoreBonuses(c,arg,[2,0,2,0,0,0])
       
    # needs work (?)
def halfOrc(c,arg=[]):
    
    c.raceString = "Half-Orc"
    c.charInfos.append(entry.TextEntry("savageAttacks"))
    c.charInfos.append(entry.TextEntry("relentlessEndurance"))
    c.size="Medium"
    c.speed = 30
    
    gf.addScoreBonuses(c,arg,[2,0,1,0,0,0])
    
    if not 7 in c.skillProficiencies:
        c.skillProficiencies.append(7)

# we need rock gnomes tinkering
def gnome(c, arg=[]):

    
    c.size="Small"
    c.saveNotes.append([4,"(adv. vs magic)"])
    c.saveNotes.append([3,"(adv. vs magic)"])
    c.saveNotes.append([5,"(adv. vs magic)"])
    c.raceString = "Gnome"
    c.speed = 25

    subraces = ["forest", "rock"]
    subrace = findSubrace(arg,subraces)

    

    if subrace == "forest":
        c.raceString = "Gnome (Forest)"
        c.charInfos.append(entry.Entry("You can communicate simple ideas with Small or smaller beasts. <em>(Forest Gnome)</em>"))
        gf.addScoreBonuses(c,arg,[0,1,0,2,0,0])
    elif subrace == "rock":
        c.raceString = "Gnome (Rock)"   
        gf.addScoreBonuses(c,arg,[0,0,1,2,0,0])
    
        
def dragonborn(c,arg=[]):
    
    c.size="Medium"
    c.speed = 30
    
    gf.addScoreBonuses(c,arg,[2,0,0,0,0,1])
    
    
    subraces = ["Black","Blue","Brass","Bronze","Copper","Gold","Green","Red","Silver","White"]
    subrace = findSubrace(arg,subraces)
    
    dragons = {
        subraces[0]:["30ft line","acid","DEX"],
        subraces[1]:["30ft line","lightning","DEX"],
        subraces[2]:["30ft line","fire","DEX"],
        subraces[3]:["30ft line","lightning","DEX"],
        subraces[4]:["30ft line","acid","DEX"],
        subraces[5]:["15ft cone","fire","DEX"],
        subraces[6]:["15ft cone","poison","CON"],
        subraces[7]:["15ft cone","fire","DEX"],
        subraces[8]:["15ft cone","cold","CON"],
        subraces[9]:["15ft cone","cold","CON"]
        

    }
    
    typeDetails = dragons[subrace]
    shape = typeDetails[0]
    damage = typeDetails[1]
    save = typeDetails[2]

    
    c.raceString = "Dragonborn ("+subrace+")"
    
    damageAmount = "2d6"
    
    if c.level>5:
        damageAmount = "3d6"
        
    c.addResistance(damage)
        
    breath = entry.SpellEntry("blank")
    breath.title = "Breath Weapon"
    breath.preSaveNormalText = "Unleash a "+shape+" of "+damage+". "+damageAmount+" damage, "+save
    breath.postSaveNormalText = " to half damage."
    breath.preSaveItalicText = " Recharges after a Short Rest - </em>O<em>"
    breath.modiferIndex=2
    c.actionEntries.append(breath)
    
def elf(c,arg=[]):
    
    c.size="Medium"
    c.raceString = "Elf "
    c.speed = 30
    
    subraces = ["high","drow","wood"]
    subrace = findSubrace(arg,subraces)
    
    c.saveNotes.append([4,"(adv. vs charmed)"])
    c.charInfos.append(entry.Entry("Magic cannot put you to sleep <em>(Elf)</em>"))
    
    if not 14 in c.skillProficiencies:
        c.skillProficiencies.append(14)
    
    if subrace == subraces[0]:
        c.raceString += "(High)"
        gf.addScoreBonuses(c,arg,[0,2,0,1,0,0])
    elif subrace == subraces[1]:
        c.raceString += "(Drow)"
        gf.addScoreBonuses(c,arg,[0,2,0,0,0,1])
    
    elif subrace == subraces[2]:
        c.raceString += "(Wood)"
        gf.addScoreBonuses(c,arg,[0,2,0,0,1,0])
        c.speed+=5
        c.charInfos.append(entry.TextEntry("maskOfWild"))
    
    
def halfElf(c,arg=[]):
    
    
    c.size="Medium"
    c.raceString = "Half-Elf "
    c.speed = 30
    
    c.skillProficiencies.append(c.pickSkillProficiency(list(range(17))))
    c.skillProficiencies.append(c.pickSkillProficiency(list(range(17))))
    print()
    print("scores before half elf added ", c.scores)
    
    # l is the list that of how much each scores were increased by. 
    l = gf.addScoreBonuses(c,arg,[0,0,0,0,0,2])
    
    print("we added our +2 from being a half elf like this ",l)
    
    # ok lets find out which attribute was increased, default is 5 of course
    # i is the index of the attribute increased
    i = 5
    if 2 in l:
        i=l.index(2)
    else:
        print("error - half elf +2 bonus has gone arwyry")
    
    if 1 in l:
        #ok great the input has added the +1s thats great
        pass
    else:
        p = c.attributePriorityList[:]
    
        # we cant add our plus ones to the same attribute as our +2, so remove it from priorities
        p.remove(i)
        
        print("p is ",p)
        
        a = gf.chooseAttributesToIncreaseBy(c,1, False, p)[0]
        print("were gonna add a +1 here ",a)
        c.scores[a]+=1
        p.remove(a)
        
        print("p is ",p)
        b = gf.chooseAttributesToIncreaseBy(c,1, False, p)[0]
        print("were gonna add a +1 here  ",b)
        c.scores[b]+=1
    

    
    
def findSubrace(arg, subraces):
    subrace = ""
    for a in arg:
        if "subrace-" in a:
            x = a.split("-")
            if x[1] in subraces:
                subrace = x[1]
    if subrace == "":
        subrace = subraces[0]
    return subrace
    
races = {
    "human":human,
    "dwarf":dwarf,
    "tiefling":tiefling,
    "halfling":halfling,
    "halfOrc":halfOrc,
    "gnome":gnome,
    "dragonborn":dragonborn,
    "halfElf":halfElf
}

