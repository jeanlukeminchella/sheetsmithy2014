from dataclasses import dataclass
import Class as sh

class Input():
    
    def __init__(self, level,classAsString):
        
        self.level = level
        self.classAsString=classAsString
        self.backgroundAsString=""
        self.modifiers = None
        self.scores = None
        self.AC= 10
        self.profs=[]
        self.exps=[]
        self.race=None
        self.showScores = False
        self.stuff = ""
        self.choices = [None]*20
        self.wearingShield = False
        self.name=""
        
        self.showScores = False
        self.tashaContent = False

    # takes a string as a label for the attribute, then changes it to value. input probably needs checking like
    def changeAttribute(self, attributeLabel, value):
        if attributeLabel == "level":
            a = None
            try:
                a = int(value)
                if a<1:
                    a = 1
                if a>6:
                    a = 6
                self.level = a
            except:
                a = 1
        elif attributeLabel == "classAsString":
            self.classAsString = value
        elif attributeLabel == "backgroundAsString":
            self.backgroundAsString = value
        elif attributeLabel == "modifiers":
            self.modifiers = value
        elif attributeLabel == "scores":
            self.scores = value
        elif attributeLabel == "stuff":
            self.stuff = value
        elif attributeLabel == "choices":
            self.choices = value
        elif attributeLabel == "wearingShield":
            try:
                self.wearingShield = bool(value)
            except:
                self.wearingShield = False
                
        elif attributeLabel == "race":
            self.race = value
        elif attributeLabel == "showScores":
            try:
                self.showScores = bool(value)
            except:
                self.showScores = False
                
        elif attributeLabel == "race":
            self.race = value
        elif attributeLabel == "tashaContent":
            self.tashaContent = value
        elif attributeLabel == "name":
            self.name = value
            
            
        
        else:
            print("attribute label ",attributeLabel," not found while trying to change it on input for ",self.classAsString)
    
    # takes list of [[attributeLabel,value]] and load it into self
    def loadInput(self,commands):
        for command in commands:
            self.changeAttribute(command[0],command[1])
        
    