from flask import Flask, redirect, render_template, request, url_for

from Classes import Barbarian as barb
from Classes import Fighter as fighter
from Classes import Rogue as rogue
from Classes import Monk as monk
from Classes import Ranger as ranger
from Classes import Paladin as pal
from Classes import Cleric as cleric
import Class as Sheet
import Input

app = Flask(__name__)

def getHTMLFromInput(d):

    inp = {
        "classAsString":"",
        "scores" : None,
        "race":None,
        "showScores" : False,
        "backgroundAsString":"",
        "choices" : [None]*20,
        "name":"",
        "level":1,
        "showScores" : False,
        "tashaContent" : False
    }

    for key in d.keys():
        inp[key]=d[key]

    race = inp["race"]


    c = inp["classAsString"]
    
    i = Input.Input(d["level"],d["classAsString"])
        
    commandTuples = []
    
    for k in d.keys():
        i.changeAttribute(k,d[k])

    inp = i

    character = None

    if c=="Fighter":
        character = fighter.Fighter(inp)
    elif c=="Rogue":
        character = rogue.Rogue(inp)
    elif c=="Monk":
        character = monk.Monk(inp)
    elif c=="Barbarian":
        character = barb.Barbarian(inp)
    elif c=="Ranger":
        character = ranger.Ranger(inp)
    elif c=="Paladin":
        character = pal.Paladin(inp)
    elif c=="Cleric":
        character = cleric.Cleric(inp)
    else:

        inp["classAsString"]="Fighter"
        character = fighter.Fighter(inp)

    return(character.generateClassHTML())


@app.route('/generate')
def makeSheet():
    d = request.args
    print()
    print("This is what we got from the request: ")
    print(d)
    
    # changing form values into one thats readable by the generator
    # this needs to be resilient to bad  requests as well

    keys = d.keys()
    inp = {}
    
    try:
        inp["level"] = int(d["level"])
    except:
        pass
        #print("issue loading / parsing level from input")
    
    try:
        inp["classAsString"] = str(d["classAsString"])
    except:
        pass
        #print("issue loading / parsing class from input")

    if "backgroundAsString" in keys:
        inp["backgroundAsString"]=d["backgroundAsString"]
    if "race" in keys:
        inp["race"]=d["race"]
    
    bools = ["tashaContent","showScores"]
    for i in range(len(bools)):
        if bools[i] in keys:
            inp[bools[i]] = bool(d[bools[i]])
    if "name" in keys:
        if d["name"]:
            inp["name"] = d["name"]
    

    choicesDic = [None]*20



    possibleFeatChoices = ["fightStyle","l4-feat"]

    for choice in possibleFeatChoices:

        if choice in keys:
            if d[choice]!="" and d[choice] in barb.c.feats.Feats.keys():
                choicesDic[choice]=d[choice]

    try:
        if inp["classAsString"]=="Barbarian":
            choicesDic[3]=d["barbarianSubclass"]
        if inp["classAsString"]=="Monk":
            choicesDic[3]=d["monkSubclass"]
        if inp["classAsString"]=="Paladin":
            choicesDic[3]=d["paladinSubclass"]
        if inp["classAsString"]=="Fighter":
            choicesDic[3]=d["fighterSubclass"]
            choicesDic[6]=d["l6-feat"]
        if inp["classAsString"]=="Rogue":
            choicesDic[3]=d["rogueSubclass"]
        if inp["classAsString"]=="Ranger":
            choicesDic[3]=d["rangerSubclass"]
        if inp["classAsString"]=="Cleric":
            choicesDic[3]=d["clericSubclass"]
    except:
        pass
        print("issue handling subclass")  

    inp["choices"]=choicesDic

    

    attributes =  ["str","dex","con","int","wis","cha"]
    scores = []
    userHasChosenAScore = False
    try:

        for a in attributes:
            chosenScore = d[a]
            if chosenScore == "":
                scores.append(10)
            else:
                scores.append(int(chosenScore))
                userHasChosenAScore = True
        if userHasChosenAScore:
            inp["scores"]=scores
    except:
        pass
        #print("issue picking scores") 
    
    if "seed" in keys:
        inp["seed"]=int(d["seed"])
        
    print()
    print("This is what were sending to the code: ")
    print(inp)
    print()
    return getHTMLFromInput(inp)

@app.route('/')
def landingPad():
    return render_template("index.html")

