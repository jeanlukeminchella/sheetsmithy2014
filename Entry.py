import globalFunctions as gf
import json
import os

fileExtension = ".txt"

standardEntryStart = "<p>"
standardEntryEnd = "</p>\n"

# this needs consolidating a lot

# self.folderName needs defining to load a codename
class Entry():
    
    # datum could be loads of data types  - depends on type of entry)
    def __init__(self, datum):
        self.datum=datum
        
    # if not a specific type of entry, just returns datum as flat text
    def getHTML(self, c=None):
        t = getThrupleFromFlatText(self.datum)
        return getHTMLfromThruple(t)
        
    def applyCommand(self,commandWord,result):
        if commandWord=="title":
            self.title=result
        elif commandWord=="damage":
            self.damage=result
        elif commandWord=="rang":
            self.rang=result
        elif commandWord=="cost":
            self.cost=result
        elif commandWord=="duration":
            self.duration=result
        elif commandWord=="conc":
            self.conc=result
        elif commandWord=="addModToDamage":
            self.addModToDamage=result
        elif commandWord=="damageType":
            self.damageType=result
        elif commandWord=="forcedMod":
            self.forcedMod=result
        elif commandWord=="cantripScaling":
            self.cantripScaling=result
        elif commandWord=="saveNotAttack":
            self.saveNotAttack=result
        elif commandWord=="resistAttributeText":
            self.resistAttributeText=result
        elif commandWord=="resistText":
            self.resistText=result
        elif commandWord=="note":
            self.note=result
        elif commandWord=="castTime":
            self.castTime=result
        elif commandWord=="ritual":
            self.ritual=result
        elif commandWord=="modiferIndex":
            self.modiferIndex=result
        elif commandWord=="castTime":
            self.castTime=result
        elif commandWord=="ritual":
            self.ritual=result
            
        elif commandWord=="preSaveNormalText":
            self.preSaveNormalText=result
        elif commandWord=="postSaveNormalText":
            self.postSaveNormalText=result
        elif commandWord=="preSaveItalicText":
            self.preSaveItalicText=result
        elif commandWord=="postSaveItalicText":
            self.postSaveItalicText=result
            
        elif commandWord=="preHealText":
            self.preHealText=result
        elif commandWord=="postHealText":
            self.postHealText=result


    def applyCommandList(self,commandList):
        for command in commandList:
            self.applyCommand(command[0],command[1])
            
    def loadCodeName(self,codeName):
        
        d= {}
        
        with open(gf.pathToSource+""+self.folderName+"/"+codeName+fileExtension, 'r') as file:
            d = json.load(file)
            
        commandTuples = []
        
        for k in d.keys():
            commandTuples.append([k,d[k]])
            
        self.applyCommandList(commandTuples)
    
# this has a bold bit, normal bit then italicised bit, and is static (is not affected by character at all)
class TextEntry(Entry):
    
    def __init__(self, datum):
        self.datum=datum
        with open(gf.pathToSource+"TextEntries.txt", 'r') as file:
            self.textEntryDictionary = json.load(file)
        
    def getHTML(self,c=None):
        thruple = self.textEntryDictionary[self.datum]
        return getHTMLfromThruple(thruple)

# this is best for attacks and spell attacks with roll to hit then damage dice
class AttackRollEntry(Entry):
    
    def __init__(self, datum):
        self.title=""
        self.damage=""
        self.rang=0
        self.cost=""
        self.duration=""
        self.conc=False
        self.addModToDamage=False
        self.damageType=None
        self.forcedMod=-1
        self.cantripScaling=False
        self.saveNotAttack=False
        self.resistAttributeText=""
        self.resistText=""
        self.note=""
        self.datum=datum
        self.castTime="a"
        self.ritual=False
        
        self.folderName = "AttackRolls"
        self.loadCodeName(datum)
        
    def getHTML(self,c):
        
        result = ""
        
        thruple = self.attackGetThruple(c)
        return getHTMLfromThruple(thruple)
        
        # note is un actioned
    def attackGetThruple(self, c):
        name = self.title
        boldBit = name
        #consolidate?
        if self.rang > 0 or self.duration!="" or self.cost!="":
            boldBit+=" ("
            prior = False
            if self.rang>0 :
                boldBit+=gf.getDistanceString(self.rang)
                prior = True
            if self.duration!="":
                if prior:
                    boldBit+=", "
                    prior = True
                boldBit+= self.duration
            if self.cost!="":
                if prior:
                    boldBit+=", "
                    prior = True
                boldBit+= str(c.costDic[str(self.cost)])
            boldBit+=")"
       
        if self.conc:
            boldBit+=" ©. "
        else:
            boldBit+=". "
        
        normalBit = ""
        
        attributeModifier = c.modifiers[c.defaultMod]
        if self.forcedMod!=-1:
            attributeModifier=c.modifiers[self.forcedMod]
        
        dmgString = self.damage
        if self.cantripScaling:
            #needs a fix
            pre = int(c.level/5)
            if pre>0:
                dmgString = str(pre+1)+dmgString
        if self.addModToDamage:
            dmgString += gf.getSignedStringFromInt(attributeModifier,True)
        
        if self.damageType is not None:
            dmgString+=" "+damageType
        dmgString+=" damage"
        
        if not self.saveNotAttack:
            normalBit+="d20"+gf.getSignedStringFromInt(attributeModifier+c.profBonus)+" to hit, "
            normalBit+=dmgString+"."
        else:
            normalBit+=dmgString+", "
            normalBit+=self.resistAttributeText+str(8+attributeModifier+c.profBonus)+self.resistText+"."
        
        italicBit = self.note
        
        return [boldBit,normalBit,italicBit]


    

