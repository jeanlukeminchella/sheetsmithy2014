import Class as sh
import featFunctions as feats

#its on the classclass to do a lot of shit, like generate the stuff, and save profs

class Rogue(sh.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 8
        self.saveProficiencies = [1,3]
        self.defaultMod = 1
        
      
      
        self.loadScoresAndMods([10,15,13,10,14,10],inp)
        self.attributePriorityList = [1,2,4,5,3,0]
        
        super().__init__(inp)
        
        level = self.level
        
        #sort
        
        if not 18 in self.skillProficiencies:
            self.skillProficiencies.append(18)
            
                    
            
        
        
        evasiveMoveLabel="Evasive Action."
        evasiveMoveTitle="EVASIVE ACTIONS"

        self.actionEntries.append(sh.bl.TextEntry("Hide"))
        self.actionEntries.append(sh.bl.TextEntry("useObject"))
        self.highlightedEntries.append(sh.bl.AttackRollEntry("shortsword"))
        self.highlightedEntries.append(sh.bl.AttackRollEntry("shortbow"))
        
        
        if inp.stuff =="":
            self.stuff="Leather Armor, Shortsword x2, Shortbow, Thieves' Tools (lockpicks), Traveller's Clothes, quiver, caltrops, oil x2, crowbar, a bag of 1,000 ball bearings, 10 feet of string"


        
        sneakAttackString = "Once per turn when you hit a target, you may add "
        sneakAttackString += "<strong>"+getSneakAttackString(level)+"</strong>"
        sneakAttackString += " to the damage if you have advantage on the attack roll or the target is distracted (has a hostile within 5ft)."
        
        
        offHandEntry = sh.bl.TextEntry("shortswordOffHandNoMod")
        self.bonusActionEntries.append(offHandEntry)
        
        #right lets level this shit UP
        
        if level>1:
            
            # were going to have to fish out the cunning actions from the action list :(
            
            commandsToFishOut = ["Dash","Disengage","Hide"]
            indiciesToFishOut = []
            
            for i in range(len(self.actionEntries)):
                if self.actionEntries[i].datum in commandsToFishOut:
                    indiciesToFishOut.append(i)
                   
            fishedOutCount = 0
            for index in indiciesToFishOut:
                self.actionEntries.pop(index-fishedOutCount)
                fishedOutCount=fishedOutCount+1
            
            
            evasiveMoveEntry = sh.bl.Entry("<strong>"+evasiveMoveLabel+"</strong>")
            self.bonusActionEntries.append(evasiveMoveEntry)
            self.actionEntries.append(evasiveMoveEntry)
            
            
            evasiveMoves = []
            evasiveMoves.append(sh.bl.TextEntry("Dash"))
            evasiveMoves.append(sh.bl.TextEntry("Disengage"))
            evasiveMoves.append(sh.bl.TextEntry("Hide"))
            evasiveBlock=sh.bl.Block(evasiveMoves,evasiveMoveTitle)
            self.rightColumnBlocks.append(evasiveBlock)
            
        if level>2:
            subclassChoice = inp.choices[3]
            chosen = False
            if subclassChoice == "thief":
                self.classAsString ="Rogue (Thief)"
                self.charInfos.append(sh.bl.Entry(" • Climbing costs you no extra movement <em>(Thief)</em>"))
                self.bonusActionEntries.append(sh.bl.TextEntry("useObjectThief"))
                pass
            elif subclassChoice == "swash" or not chosen:
                
                self.classAsString ="Rogue (Swashbuckler)"
                sneakAttackString = "Once per turn when you hit a target, you may add "
                sneakAttackString += "<strong>"+getSneakAttackString(level)+"</strong>"
                sneakAttackString += "  to the damage if you have advantage on the attack roll, the target is distracted (has a hostile within 5ft), or you are in a duel <em>(Swashbuckler)</em>."
                
                self.charInfos.append(sh.bl.Entry(sh.infoBullet+" Targets of your Shortsword cannot make Opportunity Attacks on you for one turn. <em>(Swashbuckler)</em>"))
                
                
            # ect ect
        if level>3:
            featChoice = inp.choices[4]
            
            if featChoice in feats.featFunctions.keys():
                feats.featFunctions[featChoice](self)
            else:
                feats.featFunctions["addDex"](self)
        if level>4:
            
            self.reactions.append(sh.bl.TextEntry("uncannyDodge"))
        if level>5:
            featChoice = inp.choices[6]
            
        
        
        
        #  Acrobatics, Athletics, Deception, Insight, Intimidation, Investigation, Perception, Performance, Persuasion, Sleight of Hand, and Stealth.
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,4,6,7,8,11,12,13,15,16]))
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,4,6,7,8,11,12,13,15,16]))
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,4,6,7,8,11,12,13,15,16]))
        self.skillProficiencies.append(self.pickSkillProficiency([0,3,4,6,7,8,11,12,13,15,16]))
    
        expertisePriority = [15,11,0,16,18]
        
        numberOfExpertisesToChoose = 2
        if level>5:
            numberOfExpertisesToChoose = 4
        
        # ok this is not going to like it if we have different skills but fuck it - mood low after data loss 07/2024
        
        numberChosen = 0
        
        for expertisePreference in expertisePriority:
            if numberChosen <  numberOfExpertisesToChoose and expertisePreference in self.skillProficiencies and not expertisePreference in self.skillExpertises:
                self.skillExpertises.append(expertisePreference)
                numberChosen+=1
        # ok our preferences list wasnt long enough lets go through character skills and see if we can add them
        if numberChosen < numberOfExpertisesToChoose:
            for p in self.skillProficiencies:
                if not p in self.skillExpertises and numberChosen < numberOfExpertisesToChoose:
                    self.skillExpertises.append(p)
                    numberChosen+=1
        
        
        sneakEntry = sh.bl.Entry(sneakAttackString)
        sneakBlock = sh.bl.Block([sneakEntry],"SNEAK ATTACK")
        self.rightColumnBlocks.append(sneakBlock)
        
        
        
        
        
def getSneakAttackString(level):
    d6count = sh.gf.getNumberFromRange(level,[2,4,6,8,10,12,14,18,20])
    return str(d6count)+"d6"