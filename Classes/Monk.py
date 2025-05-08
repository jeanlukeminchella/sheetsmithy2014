import Class as sh
import featFunctions as feats

class Monk(sh.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 8
        self.saveProficiencies = [0,1]
        self.defaultMod = 1
        
        self.loadScoresAndMods([10,15,13,10,14,10],inp)
        self.attributePriorityList = [1,2,4,5,0,3]
        super().__init__(inp)
        level = self.level
        
        
        
        
        
        evasiveMoveLabel="Evasive Action."
        evasiveMoveTitle="EVASIVE ACTIONS"

        self.actionEntries.append(sh.bl.TextEntry("Hide"))
        self.actionEntries.append(sh.bl.TextEntry("useObject"))
        self.highlightedEntries.append(sh.bl.AttackRollEntry("quarterstaff"))
        self.highlightedEntries.append(sh.bl.AttackRollEntry("shortbow"))
        self.highlightedEntries.append(sh.bl.AttackRollEntry("dart"))

        
        
        
        
        if self.stuff =="":
            self.stuff="Robes, quarterstaff, shortbow, quiver, rations x10, 50ft rope"
            
        # some subclass features mean the flurry of blows have an asterisk
        flurryOfBlowsAstricks = False
        
        
        e = sh.bl.AttackRollEntry("punch")
        e.damage = getMartialArtsDie(self.level)
        self.highlightedEntries.append(e)
        
        offHandEntry = sh.bl.TextEntry("offhandPunchLevel1")
        if inp.level>1:
            offHandEntry = sh.bl.TextEntry("offhandPunch")
            
        self.bonusActionEntries.append(offHandEntry)
        
        subclassChoice = None
        #right lets level this shit UP
        
        if level>1:
            
            commandsToFishOut = ["Dash","Disengage","Dodge"]
            indiciesToFishOut = []
            
            for i in range(len(self.actionEntries)):
                if self.actionEntries[i].datum in commandsToFishOut:
                    indiciesToFishOut.append(i)
                   
            fishedOutCount = 0
            for index in indiciesToFishOut:
                self.actionEntries.pop(index-fishedOutCount)
                fishedOutCount=fishedOutCount+1
            
            
            evasiveMoveEntry = sh.bl.Entry("<strong>"+evasiveMoveLabel+"</strong>")
            self.actionEntries.append(evasiveMoveEntry)
            evasiveMoveEntry = sh.bl.Entry("<strong>"+evasiveMoveLabel+" (1 ki).</strong>")
            self.bonusActionEntries.append(evasiveMoveEntry)
            
            evasiveMoves = []
            evasiveMoves.append(sh.bl.TextEntry("Dash"))
            evasiveMoves.append(sh.bl.TextEntry("Disengage"))
            evasiveMoves.append(sh.bl.TextEntry("Dodge"))
            evasiveBlock=sh.bl.Block(evasiveMoves,evasiveMoveTitle)
            self.rightColumnBlocks.append(evasiveBlock)
            
            # ki block is initalised here so sublass & levelling can affect it
            kiEntry = sh.bl.Entry("<strong>Ki -</strong> "+(" O"*(level)))
            kiTag = sh.bl.Entry("<em>You regain all Ki after a rest.</em> ")
            kiBlock = sh.bl.Block([kiEntry,kiTag],"KI")
            
            self.speed+=getSpeedBonus(self.level)
            
            
        if level>2:
            
            #Deflect Missile. When hit with a ranged attack, you may deflect 2d6+4 damage. For 1 ki, hurl missile as a Dart if damage reduced to zero.
            
            class DeflectMissileEntry(sh.bl.Entry):
                def getHTML(self,c):
                    bold = "Deflect Missile. "
                    mid = "When hit with a ranged attack, you may deflect d10"
                    mid += sh.gf.getSignedStringFromInt(c.level+c.modifiers[1])
                    mid += " damage."
                    it = ""
                    if level>4:
                        it = "For 1 ki, hurl missile as a Dart with "+getMartialArtsDie(c.level)+"+"+str(c.modifiers[1])+" damage if incoming damage reduced to zero."
                    else:
                        it = "For 1 ki, hurl missile as a Dart if damage reduced to zero."
                    return sh.bl.getHTMLfromThruple([bold,mid,it])
        
            self.reactions.append(DeflectMissileEntry(self))
            
            
            
            subclassChoice = inp.choices[3]
            chosen = False
            if subclassChoice == "openHand" or not chosen:
                subclassChoice = "openHand"
                self.classAsString="Monk (Way of the Open Hand)"
                e1 = sh.bl.Entry("<strong>*</strong>When you hit with a Flurry of Blows attack, subject the target to one of the below effects.")
                flurryOfBlowsAstricks = True
                e2 = sh.bl.SpellEntry("knockProneMonk")
                e2.modiferIndex=4
                e3 = sh.bl.SpellEntry("throwMonk")
                e3.modiferIndex=4
                e4 = sh.bl.Entry("<strong>Use Target's Reaction.</strong>")
                b = sh.bl.Block([e1,e2,e3,e4],"WAY OF THE OPEN HAND")
                self.rightColumnBlocks.append(b)
            
                
            # ect ect
        if level>3:
            featChoice = inp.choices[4]
            if featChoice in feats.featFunctions.keys():
                feats.featFunctions[featChoice](self)
            else:
                feats.featFunctions["addDex"](self)
            
            slowFall = sh.bl.SpellEntry("blank")
            slowFall.title="Slow Fall"
            slowFall.preSaveNormalText="Reduce fall damage by "+str(5*level)
            self.reactions.append(slowFall)
            
            quickenedHealing = sh.bl.SpellEntry("blank")
            quickenedHealing.title="Quickened Healing (2 Ki)"
            quickenedHealing.preSaveNormalText="Regain "+getMartialArtsDie(level)+"+"+str(self.profBonus)+" hp"
            self.actionEntries.append(quickenedHealing)
            
            
        if level>4:
            
            fa = sh.bl.SpellEntry("focusedAim")
            kiBlock.entries.insert(0,fa)
            
            extraAttackEntry = sh.bl.TextEntry("extraAttackHighlighted")
            self.actionEntries.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1
            
            stunEntry = sh.bl.SpellEntry("stunningStrike")
            stunEntry.modifierIndex=4
            kiBlock.entries.insert(0,stunEntry)
            
            
            
            
        if level>5:
            
            magicalHand = sh.bl.TextEntry("magicalUnarmedStrike")
            self.charInfos.append(magicalHand)
            
            if subclassChoice == "openHand":
                wholenessOfBody = sh.bl.SpellEntry("blank")
                wholenessOfBody.title="Wholeness of Body"
                wholenessOfBody.preSaveNormalText="Regain "+str(level*3)+"hp. "
                wholenessOfBody.preSaveItalicText="You must take a Long Rest before doing this again. </em>O<em>"
                self.actionEntries.append(wholenessOfBody)
                    
        
        
        
        
        
        unarmAC = 10+self.modifiers[1]+self.modifiers[4]
        self.baseACOptions.append(unarmAC)
        
        
        #add the ki block, add the flurry of blows text
        
        if self.level>1:
            self.addBlockWithCommandLocation(kiBlock,"rightCol")
            
            flurryString = "<strong>Flurry of Blows (1 ki)"
            if flurryOfBlowsAstricks:
                flurryString += "*"
            flurryString += ".</strong> Punch twice.<em> You must have performed a melee attack or spent Ki this turn.</em>"
            
            e = sh.bl.Entry(flurryString)
            self.bonusActionEntries.append(e)
    
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,5,6,14,16]))
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,5,6,14,16]))
        
        #Acrobatics, Athletics, History, Insight, Religion, and Stealth.
        
        
        
def getMartialArtsDie(level):
    martialArtsDie = sh.gf.getNumberFromRange(level,[0,0,0,4,4,9,9,16,16])
    return "d"+str(martialArtsDie)

def getSpeedBonus(level):
    speedBoost = sh.gf.getNumberFromRange(level,[1,1,5,10,14,18],0)
    speedBoost = speedBoost*5
    return int(speedBoost)