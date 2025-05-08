
function hideHelp(){
    showIDList(["showHelpButton"]);
    hideIDList(["help","hideHelpButton"]);
};

function showHelp(){
    hideIDList(["showHelpButton"]);
    showIDList(["help","hideHelpButton"]);
};

function showInventory(){
    showIDList(["hideInventoryButton", "inventory", "stuff"]);
    hideIDList(["showInventoryButton"]);

};
function hideInventory(){
    hideIDList(["hideInventoryButton", "inventory", "stuff"]);
    showIDList(["showInventoryButton"]);

};

function loadCoreOptions(){
    showIDList(["name","background","classAsString","race"]);
    const checkBoxes = ["showScores","tashaContent" ]
    for (let i = 0; i < checkBoxes.length; i++) {
        
        document.getElementById(checkBoxes[i]).disabled=false 
        
    };
};

function showID(id){
    document.getElementById(id).style.display='block';
    document.getElementById(id).disabled=false;
}; 

function showIDList(l){
    l.forEach(showID)
}; 

function hideID(id){
    document.getElementById(id).style.display='none';
    document.getElementById(id).disabled=true;
};
function hideIDList(l){
    l.forEach(hideID)
}; 

function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min) ) + min;
};

function setSeed(){
    
};

function wrapUp(){
    ids = ["name","classAsString","race","background","stuff"];
    ids.forEach(disableIDIfBlank);
    console.log("wrapping up");

    
    

};



function disableIDIfBlank(id){
    if (document.getElementById(id).value==""){
        document.getElementById(id).disabled=true
    }
};

const abilityIDs = ["Strength","Dexterity","Constitution","Intelligence","Wisdom","Charisma"];
function showAbilityScores(){
    showIDList(abilityIDs);
    showIDList(['abilityScores','hideScoresButton']); 
    hideIDList(['showScoresButton']);

};
function hideAbilityScores(){
    hideIDList(abilityIDs);
    hideIDList(['abilityScores','hideScoresButton']); 
    showIDList(['showScoresButton']);
    
};
function loadSpeciesOptions() {
    

};
function loadClassChoices() {
    const classChoiceIDs = ["barbarianSubclass","fighterSubclass","rogueSubclass","paladinSubclass","rangerSubclass"];
    classChoiceIDs.forEach(hideID);
    
    /* multi dimensional array, showing what to display at what level. */
    let allClassChoices = {
        "Cleric":[[],[],[],["l4-feat","l4-feat-label"]],
        "Barbarian":[[],[],["barbarianSubclass"],["l4-feat","l4-feat-label"]],
        "Fighter":[[],[],["fighterSubclass"],["l4-feat","l4-feat-label"],[],["l6-feat"]],
        "Rogue":[[],[],["rogueSubclass"],["l4-feat","l4-feat-label"]],
        "Ranger":[[],[],["rangerSubclass"],["l4-feat","l4-feat-label"]],
        "Paladin":[[],[],["paladinSubclass"],["l4-feat","l4-feat-label"]],
        "Monk":[[],[],[],["l4-feat","l4-feat-label"]],
        "Warlock":[],
        "":[]
    };
    const level = document.getElementById("level").value;
    const cls = document.getElementById("classAsString").value;
    
    const thisClassChoices = allClassChoices[cls]
    
    thisClassChoices.forEach(considerShowingClassChoices)

    function considerShowingClassChoices(value,index){
        if (index<level){
            

            value.forEach(showID);
            
        }
    }
}
