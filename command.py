import Input as inpc
from Classes import Barbarian as barb
from Classes import Fighter as fighter
from Classes import Rogue as rogue
from Classes import Monk as monk
from Classes import Ranger as ranger
from Classes import Paladin as pal
from Classes import Cleric as cleric
import datetime
import os
import webbrowser
import shutil
import json

pathToLoad = "file:///media/fuse/crostini_c198dff15dfd992cb319b5ca255e286f9ff04409_termina_penguin/2014%20Character%20Generator/Generated/"


def generateClass(inp):
    
    c = inp.classAsString
    
    b = None
    
    if c=="Fighter":
        b = fighter.Fighter(inp)
    elif c=="Rogue":
        b = rogue.Rogue(inp)
    elif c=="Monk":
        b = monk.Monk(inp)
    elif c=="Barbarian":
        b = barb.Barbarian(inp)
    elif c=="Ranger":
        b = ranger.Ranger(inp)
    elif c=="Paladin":
        b = pal.Paladin(inp)
    elif c=="Cleric":
        b = cleric.Cleric(inp)
    else:
        print("we could not place that class name sorry")
        
    #blockSample = barb.sh.bl.TextActionBlock(1, ["Dash"],"","attack01")
    
    #b.addBlock(blockSample)
    
    
    return (b.generateClassHTML())
    
    
    
    
def getTimeAsString():
    result = ""
    x= datetime.datetime.now()
    result += x.strftime("%y")
    result += "-"+x.strftime("%m")
    result += "-"+x.strftime("%d")
    result += "-"+x.strftime("%H")
    result += "-"+x.strftime("%M")
    result += "-"+x.strftime("%S")
    return result
    
    

def getFileNameForThisClass(title, level):
    return title+str(level)+".html"

level = 4




#seedsToGo = [rangerSeed,rogueSeed,fighterSeed,barbarianSeed,paladinSeed]
#seedsToGo = [cl]
seedsToGo = os.listdir(barb.sh.gf.pathToSource+"Seeds")

fileExtension = ".txt"

def growSeeds (seeds):
    
    
    folderName = getTimeAsString()
    os.mkdir(barb.sh.gf.pathToSource+"Generated/"+folderName)
    shutil.copy(barb.sh.gf.pathToSource+"bkg01.jpg", barb.sh.gf.pathToSource+"Generated/"+folderName)
    os.chdir(barb.sh.gf.pathToSource+"Generated/"+folderName)
    
    for seed in seeds:
        
        d={}
        
        with open("../../Seeds/"+seed, 'r') as file:
            d = json.load(file)
        
        i = inpc.Input(d["level"],d["classAsString"])
        
        commandTuples = []
        
        for k in d.keys():
           i.changeAttribute(k,d[k])
            
        
        text = generateClass(i)
        fileName = getFileNameForThisClass(i.classAsString,i.level)
        f = open(fileName,"w")
        f.write(text)
        f.close()
        
        webbrowser.open(pathToLoad+folderName+"/"+fileName)
    
    os.chdir("../../")

#growSeeds(seedsToGo)