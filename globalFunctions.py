infoBullet = ""


# args is the list of arguments passed in - for example if you want your attribues somewhere specific with attBoost arguments
# default boosts is [int,int,int,int,int,int] with a different int for the places the race 'naturally' boosts, without TCoE variant.
# defaultBoosts UNCHECKED? dont let anyone make their own race i guess - use args instead
# this also returns the score boosts as a list
def addScoreBonuses(c,args, defaultBoosts):
    print("adding score bonuses")
    scoresBoosted = [0]*6
    
    tash = c.tashaContent
    
    if not tash:
        for i in range(6):
            c.scores[i]+=defaultBoosts[i]
            scoresBoosted[i]+=defaultBoosts[i]
    else:
        
        boostsAddedFromArgs = False
        
        for a in args:
            
            # ok this would allow a sneaky input to do something like attBoost-0-1000 to get massive strength.
            # never trust power gamers! ill leave it as it is for now though
            
            if "attBoost" in a and "-" in a:
                x = a.split("-")
                
                targetAttributeString = x[1]
                targetAttributeInt = None
            
                try:
                    i = int(targetAttributeString)
                    if not i in range(5):
                        raise ValueError
                    targetAttributeInt = i
                    varHuman = True
                    
                except:
                    print("ok i just tried to make this an int and it failed ",x[1])
                    
                amount = 1
                
                if len(x)>2:
                    try:
                        i = int(x[2])
                        amount+=i
                    except:
                        print("ok i just tried to make this an int and it failed ",x[2])
                
                scoresBoosted[targetAttributeInt]+=amount
                c.scores[targetAttributeInt]+=amount
                boostsAddedFromArgs = True
                
        if not boostsAddedFromArgs:
            #print(" ok no boost from args so well pick where they go")
            # ok ive guess weve got to pick them then innit, tashas allows us to move them and the input hasnt told us where to pop them
            defaultBoosts.sort()
            defaultBoosts.reverse()
            #print("the boosts weve got to allocate here (in no particular order - thanks to tasha) is ",defaultBoosts)
            priorityList = c.attributePriorityList[:]
            for b in defaultBoosts:
                if b> 2:
                    print("weve just got a racial boost of ",b," and its more than two so were ignoring it sorry!")
                elif b>0:
                    print(" this boost is more than 0 its ", b," lets see where to get it added")
                    l = chooseAttributesToIncreaseBy(c,b,False,priorityList)
                    print(" ok we picked ",l)
                    priorityList.remove(l[0])
                    
                    for a in l:
                        scoresBoosted[a]+=1
                        c.scores[a]+=1
    c.updateModifiers()
    print("c.hitDie,c.level,c.modifiers[2]  is ",c.hitDie,c.level,c.modifiers[2])
    c.hp = c.getHp(c.hitDie,c.level,c.modifiers[2])
    print("c.hitDie,c.level,c.modifiers[2]  is ",c.hitDie,c.level,c.modifiers[2])
    return scoresBoosted
            
    

# returns a list of integers that index attributes that should be incremented by 1. this does not consider hard cap of 20, or consider boosts of more than 2. racial +2s cannot be split.
# this structure is a bit odd, as is the function really
# this wont break as long as theres one item in priority list I suppose
def chooseAttributesToIncreaseBy(c,numberOfBoosts, canSplitBoosts = True, betterPriorityList = []):
    
    p = c.attributePriorityList
        
    if len(betterPriorityList)!=0:
        p = betterPriorityList
    
    
    s = c.scores[:]
    
    result = []

    if numberOfBoosts==2:
        if s[p[0]]%2==0:
            # weve got an even top score and two to increase by - lets boost main stat
            return [p[0],p[0]]
        else:
            # weve got an odd top score and two to increase by. can we split it?
            if not canSplitBoosts:
                return [p[0],p[0]]
            else:
                # ok were going to boost main stat by one, then crack on as if we only dealing with one boost.
                result.append(p[0])
                s[p[0]]=s[p[0]]+1
                numberOfBoosts = numberOfBoosts-1
            
    
    if numberOfBoosts ==1:
        
        highestOddPriority = None
        highestOddPriorityIndex = None
        foundOne = False
        i = 0
        
        # lets go through each attribute in terms of priority and record the first one thats odd
        for a in p:
            
            if c.scores[a]%2!=0 and not foundOne:
                foundOne = True
                highestOddPriority = a
                highestOddPriorityIndex = i
            i = i+1
            
        # if none of them are odd, lets add the +1 to our top priority
        if highestOddPriority == None:
            result.append(p[0])
            
        # ok if weve got an odd score in an attribute that is only a fourth priority, lets forget about it and boost main stat instead
        elif highestOddPriorityIndex > 2:
            result.append(p[0])
            
        else:
            result.append(p[highestOddPriorityIndex])
    
    return result
            
        
    
    
