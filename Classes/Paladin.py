import Class as sh
import featFunctions as feats

channelDivinityText = "Channel Divinity"
channelDivinityTextPlural = "Channel Divinities"


class Paladin(sh.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 10
        self.saveProficiencies = [4,5]
        self.defaultMod = 0
        self.proficientWithShields = True
        
        
        self.loadScoresAndMods([15,10,14,10,10,13],inp)
        
        self.attributePriorityList = [0,5,2,1,4,3]
        
        super().__init__(inp)
        
        
        
        level = self.level
        
        if self.wearingShield:
            
            self.highlightedEntries.append(sh.bl.AttackRollEntry("longsword"))
            self.highlightedEntries.append(sh.bl.AttackRollEntry("javelin"))
            
        else:
            
            self.highlightedEntries.append(sh.bl.AttackRollEntry("Heavy Weapon"))
            self.highlightedEntries.append(sh.bl.AttackRollEntry("javelin"))
            
        
        if self.stuff =="":
            self.stuff="Scale Mail, sword, traveller's clothes, rations x10"
            
        
        divineSenseEntry = sh.bl.SpellEntry("divineSense")
        divineSenseEntry.preSaveItalicText=str(1+self.modifiers[5])+" uses per long rest - </em>"
        for i in range(1+self.modifiers[5]):
            divineSenseEntry.preSaveItalicText+= " O"
        if self.modifiers[5]>0:
            
            self.actionEntries.append(divineSenseEntry)
        
        layOnHandsEntry =sh.bl.SpellEntry("layHands")
        layOnHandsEntry.preSaveNormalText= "Restore hp to a touched creature from a pool of "+str(5*level)+ " hp"
        self.actionEntries.append(layOnHandsEntry)
        
        subclass = None
        
        #right lets level this shit UP
        
       
        
        spellcastingTitle = "SPELLCASTING"
        spellcasting=False
        
        #of type Entry...
        notesForSpellCastingBlock = []
        
        spellsKnown = int(level/2)+self.modifiers[5]
        
        
        #generate all the spells for easy reference, and set their spellcasting ability to char. not all of them may the same subtype of Entry though
        
        cureWounds = sh.bl.HealingEntry("cureWounds")
        cureWounds.modiferIndex=5
        healingWord = sh.bl.HealingEntry("healingWord")
        healingWord.modiferIndex=5
        command = sh.bl.SpellEntry("command")
        command.modiferIndex=5
        shieldOfFaith = sh.bl.SpellEntry("shieldOfFaith")
        shieldOfFaith.modiferIndex=5
        wrathfulSmite = sh.bl.SpellEntry("wrathfulSmite")
        wrathfulSmite.modiferIndex=5
        heroism = sh.bl.SpellEntry("heroism")
        heroism.modiferIndex=5
        heroism.applyCommandList([["preSaveNormalText","A willing creature you touch is imbued with bravery. Until the spell ends, the creature is immune to being frightened and gains "+str(self.modifiers[5])+" temporary hit points at the start of each of its turns."]])
        dm = sh.bl.SpellEntry("detectMagic")
        ts = sh.bl.SpellEntry("thunderousSmite")
        ts.modiferIndex=5
        protectionFromEvilAndGood = sh.bl.SpellEntry("protectionFromEvilAndGood")
        
        
        
        
        lesserRestoration = sh.bl.SpellEntry("lesserRestoration")
        lesserRestoration.modiferIndex=5
        
        es = sh.bl.SpellEntry("ensnaringStrike")
        es.modiferIndex=5
        ms = sh.bl.SpellEntry("mistyStep")

        priorityListByMaxSpellSlot={
            "1":[ts,protectionFromEvilAndGood,command,shieldOfFaith,wrathfulSmite,dm,heroism,cureWounds],
            "2":[ts,protectionFromEvilAndGood,lesserRestoration,command,wrathfulSmite,shieldOfFaith,cureWounds,heroism,dm]
            }
        
        
        resourceDictionary = {
            1:[["Spell",0],[channelDivinityText,0]],
            2:[["Spell",2]],
            3:[["Spell",3],[channelDivinityText,1]],
            4:[["Spell",3],[channelDivinityText,1]],
            5:[[self.costDic["1"],4],[self.costDic["2"],2],[channelDivinityText,1]],
            6:[[self.costDic["1"],4],[self.costDic["2"],2],[channelDivinityText,1]]
            
            
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
            subclass = inp.choices[3]
            
            
            if subclass == "ancients":
                self.classAsString="Paladin (Oath of the Ancients)"
                subclassChosen = True
                self.actionEntries.append(sh.bl.SpellEntry("swAnimals"))
                self.bonusActionEntries.append(es)
                
                naturesWrath = sh.bl.SpellEntry("blank")
                naturesWrath.title = "Nature's Wrath ("+channelDivinityText+", 10ft)"
                naturesWrath.preSaveNormalText = "Vines restrain a foe. STR/DEX"
                naturesWrath.postSaveNormalText = " to resist."
                naturesWrath.preSaveItalicText = "Target repeats save at the end of their turns."
                naturesWrath.modiferIndex=5
                self.actionEntries.append(naturesWrath)
                
                mb = sh.bl.SpellEntry("moonbeam")
                mb.modiferIndex=5
                if level>4:
                    self.actionEntries.append(mb)
                    self.bonusActionEntries.append(ms)
                
                
            
            if subclass == "vengeance" or not subclassChosen:
                subclass = "vengeance"
                self.classAsString="Paladin (Oath of Vengeance)"
                
                hm = sh.bl.SpellEntry("huntersMark")
                self.bonusActionEntries.append(hm)
                 
                bane = sh.bl.SpellEntry("bane")
                bane.modiferIndex=5
                self.actionEntries.append(bane)
                
                vowOfEmnity = sh.bl.SpellEntry("blank")
                vowOfEmnity.title = "Vow of Emnity ("+channelDivinityText+", 10ft, 1 min)"
                vowOfEmnity.preSaveNormalText = "You gain advantage on attack rolls against target."
                self.bonusActionEntries.append(vowOfEmnity)
                
                abjureEnemy = sh.bl.SpellEntry("blank")
                abjureEnemy.modiferIndex=5
                abjureEnemy.title = "Abjure ("+channelDivinityText+", 60ft, 1 min)"
                abjureEnemy.preSaveNormalText = "Target is frightened and its speed is 0. WIS"
                abjureEnemy.postSaveNormalText = " to resist. Targets who resist still have their speed halved until they take damage."
                abjureEnemy.preSaveItalicText = "Fiends and Undead have disadvantage on their saving throw. "
                self.actionEntries.append(abjureEnemy)
                
                
                
                
                if level>4:
                    self.bonusActionEntries.append(ms)
                    
                    hp = sh.bl.SpellEntry("holdPerson")
                    hp.modiferIndex=5
                    self.actionEntries.append(hp)
                    
                
            
            harnessDivinePowerLimitText = "You must take a Long Rest before doing this again.</em> O<em>"
            if level>6:
                harnessDivinePowerLimitText = "You can do this twice per long rest."
                
            harnessDivinePower = sh.bl.SpellEntry("blank")
            harnessDivinePower.title = "Regain Spell Slot ("+channelDivinityText+")"
            harnessDivinePower.preSaveItalicText = harnessDivinePowerLimitText+" <em>(TCoE)</em>"
            
            spellLevel = int(self.profBonus/2)+self.profBonus%2
            harnessText = "Harness your divine power and regain a "+self.costDic[str(spellLevel)]+" slot. "
            harnessDivinePower.preSaveNormalText = harnessText
            
            self.bonusActionEntries.append(harnessDivinePower)
            
            
            
            
                    
            # ect ect
        if level>3:
            
            featChoice = inp.choices[4]
            if featChoice in feats.featFunctions.keys():
                feats.featFunctions[featChoice](self)
            else:
                feats.featFunctions["addStr"](self)
                
            # in case it has changed
            cureWounds.preSaveNormalText="Heal a target d8+"+str(self.modifiers[5])
                
        if level>4:
            extraAttackEntry = sh.bl.TextEntry("extraAttackHighlighted")
            self.actionEntries.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1
            
        if level>5:
            char = max(1,self.modifiers[5])
            auraBoosts = [[0,char],[1,char],[2,char],[3,char],[4,char],[5,char]]
            self.saveBoosts.extend(auraBoosts)
            auraText = sh.bl.SpellEntry("blank")
            auraText.title = "</strong>"+sh.infoBullet+"Allies within "+sh.gf.getDistanceString(10)+" gain "+sh.gf.getSignedStringFromInt(char)+" to saving throws<strong>"
            self.charInfos.append(auraText)
        
        
        
        
        
        
        
        #add all this shit to the main class block & entry lists (columns ect), and compile some stuff
        
        #lets make the spellcasting block
        if spellcasting:
            
            l = self.actionEntries[:]
            l.extend(self.reactions)
            l.extend(self.bonusActionEntries)
            
            spellTitlesKnownAlready = []
            
            for action in l:
                if type(action) == sh.bl.SpellEntry or type(action)==sh.bl.AttackRollEntry:
                    spellTitlesKnownAlready.append(action.title)
            
            spellPriorityList = priorityListByMaxSpellSlot[str(sh.gf.getNumberFromRange(self.level,[4]))]
            spellsKnown = int(level/2)+self.modifiers[4]
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
            
            
            
            s = sh.bl.Entry("<strong>Smite. </strong>You can expend one spell slot on a melee hit to deal +2d8 damage, or +3d8 damage if Smiting an Undead or Fiend.")
            if level > 4:
                s = sh.bl.Entry("<strong>Smite. </strong>You can expend one spell slot on a melee hit to deal +2d8 damage, plus 1d8 for each spell level higher than 1st, plus +1d8 damage if Smiting an Undead or Fiend.")
            spellcastingBlockEntries.append(s)
            
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
            
        self.skillProficiencies.append(self.pickSkillProficiency([3,6,7,9,13,14]))
        self.skillProficiencies.append(self.pickSkillProficiency([3,6,7,9,13,14]))
        
        # Athletics, Insight, Intimidation, Medicine, Persuasion, and Religion.
        
        """if numberOfBlanks>0:
            
            blankBlock = sh.bl.Block([sh.bl.TextEntry("blank")]*numberOfBlanks)
            self.middleColumnBlocks.append(blankBlock)
        """
        