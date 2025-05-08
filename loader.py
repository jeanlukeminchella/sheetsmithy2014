import globalFunctions as gf
import json
import os

def encode_to_file(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file,indent=4)

spell = {
    "title":"Hellish Rebuke ",
    "damage":"",
    "rang":60,
    "cost":"",
    "duration":"10 min",
    "conc":True,
    "modiferIndex":5,
    "preSaveNormalText":"A creature that just damaged you takes 3d10 fire damage. DEX",
    "postSaveNormalText":" to half damage.",
    "preSaveItalicText":"One use per Long Rest - </em>O<em> (Tiefling)",
    "postSaveItalicText":"",
    "castTime":"r",
    "ritual":False
}

spellName = "tieflingRebuke.txt"

#encode_to_file(spell,"./Spells/"+spellName)

attack = {
    "title":"Dagger",
    "damage":"d4",
    "rang":20,
    "cost":"",
    "duration":"",
    "conc":False,
    "addModToDamage":True,
    "damageType":None,
    "forcedMod":-1,
    "cantripScaling":False,
    "saveNotAttack":False,
    "resistAttributeText":"",
    "resistText":"",
    "note":""
}
attackName = "dagger.txt"
#encode_to_file(attack,"./AttackRolls/"+attackName)

modifiers = [3,2,2,0,0,0]
profs = [1,2,3]

classesToIterate = ["Fighter","Rogue","Cleric","Paladin","Barbarian","Ranger","Monk"]
levelsToIterate = [3]
#

#classesToIterate = []
#levelsToIterate = []
c = [None]*20


for l in levelsToIterate:
    
    for cl in classesToIterate:
        
    
        seed = {
            "level" : l,
            "classAsString":cl,
            "tashaContent" : True,
            "choices" : c,
            "showScores":True
            }

#seed[choices][1]="defence"

        seedName = cl+str(l)+".txt"
    
    
        encode_to_file(seed,"./Seeds/"+seedName)

armorsToEncode = [["Studded Leather",13,True,False,"Light",False],["Leather",12,True,False,"Light",False], ["Chain Shirt",13,True,False,"Medium",True], ["Breastplate",14,True,False,"Medium",True], ["Hide",12,True,False,"Medium",True], ["Half Plate",15,True,True,"Medium",True],["Scale Mail",14,True,True,"Medium",True], ["Chain Mail",16,False,True,"Heavy",False], ["Splint",17,False,True,"Heavy",False], ["Ring Mail",14,False,True,"Heavy",False], ["Plate",18,False,True,"Heavy",False]]
armorsToEncode = []

for a in armorsToEncode:
    
    armor = {
        "name": a[0],
        "base":a[1],
        "addDex":a[2],
        "stealthDisadvantage":a[3],
        "category":a[4],
        "maxTwo":a[5]
    }
    
    encode_to_file(armor,"./Armors/"+a[0]+".txt")
    
heal = {
    "title":"Healing Word",
    "damage":"",
    "rang":60,
    "cost":"1",
    "duration":"",
    "conc":False,
    "preHealText":"Heal a target d4",
    "postHealText":" hp",
    "modiferIndex":-1,
    "castTime":"ba",
    "ritual":False
}

healName = "healingWord.txt"

#encode_to_file(heal,"./Heals/"+healName)