def getNumberFromRange(level,indents,start=1):
    results = [start]*20
    
    for indent in indents:
        for i in range(indent,20):
            results[i]=results[i]+1
    
    #print(results)
    return results[level-1]
    
def getSignedStringFromInt(i,ignoreZeros=False):
    if i == 0 and ignoreZeros:
        return ""
    
    if i > -1:
        return("+"+str(i))
    else:
        return(str(i))

def getDistanceString(distance,style=1):
    if distance>0:
        if style==1:
            return str(distance)+"ft"
        elif style==2:
            return str(int(distance/5))+" sqs."
    else:
        return ""

def runFuncWithList(f,lst):
    l = []
    for arg in lst:
        l.append(arg)
    
    if len(l)==1:
        return f(l[0])
    if len(l)==2:
        return f(l[0],l[1])
    if len(l)==3:
        return f(l[0],l[1],l[2])
    if len(l)==4:
        return f(l[0],l[1],l[2],l[3])
    if len(l)==5:
        return f(l[0],l[1],l[2],l[3],l[4])
    if len(l)==6:
        return f(l[0],l[1],l[2],l[3],l[4],l[5])
    if len(l)==7:
        return f(l[0],l[1],l[2],l[3],l[4],l[5],l[6])
    if len(l)==8:
        return f(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7])
    if len(l)==9:
        return f(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8])
    if len(l)==10:
        return f(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9])
    if len(l)==11:
        return f(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10])

def getDefaultGrappleTexts(meleeVerb="Punch"):
    return ["• You may only perform "+meleeVerb+" attacks while grappling.","• You move at half speed, and the grappled creature moves with you.","• The grappled creature's speed becomes 0","• You may release the target at any time."]

# listOfResourcesAndCounts is list of tuples, ordered
def getSpellSlotHTMLString(listOfResourcesAndCounts):
    s = "\n"
    for resourceAndCountTuple in listOfResourcesAndCounts:
        resourceLabel =  resourceAndCountTuple[0]
        resourceCount = resourceAndCountTuple[1]
        s+="<strong>"+resourceLabel+"s </strong>- "
        for i in range(resourceCount):
            s+="O "
        s+="<br>\n"
    #s+="<br>\n"
    return s
    
    
backgrounds = {
    "Acolyte":[6,14],
    "Charlatan":[4,15],
    "Criminal":[4,16],
    "Entertainer":[0,12],
    "Folk Hero":[1,17],
    "Guild Artisan":[6,13],
    "Hermit":[9,14],
    "Noble":[5,13],
    "Outlander":[3,17],
    "Sage":[2,5],
    "Sailor":[3,11],
    "Soldier":[3,7],
    "Urchin":[15,16]
}

def applyBackground(c,backgroundInput):
    
    if backgroundInput == "":
        # this means the input wants us to pick.
        # were just going to pick Sailor
        backgroundInput = "Sailor"
    
    c.backgroundAsString=backgroundInput
        
    if backgroundInput in backgrounds.keys():
        profs = backgrounds[backgroundInput]
        for p in profs:
            if not p in c.skillProficiencies:
                c.skillProficiencies.append(p)
            else:
                print("already proficient in ",p," so cannot add that despite background ",backgroundInput)
    else:
        print("background ",backgroundInput," does not tell us what to do, were going to just make it backgroundstring")
        

    