class SpellEntry(Entry):
    
    def __init__(self, datum):
        self.title=""
        self.damage=""
        self.rang=0
        self.cost=""
        self.duration=""
        self.conc=False
        self.modiferIndex=-1
        self.preSaveNormalText=""
        self.postSaveNormalText=""
        self.preSaveItalicText=""
        self.postSaveItalicText=""
        self.castTime="a"
        self.ritual=False
        
        self.datum=datum
        self.folderName = "Spells"
        self.loadCodeName(datum)
    
    def getHTML(self,c):
        
        modifier = c.modifiers[c.defaultMod]
        if self.modiferIndex>-1:
            modifier = c.modifiers[self.modiferIndex]
        
        #consolidate maybe
        boldBit = self.title
        if self.rang > 0 or self.duration!="" or self.cost!="":
            boldBit+=" ("
            prior = False
            if self.rang>0 :
                boldBit+=gf.getDistanceString(self.rang)
                prior = True
            if self.duration!="":
                if prior:
                    boldBit+=", "
                prior = True
                boldBit+= self.duration
            if self.cost!="":
                if prior:
                    boldBit+=", "
                prior = True
                boldBit+= str(c.costDic[self.cost])
            boldBit+=")"
       
        if self.conc:
            boldBit+=" ©. "
        else:
            boldBit+=". "
        
        normalBit = self.preSaveNormalText
        if self.postSaveNormalText!="":
            
            normalBit += str(8+c.profBonus+modifier)
            normalBit += self.postSaveNormalText
            
        
        italicBit = self.preSaveItalicText
        if self.postSaveItalicText!="":
            
            italicBit += str(8+c.profBonus+modifier)
            italicBit += self.postSaveItalicText
            
        if self.ritual and c.ritualCaster:
            italicBit += "</em> ⌆<em>"
        
        return getHTMLfromThruple([boldBit,normalBit,italicBit])
        

class HealingEntry(Entry):
    
    def __init__(self, datum):
        self.title=""
        
        self.rang=0
        self.cost=""
        self.duration=""
        self.conc=False
        self.modifierIndex=-1
        self.preHealText=""
        
        self.postHealText=""
        self.castTime="a"
        self.ritual=False
        
        self.datum=datum
        self.folderName = "Heals"
        self.loadCodeName(datum)
        
        self.healingBonus = 0
            
    def getHTML(self,c):
        
        
        modifier = c.modifiers[c.defaultMod]
        if self.modifierIndex>-1:
            modifier = c.modifiers[self.modifierIndex]
        
        
        
        #consolidate maybe
        boldBit = self.title
        if self.rang > 0 or self.duration!="" or self.cost!="":
            boldBit+=" ("
            prior = False
            if self.rang>0 :
                boldBit+=gf.getDistanceString(self.rang)
                prior = True
            if self.duration!="":
                if prior:
                    boldBit+=", "
                prior = True
                boldBit+= self.duration
            if self.cost!="":
                if prior:
                    boldBit+=", "
                prior = True
                boldBit+= str(c.costDic[self.cost])
            boldBit+=")"
       
        if self.conc:
            boldBit+=" ©. "
        else:
            boldBit+=". "
        
        normalBit = self.preHealText
        if self.postHealText!="":
            
            normalBit += str(gf.getSignedStringFromInt(modifier+self.healingBonus))
            normalBit += self.postHealText
            
        italicBit = ""
            
        if self.ritual and c.ritualCaster:
            italicBit += "</em> ⌆<em>"
        
        return getHTMLfromThruple([boldBit,normalBit,italicBit])

def getThrupleFromFlatText(text):
    return ["",text,""]

def getHTMLfromThruple(thruple):
    boldBit = thruple[0]
    normalBit = thruple[1]
    italicBit = thruple[2]
    result = standardEntryStart
    if boldBit!= "":
        result+="<strong>"+boldBit+"</strong> "
    
    if normalBit!= "":
        result+=normalBit+" "
    
    
    if italicBit!= "":
        result+="<em>"+italicBit+"</em>"
        
    return result+standardEntryEnd
        

class Block():
    
    def __init__(self, entries=[], title="",divID=""):
        self.entries = entries
        self.title=title
        self.divID=divID
    
    def addEntry(self, e):
        self.entries.append(e)
        
    def getHTML(self,c=None):
        
        result = ""
        if self.title !="":
            result += "<div id='sectionTitle'>"+self.title+"</div>\n"
            
        if self.divID !="":
            result += "<div id='"+self.divID+"'>\n"
            
        for e in self.entries:
            result += e.getHTML(c)
        
        if self.divID !="":
            result += "</div>\n"
        
        return result
   
