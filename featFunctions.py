import Entry as bl
import globalFunctions as gf

def addStr(c):
    c.scores[0]=c.scores[0]+2
    c.updateModifiers()

# an automated booster that chooses the scores to boost for the player
def boostScores(c):
    x = gf.chooseAttributesToIncreaseBy(c,2)
    c.scores[x[0]]+=1
    c.scores[x[1]]+=1
    c.updateModifiers()

def addDex(c):
    c.scores[1]=c.scores[1]+2
    c.updateModifiers()
    
    
def addCon(c):
    
    c.scores[2]=c.scores[2]+2
    c.updateModifiers()
    
    
def addInt(c):
    
    c.scores[3]=c.scores[3]+2
    c.updateModifiers()
    
    
def addWis(c):
    
    c.scores[4]=c.scores[4]+2
    c.updateModifiers()
    
    
def addCha(c):
    
    c.scores[5]=c.scores[5]+2
    c.updateModifiers()
    
def greatWeaponMaster(c):
    
    class HeavyWeaponEntry(bl.Entry):
        def getHTML(self,c):
            boldBit = "Headshot. "
            middleBit = "d20"
            
            attackMod = c.modifiers[0]+c.profBonus-5
            middleBit+=bl.gf.getSignedStringFromInt(attackMod,True)
            middleBit+=" to hit, 2d6"
            middleBit+=bl.gf.getSignedStringFromInt(c.modifiers[0]+10,True)
            middleBit+=" damage."
            
            thruple = [boldBit,middleBit,""]
            
            return bl.getHTMLfromThruple(thruple)
    e = HeavyWeaponEntry(" ")
    c.highlightedEntries.insert(1,e)
    
    c.charInfos.append(bl.Entry("• Critical Hits and Knockouts allow an attack as a Bonus Action."))
            
            
def defenceFightStyle(c):
    c.cumulativeACBonus=c.cumulativeACBonus+1
            
featFunctions = {
    "addStr":addStr,
    "addDex":addDex,
    "addCon":addCon,
    "addInt":addInt,
    "addWis":addWis,
    "addCha":addCha,
    "boostScores":boostScores,
    "defence":defenceFightStyle,
    "gwm":greatWeaponMaster
}
