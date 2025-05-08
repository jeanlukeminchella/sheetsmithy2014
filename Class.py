
import globalFunctions as gf
#this 'bl' nonesense needs digging out all the code and sorting i think
import Entry as bl
import Armor as armor
import Race as raceFunctions

equipmentTitle = "EQUIPMENT & TREASURE"
bonusActionTitle = "BONUS ACTIONS (1 per turn)"
skillsAsStrings = ["Acrobatics",   "Animal Handling",  "Arcana",  "Athletics",  "Deception",  "History",  "Insight",  "Intimidation",  "Investigation",  "Medicine",  "Nature",  "Perception","Performance",  "Persuasion",  "Religion",  "Sleight of Hand",  "Stealth",  "Survival",  "Thieves' Tools"]
savesAsStrings = ["Strength","Dexterity","Constitution","Intelligence","Wisdom","Charisma"]
skillModifierIndex =[1,4,3,0,5,3,4,5,3,4,3,4,5,5,3,1,1,4,1]
#this needs digging out all the code and sorting
infoBullet = gf.infoBullet

armors = ["Studded Leather","Leather","Splint","Scale Mail","Ring Mail","Plate","Hide","Half Plate","Chain Shirt","Chain Mail","Breastplate"]

# in this iteration 17/02/2024 - were having BAs on left, actions in middle and char info in top left, reactions bottom right etc. trying to move away from [some other shite]
class Sheet:
    
    #inp is of type Input
    def __init__(self, inp):
        
        #cosmetics stuff & variants
        
        self.showScores = inp.showScores
        self.tashaContent = inp.tashaContent
        
        self.skillProficiencies = []
        self.skillExpertises = []
        
        # these are tuples with [index,modifier/note]
        # we should check for duplicates in the notes if possible here :)
        self.skillBoosts = []
        self.skillNotes = []
        self.saveBoosts = []
        self.saveNotes = []
        # saveProficiencies is not initaliased here, type of sheet has already initalised it
        
        self.level = inp.level
        self.profBonus = gf.getNumberFromRange(self.level,[0,4,8,12,16])
        self.speed = 30
        self.raceString = ""
        self.classAsString = inp.classAsString
        self.resistances = ""
        self.name= inp.name
        
        gf.applyBackground(self,inp.backgroundAsString)
        self.stuff = inp.stuff
        
        # this includes things like defence fighting style, cloaks of protection ect.
        self.cumulativeACBonus = 0
        # these are static AC options without shield / other stacking bonuses. eg. warforged / tortle
        self.baseACOptions = [inp.AC]
        self.equippedArmor = None
        self.wearingShield = inp.wearingShield
        self.calculateAC()
        
        # class specific booleans
        self.proficientWithShields = False
        self.ritualCaster = False
            
        
        self.costDic = {
            "1": "1st-level-spell",
            "2": "2nd-level-spell",
            "3": "3rd-level-spell",
        }
        
        # hitDie is not initaliased here, type of sheet has to have already initalised it
        self.hpBoost = 0
        self.hp = getHp(self.hitDie,self.level,self.modifiers[2])

        
        
        # dynamic sections of blocks that build the page, at the very end
        self.leftColumnBlocks = []
        self.middleColumnBlocks = []
        self.rightColumnBlocks = []
        
        # dynamic blocks that are in every class, and customisable attributes for each
        self.charInfos = []
        self.highlightedEntries = []
        self.highlightedBlockIndex = 0
        self.reactions=[]
        self.reactionLocationCommand = "leftCol"
        self.bonusActionEntries = []
        self.bonusActionLocationCommand = "rightCol"
        self.actionEntries = []

        # ok race input is a data structure that is a string split by "?", the first argument is the name of the race - the key that finds the race function
        self.size = None
        defaultRaceString = "human"
        if inp.race in [None,""]:
            self.race = defaultRaceString
        elif type(inp.race) == str :
            self.race=inp.race
        else:
            print("ok I did not recognise this race becuase it is the wrong data type", inp.race)
            self.race = defaultRaceString
        
        raceArgs = self.race.split("?")
        race = raceArgs.pop(0)
        
        if not race in raceFunctions.races.keys():
            print("ok I did not recognise this race command, its not one of the keys ", inp.race)
            self.race = defaultRaceString
            raceArgs = self.race.split("?")
            race = raceArgs.pop(0)
            
        raceFunctions.races[race](self, raceArgs)
        

        # add the blocks and entries that each class has (can be deleted if necessary)
        self.reactions.append(bl.TextEntry("oppAttack"))
        textActionsForEveryClass = ["Dash","Disengage","Dodge"]
        for textAction in textActionsForEveryClass:
            self.actionEntries.append(bl.TextEntry(textAction))
    
    def addResistance(self,r):
        
        if not r in self.resistances:
            if self.resistances == "":
                self.resistances = r
            else:
                self.resistances += ", "+r
                
    def calculateAC(self):
        
        options = self.baseACOptions
        options.append(10+self.modifiers[1])
        
        armorsThatWeHave = []
        bestArmor = None
        bestArmorAC = max(options)
        bestArmorObject = None
        
        
        for a in armors:
            if a in self.stuff:
                armorsThatWeHave.append(a)
        
        for a in armorsThatWeHave:
            armorObject = armor.Armor()
            armorObject.loadArmor(a)
            ac = armorObject.base
            if armorObject.addDex:
                if armorObject.maxTwo:
                    ac=ac+max(2,self.modifiers[1])
                else:
                    ac=ac+self.modifiers[1]
            if ac>bestArmorAC:
                bestArmor = a
                bestArmorAC = ac
                bestArmorObject = armorObject
        ac = None
        
        if max(options)<bestArmorAC:
            
            #lets get that armor on its great
            self.equippedArmor = bestArmorObject
            ac = bestArmorAC
            if bestArmorObject.stealthDisadvantage:
                self.skillNotes.append([16,"(disadavantage)"])
            
        else:
            ac = max(options)
        
        if self.wearingShield:
            ac = ac+2
        
        self.AC = ac  + self.cumulativeACBonus
        
    
    def updateModifiers(self):
        
        scores = self.scores
        
        
        if scores==None:
            print("Ive been asked to update scores and scores have not been set")
        elif len(scores) != 6:
            print("Theres a problem with the scores when trying to update modifiers: ",scores)
        else:
            
            self.modifiers = [0]*6
            
            for i in range(len(scores)):
                score = scores[i]
                score = score-10
                if score<0:
                    score = score-1
                
                self.modifiers[i]=int(score/2)
            
           
                    
    def loadScoresAndMods(self,preferredScores,inp):
        
        
        if inp.modifiers == None:
            print("inp.scores is ",inp.scores)
            if inp.scores == None:
                self.scores = preferredScores
            else:
                self.scores = inp.scores
            self.updateModifiers()

        else:
            if inp.scores == None:
                # ok weve got mods but no scores. #
                self.modifiers=inp.modifiers
                self.scores=[]
                for m in inp.modifiers:
                    print("ok weve got mods but no scores. #, adding ",m," to the score list")
                    self.scores.append(int(10+(m*2)))
            else:
                #weve got mods and weve got scores, lets prioritise scores I guess
                self.updateModifiers()
            
        
        
    def pickSkillProficiency(self,skillsToChooseFrom):
        
        #print()
        #print(self.classAsString)
        
        def w(l):
            k=[]
            for i in l:
                k.append(skillsAsStrings[i])
            return k 
                
        
        #print("right lets go weve got these to choose from ",w(skillsToChooseFrom), " lets pick a nice skill")
        #lets just check were not already proficient in everything to choose from
        skillsToChooseFromWeHaveAlready = []
        for s in skillsToChooseFrom:
            if s in self.skillProficiencies:
                skillsToChooseFromWeHaveAlready.append(s)
                
        if len(skillsToChooseFromWeHaveAlready)==len(skillsToChooseFrom):
            #bad news - were already skilled in everything on offer
            return None
     
        #lets take out the ones were proficient in already from our choices
        for s in skillsToChooseFromWeHaveAlready:
            skillsToChooseFrom.remove(s)
        #print("ok just whipped out the stuff were proficient already ",w(skillsToChooseFrom))
        
        # ok i think were going to have to score each fkn skill and pick the best
        
        #lets give each skill a score.
        #["Acrobatics",   "Animal Handling",  "Arcana",  "Athletics",  "Deception",  "History",  "Insight",  "Intimidation",  "Investigation",  "Medicine",  
        skillScores = [7,10,5,10,5,0,18,5,15,3]
        # "Nature",  "Perception","Performance",  "Persuasion",  "Religion",  "Sleight of Hand",  "Stealth",  "Survival",  "Thieves' Tools"]
        skillScores.extend([0,28,11,8,0,4,25,7,6])
        
        # ok some stuff is going to be more valuable to certian classes
        weCanHeal = False
        healingClasses = ["Cleric","Druid","Ranger","Paladin"]
        for h in healingClasses:
            if h in self.classAsString:
                weCanHeal = True
        if weCanHeal:
            skillScores[9]-=50
        ourSkillScores = []
        
        for s in skillsToChooseFrom:
            value = skillScores[s]
            value += int(self.modifiers[skillModifierIndex[s]]*10)
            ourSkillScores.append(value)
        
        #print("ourSkillScores", ourSkillScores)
        return skillsToChooseFrom[ourSkillScores.index(max(ourSkillScores))]
            
        
        
        
    
    def addBlockWithCommandLocation(self,block,command):
        if command == "leftCol":
            self.leftColumnBlocks.append(block)
        elif command == "midCol":
            self.middleColumnBlocks.append(block)
        elif command == "rightCol":
            self.rightColumnBlocks.append(block)
    
    
            
    def generateClassHTML(self):
        
        # bit of compiling to do at the start
        
        self.calculateAC()
        self.updateModifiers()
        
        
        #lets do stuff
        stuffEntry = bl.Entry(self.stuff)
        stuffBlock = bl.Block([stuffEntry],equipmentTitle)
        self.rightColumnBlocks.append(stuffBlock)
        
        # generate bit before, the highlighted Block, the bits after it, and add it to middle col at the index in class parameter
     
        blockBeforeHighlightedStuff = bl.Block([])
        #print("self.highlightedBlockIndex",self.highlightedBlockIndex)
        for i in range(self.highlightedBlockIndex):
            blockBeforeHighlightedStuff.addEntry(self.actionEntries[i])
        self.middleColumnBlocks.append(blockBeforeHighlightedStuff)
        
        highLightedBlock = bl.Block(self.highlightedEntries, "","attack01")
        self.middleColumnBlocks.append(highLightedBlock)
        
        blockAfterHighlightedStuff = bl.Block([])
        for i in range(self.highlightedBlockIndex,len(self.actionEntries)):
            blockAfterHighlightedStuff.addEntry(self.actionEntries[i])
        self.middleColumnBlocks.append(blockAfterHighlightedStuff)
        
        
        #generateReactionBlock, add it to the (end of the) chosen column, as per parameter at start
        reactionBlock = bl.Block(self.reactions,"REACTIONS (1 per round)")
        self.addBlockWithCommandLocation(reactionBlock,self.reactionLocationCommand)
        
        #generate charinfos Block, and put it at the top of right column
        charInfoCount = len(self.charInfos)
        if charInfoCount>0:
            
            # puts bullet points in if the character is short of info 
            """for i in range(3-charInfoCount):
                self.charInfos.append(bl.Entry(infoBullet))"""
                
            charInfoBlock = bl.Block(self.charInfos,"CHARACTER INFORMATION")
            self.rightColumnBlocks.insert(0,charInfoBlock)
        
        # generateBonusActionBlock
        if len(self.bonusActionEntries)>0:
            
            bonusActionBlock = bl.Block(self.bonusActionEntries,bonusActionTitle)
            self.addBlockWithCommandLocation(bonusActionBlock,self.bonusActionLocationCommand)
        
        
        
        
        result=""
        result += "<!DOCTYPE html>\n"
        result += "<html>\n"
        result += "<head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>\n"
        result += "<title>"+self.classAsString+"</title>\n"
        result += writeStyle()
        result += self.generateHeaderHTML()
        result += self.generatemodifierHTML()
        result += self.generateSaveHTML()
        result += self.generateSkillHTML()
        
        result +="<div id='reactions'>"
        for block in self.leftColumnBlocks:
            result += block.getHTML(self)
        result +="</div>"
        
        result += self.writeUpperCentralColumn()
        
        
        result +="<div id='labelattackactions'>ACTIONS (1 per turn)</div>\n"
        result +="<div id='attackactions'>\n"
        
        for block in self.middleColumnBlocks:
            result += block.getHTML(self)
        result +="</div >\n"
        result +="<div id='specialabilities'>\n"
        
        for block in self.rightColumnBlocks:
            result += block.getHTML(self)
        
        result +="</div>\n"
        result +="</div>\n"
        result +="</div>\n"
        result +="</body>\n"
        result +="</html>\n"
        
        
        return result
    
    
    
    def generateSkillHTML(self):
    
        
        mods = self.modifiers[:]
        profs = self.skillProficiencies
        p = self.profBonus
        
        result = "<div id='skills'>\n"
        
        skillMods = []

        if 18 in profs:
            skillMods = [0]*len(skillsAsStrings)
        else:
            skillMods = [0]*(len(skillsAsStrings)-1)
        
        for i in range(len(skillMods)):
            skillMods[i] = mods[skillModifierIndex[i]]
        
        for prof in profs:
            skillMods[prof]+=p
        for expertise in self.skillExpertises:
            skillMods[expertise]+=p
        for skillBoost in self.skillBoosts:
            skillMods[skillBoost[0]]+=skillBoost[1]
            
        lines = []
        
        
        for i in range(len(skillMods)):
            line = skillsAsStrings[i]+" "
            line+=gf.getSignedStringFromInt(skillMods[i],True)
            if i in profs:
                line+=" *"
            if i in self.skillExpertises:
                line+="*"
            lines.append(line)
        
        for note in self.skillNotes:
            lines[note[0]]=lines[note[0]]+" <em>"+note[1]+"</em>"
                
        for i in range(len(lines)):
            lines[i]=lines[i]+" <br>\n"
        
        for line in lines:
            result+=line
        
        result+="\n<br>* <em>proficient</em><br>\n"
        if len(self.skillExpertises)>0:
            result+="** <em>expert</em><br>\n"
        result+="</div>\n\n"
        
        
        return(result)
        
    def generateSaveHTML(self):
    
        
        mods = self.modifiers[:]
        profs = self.saveProficiencies
        p = self.profBonus
        
        result = "<div id='savingthrows'>\n"
        
        saveMods = [0]*len(savesAsStrings)
        
        
        for i in range(len(saveMods)):
            saveMods[i] = mods[i]
        
        for prof in profs:
            saveMods[prof]+=p
            
        for saveBoost in self.saveBoosts:
            saveMods[saveBoost[0]]+=saveBoost[1]
            
        lines = []
        
        for i in range(len(saveMods)):
            line = savesAsStrings[i]+" "
            line+=gf.getSignedStringFromInt(saveMods[i],True)
            if i in profs:
                line+=" *"
            lines.append(line)
        
        for note in self.saveNotes:
            lines[note[0]]=lines[note[0]]+" <em>"+note[1]+"</em>"
                
        for i in range(len(lines)):
            lines[i]=lines[i]+" <br>\n"
        
        for line in lines:
            result+=line
        
        
        result+="</div>\n\n"
        
        
        return(result)
    
    def writeUpperCentralColumn(self):
    
        result = ""
        result+= "<div id='upperCentralColumn'>\n"
        result+= "<div id='labelArmorClass'>ARMOR<br>CLASS<br>(AC)</div><div id='armorclass'>"+str(self.AC)+"</div>\n"
        result+= "<div id='labelSpeed'>SPEED</div><div id='speed'>"+gf.getDistanceString(self.speed)+"</div>\n"
        result+= "<div id='labelHitPoints'>HIT POINTS</div>\n"
        result+= "<div id='hitpoints'>"+str(self.hp)+"</div>\n"
        result+= "</div>\n"
        
        return result
    
    def generatemodifierHTML(self):
        modifiers = self.modifiers
        
        strScoreString = ""
        dexScoreString = ""
        conScoreString = ""
        intScoreString = ""
        wisScoreString = ""
        chaScoreString = ""
        
        if self.showScores:
            strScoreString = "<div id='STRscore'>"+str(self.scores[0])+"</div>"
            dexScoreString = "<div id='DEXscore'>"+str(self.scores[1])+"</div>"
            conScoreString = "<div id='CONscore'>"+str(self.scores[2])+"</div>"
            intScoreString = "<div id='INTscore'>"+str(self.scores[3])+"</div>"
            wisScoreString = "<div id='WISscore'>"+str(self.scores[4])+"</div>"
            chaScoreString = "<div id='CHAscore'>"+str(self.scores[5])+"</div>"
        
        result = "\n"
        result+= "<div id='labelSTR'>STR</div><div id='STRmodf'>"+gf.getSignedStringFromInt(modifiers[0])+"</div>"+strScoreString+"\n"
        result+= "<div id='labelDEX'>DEX</div><div id='DEXmodf'>"+gf.getSignedStringFromInt(modifiers[1])+"</div>"+dexScoreString+"\n"
        result+= "<div id='labelCON'>CON</div><div id='CONmodf'>"+gf.getSignedStringFromInt(modifiers[2])+"</div>"+conScoreString+"\n"
        result+= "<div id='labelINT'>INT</div><div id='INTmodf'>"+gf.getSignedStringFromInt(modifiers[3])+"</div>"+intScoreString+"\n"
        result+= "<div id='labelWIS'>WIS</div><div id='WISmodf'>"+gf.getSignedStringFromInt(modifiers[4])+"</div>"+wisScoreString+"\n"
        result+= "<div id='labelCHA'>CHA</div><div id='CHAmodf'>"+gf.getSignedStringFromInt(modifiers[5])+"</div>"+chaScoreString+"\n\n"
        return result
    
    def generateHeaderHTML(self):
    
        result = ""
        result+= "<body><div class='wrp'><div id='charsheet01'>\n\n"
        result+= "<div id='charactername'>"+self.name+"</div>\n"
        result+= "\n"
        result+= "<div id='topBanner'>\n"
        result+= "\n"
        result+= "<div id='classlabel'>CLASS</div>\n"
        result+= "<div id='class'>"+self.classAsString+"</div>\n"
        if self.size != None:
            result+= "<div id='size'>"+str(self.size)+"</div>\n"
            result+= "<div id='sizeLabel'>SIZE</div>\n"

        result+= "<div id='labelrace'>RACE</div>\n"
        result+= "<div id='race'>"+self.raceString+"</div>\n"
        result+= "<div id='labelbackground'>BACKGROUND</div>\n"
        result+= "<div id='background'>"+self.backgroundAsString+"</div>\n"
        
        if self.resistances!="":
            
            result+= "<div id='topRightText'>"+self.resistances+"</div>\n"
            result+= "<div id='topRightLabel'>"+"RESISTANCES"+"</div>\n"
        
        #result+= "<div id='bottomRightLabel'>"+""+"</div>\n"
        #result+= "<div id='bottomRightText'>"+""+"</div>\n"
        # top banner is done
        result+= "</div>\n"
        result+= "\n"
    
        result+= "<div id='labelSavingThrows'>SAVING&nbsp;THROWS</div>\n"
        result+= "<div id='labelSkills'>SKILL CHECKS</div>\n"
        
        return result

    def getHp(self,hitDie,level, conMod):
        hp = hitDie+conMod+self.hpBoost
        hpPerLevel = int((hitDie/2)+1)+conMod
        hp+=hpPerLevel*(level-1)
        return hp
    
        

def getHp(hitDie,level, conMod,hpBoost=0):
    hp = hitDie+conMod
    hpPerLevel = int((hitDie/2)+1)+conMod
    hp+=hpPerLevel*(level-1)
    return hp



def writeStyle():
    f = open(gf.pathToSource+"styleText.html", "r")
    return f.read()

