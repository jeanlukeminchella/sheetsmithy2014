import Class as sh
import featFunctions as feats

defaultRageTexts = ["• You take half non-magical damage.","• You may enter Rage as a Bonus Action.","• You have advantage on Athletics checks and Strength saving throws.","• You may add 2 to weapon damage.","• Rages last one minute, but end early if you fall unconcious. You must also attack or take damage each round."]

#its on the classclass to do a lot of shit, like generate the stuff, default mod, and save profs

class Barbarian(sh.Sheet):
    def __init__(self, inp):
        
        rageTexts = defaultRageTexts[:]
        
        self.hitDie = 12
        self.saveProficiencies = [0,2]
        self.defaultMod = 0
        self.proficientWithShields = True
        
        #default mods if none selected
        if inp.modifiers == None:
            self.modifiers = [3,2,2,0,0,0]
        else:
            self.modifiers = inp.modifiers
            
        self.loadScoresAndMods([15,14,13,10,10,10],inp)
        self.attributePriorityList = [0,2,1,4,3,0]
        
        super().__init__(inp)
        level = self.level
        
        self.highlightedEntries.append(sh.bl.AttackRollEntry("javelin"))
        self.highlightedEntries.append(sh.bl.AttackRollEntry("Heavy Weapon"))
        self.highlightedEntries.append(sh.bl.TextEntry("Shove"))
        
        
        if self.stuff =="":
            self.stuff="Shield, Heavy Weapon, Javelins x5, rations x10, 50ft rope"
            
        
        rageTitle = "RAGE - "+"O "*getRageCount(level)
        
        
        wereAddingGrapple = True
        grappleTexts = sh.gf.getDefaultGrappleTexts("Javelin")
        
        
        
        #right lets level this shit UP
        subclassChoice = None
        
        if level>1:
            #get reckless
            recklessEntry = sh.bl.TextEntry("reckless")
            self.actionEntries.insert(0,recklessEntry)
            self.highlightedBlockIndex+=1
            # danger sense
            self.saveNotes.append([1," (advantage)"])
            for i in range(len(self.actionEntries)):
                if self.actionEntries[i].datum == "Dodge":
                    self.actionEntries[i].textEntryDictionary = {
                        "Dodge":["Dodge. ","You are attacked with disadvantage until your next turn.",""]
                    }
                    
        if level>2:
            subclassChoice = inp.choices[3]
            chosen=False
            if subclassChoice == "bear":
                chosen=True
                rageTexts[0]="• You take half non-psychic damage."
                self.classAsString = "Barbarian (Totem of the Bear)"
            elif subclassChoice == "wild" or not chosen:
                inp.choices[3]="wild"
                subclassChoice = "wild"
                self.actionEntries.append(sh.bl.TextEntry("senseMagicItem"))
                self.classAsString = "Barbarian (Wild Magic)"
                rageTexts.append("• When you enter rage, roll a d8 to unleash a magical effect. <em>(Wild Magic - see TCoE for effects)</em>")
            # ect ect
        if level>3:
            featChoice = inp.choices[4]
            if featChoice == None:
                featChoice="boostScores"
            feats.featFunctions[featChoice](self)
        if level>4:
            extraAttackEntry = sh.bl.TextEntry("extraAttackHighlighted")
            self.actionEntries.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1
            self.speed+=10
        if level>5:
            subclassChoice = inp.choices[3]
            if subclassChoice == "bear":
                
                self.charInfos.append(sh.bl.Entry(sh.infoBullet+" + "+ "you have advantage on Strength checks made to push, pull, lift, or break objects. <em> (Bear)</em>"))
            elif subclassChoice == "wild":
                bolsterTitle = "<strong>Bolster.</strong> Add a d3 to target's ability checks and attack for 10 minutes, or have them regain a level d3 spell slot. O"+" O"*(self.profBonus-1)
                bolsterEntry = sh.bl.Entry(bolsterTitle)
                self.actionEntries.append(bolsterEntry)
        
        
        self.skillProficiencies.append(self.pickSkillProficiency([1,3,7,10,11,17]))
        self.skillProficiencies.append(self.pickSkillProficiency([1,3,7,10,11,17]))
        # Animal Handling, Athletics, Intimidation, Nature, Perception, and Survival.
        
        
        
        
        
        
        
        #add all this shit to the main class block & entry lists (columns ect), and compile some stuff
        
        #get the rage in there
        #get the entries first
        rageEntries = []
        for t in rageTexts:
            rageEntries.append(sh.bl.Entry(t))
        rageBlock = sh.bl.Block(rageEntries,rageTitle)
        #maybe dont put it at the bottom?
        self.rightColumnBlocks.append(rageBlock)
        
        
        
        #if were grappling lets tap it in. grappling entries all have to be flat text
        if wereAddingGrapple:
            grappleEntries =[]
            for grappleText in grappleTexts:
                grappleEntries.append(sh.bl.Entry(grappleText))
            self.rightColumnBlocks.append(sh.bl.Block(grappleEntries,"GRAPPLING"))
        
        self.baseACOptions.append(10+self.modifiers[1]+self.modifiers[2])
        
        
    
        
        

def getRageCount(level):
    return sh.gf.getNumberFromRange(level,[0,2,5,11,16])
    