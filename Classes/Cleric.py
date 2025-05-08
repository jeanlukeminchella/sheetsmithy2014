
import Class as sh
import featFunctions as feats

channelDivinityText = "Channel Divinity"
channelDivinityTextPlural = "Channel Divinities"

class Cleric(sh.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 8
        self.saveProficiencies = [4,5]
        self.defaultMod = 4
        self.proficientWithShields = True
        
        #default mods if none selected
        if inp.modifiers == None:
            self.modifiers = [0,2,2,0,3,0]
        else:
            self.modifiers = inp.modifiers
        
        self.loadScoresAndMods([10,14,13,10,15,10],inp)
        if self.modifiers[0]>self.modifiers[1]:
            self.attributePriorityList = [4,2,0,1,3,5]
        else:
            self.attributePriorityList = [4,2,1,0,3,5]
        super().__init__(inp)
        level = self.level
        
        self.ritualCaster = True
        
        sacredFlame = sh.bl.AttackRollEntry("sacredFlame")
        self.highlightedEntries.append(sacredFlame)
        qstaff = sh.bl.AttackRollEntry("quarterstaff")
        qstaff.forcedMod=0
        if self.modifiers[0]>self.modifiers[1]:
            
            self.highlightedEntries.append(qstaff)
        else:
            dag = sh.bl.AttackRollEntry("dagger")
            dag.forcedMod=1
            self.highlightedEntries.append(dag)
        self.actionEntries.append(sh.bl.SpellEntry("guidance"))
        
            
        
        if self.stuff =="":
            self.stuff="Scale Mail, Daggers x2, Shield, Traveller's Clothes, rations x10, 50ft rope"
            
        
        spellcastingTitle = "SPELLCASTING"
        
        #of type Entry...
        notesForSpellCastingBlock = []
        
        #generate all the spells for easy reference, not all of them may the same subtype of Entry though
        
        cureWounds = sh.bl.HealingEntry("cureWounds")
        healingWord = sh.bl.HealingEntry("healingWord")
        command = sh.bl.SpellEntry("command")
        guidingBolt = sh.bl.AttackRollEntry("guidingBolt")
        shieldOfFaith = sh.bl.SpellEntry("shieldOfFaith")
        bless = sh.bl.SpellEntry("bless")
        sanctuary = sh.bl.SpellEntry("sanctuary")
        dm = sh.bl.SpellEntry("detectMagic")
        protectionFromEvilAndGood = sh.bl.SpellEntry("protectionFromEvilAndGood")
        
         
        
        lesserRestoration = sh.bl.SpellEntry("lesserRestoration")
        spiritualWeapon = sh.bl.AttackRollEntry("spiritualWeapon")
        zoneOfTruth = sh.bl.SpellEntry("zoneOfTruth")
        holdPerson = sh.bl.SpellEntry("holdPerson")
        
        dispelMagic = sh.bl.SpellEntry("dispelMagic")
        revivify = sh.bl.SpellEntry("revivify")
        masshw = sh.bl.HealingEntry("massHealingWord")
        spiritShroud = sh.bl.SpellEntry("spiritShroud")
        
        
        
        priorityListByMaxSpellSlot={
            "1":[bless,healingWord, protectionFromEvilAndGood,guidingBolt,command,sanctuary,cureWounds,shieldOfFaith,dm],
            "2":[bless,healingWord,protectionFromEvilAndGood,spiritualWeapon, guidingBolt,holdPerson,sanctuary,command,shieldOfFaith,lesserRestoration,cureWounds,dm,zoneOfTruth],
            "3":[masshw,spiritualWeapon,dispelMagic,revivify, protectionFromEvilAndGood,guidingBolt,holdPerson,healingWord,sanctuary,shieldOfFaith,spiritShroud,bless, command,lesserRestoration,cureWounds,dm,zoneOfTruth]
        }
        
        
        
        
        
        subclassChosen = False
        subclassChoice = inp.choices[1]
        
        
        
        
        if subclassChoice == "life" or not subclassChosen:
            self.classAsString="Cleric (of Life)"
            
            cureWounds.healingBonus = 3
            healingWord.healingBonus = 3
            masshw.healingBonus = 5
            revivify.preSaveNormalText = revivify.preSaveNormalText.replace("1","6")
            revivify.preSaveNormalText = revivify.preSaveNormalText.replace("point","points")
            self.actionEntries.append(cureWounds)
            self.bonusActionEntries.append(healingWord)
            subclassChosen = True
            preserveLife = sh.bl.SpellEntry("blank")
            preserveLife.title = "Preserve Life ("+channelDivinityText+", "+sh.gf.getDistanceString(30)+")"
            preserveLife.preSaveNormalText = "Distribute " + str(level*5) +" hp to allies within range."
            if level>1:
                self.actionEntries.append(preserveLife)
        
        
            
        resourceDictionary = {
            1:[["Spell",2],[channelDivinityText,1]],
            2:[["Spell",3],[channelDivinityText,1]],
            3:[[self.costDic["1"],4],[self.costDic["2"],2],[channelDivinityText,1]],
            4:[[self.costDic["1"],4],[self.costDic["2"],3],[channelDivinityText,1]],
            5:[[self.costDic["1"],4],[self.costDic["2"],3],[self.costDic["3"],2],[channelDivinityText,1]],
            6:[[self.costDic["1"],4],[self.costDic["2"],3],[self.costDic["3"],3],[channelDivinityText,2]]
            
        }
        
        if level <3:
            self.costDic= {
                "1":"Spell"
            }
        
        spellSlotResourceTuples=resourceDictionary[self.level]
        
        # level up
        
        level = self.level
        
        if level>1:
            s = channelDivinityText
            if level>5:
                s=channelDivinityTextPlural
            notesForSpellCastingBlock.append(sh.bl.Entry("<em> You regain your "+s+" on a rest.</em>"))
            
            harnessDivinePowerLimitText = "You must take a Long Rest before doing this again.</em> O<em>"
            if level>5:
                harnessDivinePowerLimitText = "You can do this twice per long rest."
                
            harnessDivinePower = sh.bl.SpellEntry("blank")
            harnessDivinePower.title = "Regain Spell Slot ("+channelDivinityText+")"
            harnessDivinePower.preSaveItalicText = harnessDivinePowerLimitText+" <em>(TCoE)</em>"
            
            spellLevel = int(self.profBonus/2)+self.profBonus%2
            harnessText = "Harness your divine power and regain a "+self.costDic[str(spellLevel)]+" slot."
            harnessDivinePower.preSaveNormalText = harnessText
            
            self.bonusActionEntries.append(harnessDivinePower)
            
            turnUndead = sh.bl.SpellEntry("blank")
            turnUndead.title = "Turn Undead ("+channelDivinityText+", "+sh.gf.getDistanceString(30)+")"
            turnUndead.preSaveNormalText = "Undead that can see or hear you must spend its turns trying to move as far away from you as it can."
            turnUndead.preSaveItalicText = "WIS"+str(self.profBonus+8+self.modifiers[4])+" to resist."
            
            self.actionEntries.append(turnUndead)
            
                
                
                
            
        if level>2:
            
            pass
                    
         
        if level>3:
            
            featChoice = inp.choices[4]
            if featChoice in feats.featFunctions.keys():
                feats.featFunctions[featChoice](self)
            else:
                feats.featFunctions["addWis"](self)
                
        
        #lets start fishing some stuff out
        
        commandsToFishOut = []
            
        if level>4:
            commandsToFishOut.extend(["Dodge"])
            
        
        if level>5:
            commandsToFishOut.extend(["Disengage","Dash"])
            
        indiciesToFishOut = []
        
        for i in range(len(self.actionEntries)):
            if self.actionEntries[i].datum in commandsToFishOut:
                indiciesToFishOut.append(i)
                
        fishedOutCount = 0
        for index in indiciesToFishOut:
            self.actionEntries.pop(index-fishedOutCount)
            fishedOutCount=fishedOutCount+1
          
          
        
        
        
        
        # lets load in the spells - ones we dont have already of course
        
        l = self.actionEntries[:]
        l.extend(self.reactions)
        l.extend(self.bonusActionEntries)
        
        spellTitlesKnownAlready = []
        
        for action in l:
            if type(action) == sh.bl.SpellEntry or type(action)==sh.bl.AttackRollEntry:
                spellTitlesKnownAlready.append(action.title)
        
        spellPriorityList = priorityListByMaxSpellSlot[str(sh.gf.getNumberFromRange(self.level,[2,4]))]
        spellsKnown = int(level)+self.modifiers[4]
        spellsAdded = 0
        nextSpellIndexToConsider = 0
        
        while spellsAdded<spellsKnown and nextSpellIndexToConsider<len(spellPriorityList):
            
            if not spellPriorityList[nextSpellIndexToConsider].title in spellTitlesKnownAlready:
                
                if spellPriorityList[nextSpellIndexToConsider].castTime=="a":
                    self.actionEntries.append(spellPriorityList[nextSpellIndexToConsider])
                elif spellPriorityList[nextSpellIndexToConsider].castTime=="ba":
                    self.bonusActionEntries.append(spellPriorityList[nextSpellIndexToConsider])
                elif spellPriorityList[nextSpellIndexToConsider].castTime=="re":
                    self.reactionEntries.append(spellPriorityList[nextSpellIndexToConsider])
                else:
                    print("this cast time confused me: ",spellPriorityList[nextSpellIndexToConsider].castTime," in spell ",spellPriorityList[nextSpellIndexToConsider].title)
                
                nextSpellIndexToConsider+=1
                spellsAdded+=1
            else:
                nextSpellIndexToConsider+=1
                
        
        l = self.actionEntries[:]
        l.extend(self.reactions)
        l.extend(self.bonusActionEntries)
        
        
        weNeedToConcentrate = False
        weNeedToExplainRituals= False
        
        for action in l:
            if type(action) == sh.bl.SpellEntry or type(action)==sh.bl.AttackRollEntry:
                if action.conc:
                    weNeedToConcentrate=True
                if action.ritual:
                    weNeedToExplainRituals=True
                    
        if weNeedToConcentrate:
            notesForSpellCastingBlock.append(sh.bl.TextEntry("conc"))
        if weNeedToExplainRituals:
            notesForSpellCastingBlock.append(sh.bl.TextEntry("ritual"))
            
        
        #add all this shit to the main class block & entry lists (columns ect), and compile some stuff
        
        #lets make the spellcasting block
        
        # History, Insight, Medicine, Persuasion, and Religion.
        self.skillProficiencies.append(self.pickSkillProficiency([5,6,9,13,14]))
        self.skillProficiencies.append(self.pickSkillProficiency([5,6,9,13,14]))
        
        
        resourceEntry = sh.bl.Entry(sh.gf.getSpellSlotHTMLString(spellSlotResourceTuples))
        spellcastingBlockEntries = [resourceEntry]
        spellcastingBlockEntries.extend(notesForSpellCastingBlock)
        
        #scan the actions,bonusactions, and reactions for a concentration mark
        
        
        
        
                
        
        
        spellBlock = sh.bl.Block(spellcastingBlockEntries,spellcastingTitle)
        self.rightColumnBlocks.append(spellBlock)
            
        

     
