import Class as sh
import featFunctions as feats


class Ranger(sh.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 10
        self.saveProficiencies = [0,1]
        self.defaultMod = 1
        self.proficientWithShields = True
        
        self.loadScoresAndMods([10,15,13,10,14,10],inp)
        self.attributePriorityList = [1,2,4,5,0,3]
        
        super().__init__(inp)
        level = self.level
        
        if self.wearingShield:
            
            self.highlightedEntries.append(sh.bl.AttackRollEntry("handCrossbow"))
            self.highlightedEntries.append(sh.bl.AttackRollEntry("blade"))
            
        else:
            
            self.highlightedEntries.append(sh.bl.AttackRollEntry("longbow"))
            self.highlightedEntries.append(sh.bl.AttackRollEntry("shortsword"))
            
        
        if self.stuff =="":
            self.stuff="Leather Armor, Longbow, traveller's clothes, Shortsword x2,rations x10, 50ft rope, pitons x10, hammer, torches x10"
            
        
        
        
            
        
        self.charInfos.append(sh.bl.Entry(" • Favoured Enemy: ___________________ <br><em>Adv. on tracking & lore checks.</em>"))
        self.charInfos.append(sh.bl.Entry(" • Languages: Common, __________, ___________, ___________"))
        
        #right lets level this shit UP
        
        # this is the list of spell slots etc that the character has
        spellSlotResourceTuples = []
        
        
        spellcastingTitle = "SPELLCASTING"
        spellcasting=False
        
        #of type Entry...
        notesForSpellCastingBlock = []
        
        spellsKnown = sh.gf.getNumberFromRange(level, [1,1,2,4])
        
        
        
        #generate all the spells for easy reference, and set their spellcasting ability to wisdom. not all of them may the same subtype of Entry though (some may be attack rolls, others spells)
        cureWounds = sh.bl.SpellEntry("cureWounds")
        cureWounds.preSaveNormalText="Heal a target d8+"+str(self.modifiers[4])
        huntersMark = sh.bl.SpellEntry("huntersMark")
        huntersMark.modiferIndex=4
        entangle = sh.bl.SpellEntry("entangle")
        entangle.modiferIndex=4
        
        spikeGrowth = sh.bl.SpellEntry("spikeGrowth")
        spikeGrowth.modiferIndex=4
        lesserRestoration = sh.bl.SpellEntry("lesserRestoration")
        lesserRestoration.modiferIndex=4
        
         
        
        priorityListByMaxSpellSlot={
            "1":[cureWounds,huntersMark,entangle],
            "2":[cureWounds,spikeGrowth,huntersMark,lesserRestoration,entangle]
            }
        
        resourceDictionary = {
            1:[["Spell",0]],
            2:[["Spell",2]],
            3:[["Spell",3]],
            4:[["Spell",3]],
            5:[[self.costDic["1"],4],[self.costDic["2"],2]],
            6:[[self.costDic["1"],4],[self.costDic["2"],2]]
            
            
        }
        
        if level <5:
            self.costDic= {
                "1":"Spell"
            }
        
        spellSlotResourceTuples=resourceDictionary[self.level]
        
        if level>1:
            spellcasting = True
            featChoice = inp.choices[2]
            if featChoice in feats.featFunctions.keys():
                feats.featFunctions[featChoice](self)
            else:
                feats.featFunctions["defence"](self)
            
        if level>2:
            
            subclassChosen = False
            subclassChoice = inp.choices[3]
            
            if subclassChoice == "hunter":
                self.classAsString="Ranger (Hunter)"
                
                colSlayer = sh.bl.SpellEntry("blank")
                colSlayer.preSaveNormalText = sh.infoBullet + " Once per turn, you may deal an extra d8 damage to a wounded target you have hit."
                colSlayer.preSaveItalicText = "<em> (Monster Slayer) </em>"
                self.charInfos.append(colSlayer)
                
                subclassChosen = True
                
            if subclassChoice == "monster slayer" or not subclassChosen:
                
                self.classAsString="Ranger (Monster Slayer)"
                
                protectionFromEvilAndGood = sh.bl.SpellEntry("protectionFromEvilAndGood")
                self.actionEntries.append(protectionFromEvilAndGood)
                
                hunterSense = sh.bl.SpellEntry("blank")
                hunterSense.title = "Hunter's Sense (60ft)"
                hunterSense.preSaveNormalText = " Discern a creature's immunities, resistances, and vulnerabilities."
                count = "O "*max(1,self.modifiers[4])
                hunterSense.preSaveItalicText = "Uses per long rest -  </em>"+count+" <em>(Monster Slayer)"
                self.actionEntries.append(hunterSense)
                
                slayersPrey = sh.bl.SpellEntry("blank")
                slayersPrey.title = "Mark Slayer's Prey (60ft)"
                slayersPrey.preSaveNormalText = " Each turn, the first time you hit the target you deal an extra d6 damage. "
                slayersPrey.preSaveItalicText = "Effect ends if you target a new prey. (Monster Slayer)"
                self.bonusActionEntries.append(slayersPrey)
                
                
                
            
            #primal awareness
            swAnimals = sh.bl.SpellEntry("swAnimals")
            swAnimals.preSaveItalicText=" One free casting per long rest. O"
            self.actionEntries.append(swAnimals)
            
            
        if level>3:
            featChoice = inp.choices[4]
            if featChoice in feats.featFunctions.keys():
                feats.featFunctions[featChoice](self)
            else:
                feats.featFunctions["addDex"](self)
            
        if level>4:
            extraAttackEntry = sh.bl.TextEntry("extraAttackHighlighted")
            self.actionEntries.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1

        if level>5:
            self.speed+=5
            self.charInfos.append(sh.bl.Entry(" • Your speed is for walking, climbing or swimming."))
            

        
        # Animal Handling, Athletics, Insight, Investigation, Nature, Perception, Stealth, and Survival.
        self.skillProficiencies.append(self.pickSkillProficiency([1,3,6,7,10,11,16,17]))
        self.skillProficiencies.append(self.pickSkillProficiency([1,3,6,7,10,11,16,17]))
        self.skillProficiencies.append(self.pickSkillProficiency([1,3,6,7,10,11,16,17]))
        
        # deft explorer - expertise in stealth
        if 16 in self.skillProficiencies:
            self.skillExpertises.append(16)
        else:
            self.skillExpertises.append(self.skillProficiencies[0])
        
        
        
        
        #add all this shit to the main class block & entry lists (columns ect), and compile some stuff
        
        #lets make the spellcasting block
        if spellcasting:
            
            # lets load in the spells - ones we dont have already of course
        
            l = self.actionEntries[:]
            l.extend(self.reactions)
            l.extend(self.bonusActionEntries)
            
            spellTitlesKnownAlready = []
            
            for action in l:
                if type(action) == sh.bl.SpellEntry or type(action)==sh.bl.AttackRollEntry:
                    spellTitlesKnownAlready.append(action.title)
            
            spellPriorityList = priorityListByMaxSpellSlot[str(sh.gf.getNumberFromRange(self.level,[4]))]
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
            
            
            resourceEntry = sh.bl.Entry(sh.gf.getSpellSlotHTMLString(spellSlotResourceTuples))
            spellcastingBlockEntries = [resourceEntry]
            spellcastingBlockEntries.extend(notesForSpellCastingBlock)
            
            #scan the actions,bonusactions, and reactions for a concentration mark
            
            weNeedToConcentrate = False
            
            l = self.actionEntries[:]
            l.extend(self.reactions)
            l.extend(self.bonusActionEntries)
            
            for action in l:
                if type(action) == sh.bl.SpellEntry or type(action)==sh.bl.AttackRollEntry:
                    if action.conc:
                        weNeedToConcentrate=True
                        break
                    
            if weNeedToConcentrate:
                spellcastingBlockEntries.append(sh.bl.TextEntry("conc"))
            
            spellBlock = sh.bl.Block(spellcastingBlockEntries,spellcastingTitle)
            self.rightColumnBlocks.append(spellBlock)
        
        
        
        
        """if numberOfBlanks>0:
            
            blankBlock = sh.bl.Block([sh.bl.TextEntry("blank")]*numberOfBlanks)
            self.middleColumnBlocks.append(blankBlock)
        """
        