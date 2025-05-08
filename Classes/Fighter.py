import Class as sh
import featFunctions as feats


class Fighter(sh.Sheet):
    def __init__(self, inp):
        
        self.hitDie = 10
        self.saveProficiencies = [0,2]
        self.defaultMod = 0
        self.proficientWithShields = True
        
        
        
        self.loadScoresAndMods([15,14,13,10,10,10],inp)
        
        dexBased = False
        if self.modifiers[1]>self.modifiers[0]:
            self.defaultMod = 1
            dexBased = True
            
        if dexBased:
            self.attributePriorityList = [1,2,4,0,5,3]
        else:
            self.attributePriorityList = [0,2,1,4,5,3]
        
        super().__init__(inp)
        
        level = self.level
        
                
        
        
            
        bladeEntry = sh.bl.AttackRollEntry("blade")
        handCrossbowEntry = sh.bl.AttackRollEntry("handCrossbow")
        shortswordEntry = sh.bl.AttackRollEntry("shortsword")
        longbowEntry = sh.bl.AttackRollEntry("longbow")
        javelinEntry = sh.bl.AttackRollEntry("javelin")
        heavyWeaponEntry = sh.bl.AttackRollEntry("Heavy Weapon")
        punchEntry = sh.bl.AttackRollEntry("punch")
            
        
        
        wearingShield = inp.wearingShield
        
        if dexBased:
            if wearingShield:
                self.highlightedEntries.append(bladeEntry)
                self.highlightedEntries.append(handCrossbowEntry)
            else:
                self.highlightedEntries.append(shortswordEntry)
                self.highlightedEntries.append(longbowEntry)
                
        else:
            if wearingShield:
                self.highlightedEntries.append(bladeEntry)
                self.highlightedEntries.append(javelinEntry)
            else:
                self.highlightedEntries.append(heavyWeaponEntry)
                self.highlightedEntries.append(javelinEntry)
                self.highlightedEntries.append(punchEntry)
                
            self.highlightedEntries.append(sh.bl.TextEntry("Shove"))
        
        
        stuff = inp.stuff
        
        if inp.stuff =="":
            if dexBased:
                self.stuff="Leather Armor, Longbow, light crossbow, 50ft rope, rations x10, crowbar, hammer & pitons, torches x10"
                if wearingShield:
                    self.stuff+=", Blade (Rapier), shield"
                else:
                    self.stuff+=", Shortsword x2"
            else:
                self.stuff="Chain Mail, handaxe x2, 50ft rope, rations x10, crowbar, hammer & pitons, torches x10"
                if wearingShield:
                    self.stuff+=", Blade (Longsword), shield"
                else:
                    self.stuff+=", Heavy Weapon (Greatsword), javelin"
                

        
        #initialising grapple texts here so that subclasses can change them if they like
        grappleTexts = sh.gf.getDefaultGrappleTexts("Punch")
        
        secondWindEntry = sh.bl.Entry("<strong>Second Wind. </strong> Regain d10+"+str(level)+" hp. <em>You must rest before doing this again. </em> O")
        
        self.bonusActionEntries.append(secondWindEntry)
        
        if dexBased and not wearingShield:
            offHandEntry = sh.bl.TextEntry("shortswordOffHand")
            self.bonusActionEntries.append(offHandEntry)
        
        #right lets level this shit UP
        
        featChoice = inp.choices[2]
        # make this more resilient definitely
        if featChoice==None:
            featChoice="defence"
        feats.featFunctions[featChoice](self)
        
        if level>1:
            actionSurgeEntry = sh.bl.TextEntry("actionSurge")
            self.actionEntries.insert(0,actionSurgeEntry)
            self.highlightedBlockIndex+=1
        if level>2:
            chosen = False
            
            subclassChoice = inp.choices[3]
            if subclassChoice == "champion":
                chosen = True
                self.charInfos.append(sh.bl.Entry("• You Critically Hit on a 19 or 20."))
                self.classAsString = "Fighter (Champion)"
            elif subclassChoice == "rune" or chosen == False:
                self.classAsString = "Fighter (Rune Knight)"
                stoneRuneEntryCommands = [["title","Stone Rune (1 min)"],["range",30],["preSaveNormalText","When an enemy ends their turn, charm them. WIS"],["postSaveNormalText"," to resist."],["preSaveItalicText","Target is incapactiated and has speed 0 while charmed, repeating saves on end of turn. </em>O"],["modiferIndex",2]]
                fireRuneEntryCommands = [["title","Fire Rune"],["preSaveNormalText","When you hit a creature with an attack, you can invoke the Fire rune, summoning firey shackles. "],["preSaveItalicText","2d6 fire damage on hit and on start of target turns, STR"],["postSaveItalicText"," to avoid being restrained, retry on turns end. </em>O"],["modiferIndex",2]]
                
                stoneRuneEntry = sh.bl.SpellEntry("blank")
                stoneRuneEntry.applyCommandList(stoneRuneEntryCommands)
                self.skillNotes.append([6,"(advantage)"])
                self.reactions.append(stoneRuneEntry)
                
                fireRuneEntry = sh.bl.SpellEntry("blank")
                fireRuneEntry.applyCommandList(fireRuneEntryCommands)
                
                endEntry = sh.bl.Entry("<em>You must rest before invoking each rune again.</em>")
                
                runeBlock = sh.bl.Block([fireRuneEntry,endEntry],"RUNES")
                self.rightColumnBlocks.append(runeBlock)
                
            # ect ect
        if level>3:
            featChoice = inp.choices[4]
            
            if featChoice in feats.featFunctions.keys():
                feats.featFunctions[featChoice](self)
            else:
                
                if dexBased:
                    feats.featFunctions["addDex"](self)
                else:
                    feats.featFunctions["addStr"](self)
                    
        if level>4:
            extraAttackEntry = sh.bl.TextEntry("extraAttackHighlighted")
            self.actionEntries.insert(self.highlightedBlockIndex,extraAttackEntry)
            self.highlightedBlockIndex+=1
        if level>5:
            
            featChoice = inp.choices[6]
            
            if featChoice in feats.featFunctions.keys():
                feats.featFunctions[featChoice](self)
            else:
                
                if dexBased:
                    feats.featFunctions["addDex"](self)
                else:
                    feats.featFunctions["addStr"](self)
        
        
        #Acrobatics, Animal Handling, Athletics, History, Insight, Intimidation, Perception, and Survival.
        self.skillProficiencies.append(self.pickSkillProficiency([0,1,3,5,6,7,11,17]))
        self.skillProficiencies.append(self.pickSkillProficiency([0,1,3,5,6,7,11,17]))
        
        
        
        
        
        
        
        #add all this shit to the main class block & entry lists (columns ect), and compile some stuff
        
        
        #if were grappling lets tap it in. grappling entries all have to be flat text
        if not dexBased:
            grappleEntries =[]
            for grappleText in grappleTexts:
                grappleEntries.append(sh.bl.Entry(grappleText))
            self.rightColumnBlocks.append(sh.bl.Block(grappleEntries,"GRAPPLING"))
        
