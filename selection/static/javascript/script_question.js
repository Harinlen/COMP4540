//Disable the dimmer.
$.fn.dimmer.settings.closable=false;
//Initial widgets.
$('#answer-combo').dropdown();
$('#answer-range').range();
//Variables.
var questionWidget="";
var questionIndex=0;
//Hide all the widgets.
$('#answer-combo').transition('hide');
document.getElementById('answer-combo').classList.add('hidden_widget');
$('#answer-line-text').transition('hide');
$('#answer-range').transition('hide');
$('#answer-range-data').transition('hide');
$('#answer-radio-list').transition('hide');
$('#answer-checkbox-list').transition('hide');
//Hide question area and submit button.
$('#next-button-area').transition('hide');
$('#queation-area').transition('hide');

//Update range function.
function updateAnswerValue(value) {
  $('#answer-range-value').html(value);

  //Disable the next button.
  var nextButton=document.getElementById('next-button');
  nextButton.classList.remove('disabled');
}

function hideAnswerCombo() {
    document.getElementById('answer-combo').classList.add('hidden_widget');
}

function onNextAnimationFinished() {
    //Increase the question index.
    ++questionIndex;
    //Check index.
    if(questionIndex==questionTypes.length) {
        $('#submit-dimmer').dimmer('show');
    } else {
        prepareAndShowQuestion();
    }
}

function onNextPressed() {
    if(questionType==0) {
        $('#answer-combo').transition({
            animation: 'fade up',
            onComplete: hideAnswerCombo
        });
    } else if(questionType==1){
        $('#answer-line-text').transition('fade up');
    } else if(questionType==2) {
        $('#answer-range').transition('fade up');
        $('#answer-range-data').transition('fade up');
    } else if(questionType==3) {
        $('#answer-radio-list').transition('fade up');
    } else if(questionType==4) {
        $('#answer-checkbox-list').transition('fade up');
    }
    //Hide the question area, submit button.
    $('#next-button-area').transition('fade up');
    $('#queation-area').transition({
        animation: 'fade down',
        onComplete: onNextAnimationFinished
    });
}

function generalNextCheck() {
    //Disable the next button.
    var nextButton=document.getElementById('next-button');
    nextButton.classList.remove('disabled');
}

function inputBoxNextCheck() {
    //Check the value.
    var inputBoxValue=document.getElementById('answer-line-text-input').value;
    //Check length.
    var nextButton=document.getElementById('next-button');
    if(inputBoxValue.length==0) {
        nextButton.classList.add('disabled');
    } else {
        nextButton.classList.remove('disabled');
    }
}

function prepareAndShowQuestion() {
    //Prepare the current question.
    questionType=questionTypes[questionIndex];
    questionText=questionTexts[questionIndex];
    questionExplain=questionExplains[questionIndex];
    questionSetting=questionSettings[questionIndex];
    //Set the content of the widget.
    document.getElementById('question-text').innerHTML=questionText;
    document.getElementById('question-explain').innerHTML=questionExplain;
    //Set the question widget.
    if(questionType==0) {
        //Set the question widget.
        questionWidget="answer-combo";
        document.getElementById('answer-combo-default-text').innerHTML=questionSetting["defaultText"];
        //Remove all the current combo element child.
        var comboElement=document.getElementById('answer-combo-menu');
        while(comboElement.firstChild) {
            comboElement.firstChild.removeEventListener("click", generalNextCheck, false);
            comboElement.removeChild(comboElement.firstChild);
        }
        var itemList=questionSetting["values"];
        for(var i=0; i<itemList.length; ++i) {
            var current_item=itemList[i];
            var current_element=document.createElement('div');
            current_element.classList.add('item');
            current_element.setAttribute('data-value', current_item[1]);
            current_element.innerHTML=current_item[0];
            current_element.addEventListener("click", generalNextCheck, false);
            comboElement.appendChild(current_element);
        }
        //Show the answer combo.
        document.getElementById('answer-combo').classList.remove('hidden_widget');
        $('#answer-combo').transition('fade up');
    } else if(questionType==1){
        questionWidget="answer-line-text";
        var editElement=document.getElementById('answer-line-text-input');
        editElement.setAttribute("placeholder", questionSetting["defaultText"]);
        editElement.value="";
        $('#answer-line-text').transition('fade up');
    } else if(questionType==2) {
        questionWidget="answer-range";
        $('#answer-range').range({
            min: questionSetting["min"],
            max: questionSetting["max"],
            start: questionSetting["min"],
            onChange: updateAnswerValue});
        $('#answer-range').transition('fade up');
        $('#answer-range-data').transition('fade up');
    } else if(questionType==3) {
        questionWidget="answer-radio-list";
        var candidateList=questionSetting["values"];
        var listArea=document.getElementById('answer-radio-list-area');
        while(listArea.firstChild){
            listArea.firstChild.removeEventListener('click', generalNextCheck, false);
            listArea.removeChild(listArea.firstChild);
        }
        for(var i=0; i<candidateList.length; ++i) {
            var candidateField=document.createElement('div');
            candidateField.classList.add('field');
            candidateField.addEventListener('click', generalNextCheck, false);
            var candidateItem=document.createElement('div');
            candidateItem.classList.add('ui');
            candidateItem.classList.add('radio');
            candidateItem.classList.add('checkbox');
            var candidateInput=document.createElement('input');
            candidateInput.setAttribute('name', 'question-field');
            candidateInput.setAttribute('type', 'radio');
            candidateItem.appendChild(candidateInput);
            var candidateValue=document.createElement('label');
            candidateValue.innerHTML=candidateList[i];
            candidateItem.appendChild(candidateValue);
            candidateField.appendChild(candidateItem);
            listArea.appendChild(candidateField);
        }
        $('#answer-radio-list').transition('fade up');
    } else if(questionType==4) {
        questionWidget="answer-checkbox-list";
        var candidateList=questionSetting["values"];
        var listArea=document.getElementById('answer-checkbox-list-area');
        while(listArea.firstChild){
            listArea.firstChild.removeEventListener('click', generalNextCheck, false);
            listArea.removeChild(listArea.firstChild);
        }
        for(var i=0; i<candidateList.length; ++i) {
            var candidateField=document.createElement('div');
            candidateField.classList.add('field');
            candidateField.addEventListener('click', generalNextCheck, false);
            var candidateItem=document.createElement('div');
            candidateItem.classList.add('ui');
            candidateItem.classList.add('checkbox');
            var candidateInput=document.createElement('input');
            candidateInput.setAttribute('name', 'question-field');
            candidateInput.setAttribute('type', 'checkbox');
            candidateItem.appendChild(candidateInput);
            var candidateValue=document.createElement('label');
            candidateValue.innerHTML=candidateList[i];
            candidateItem.appendChild(candidateValue);
            candidateField.appendChild(candidateItem);
            listArea.appendChild(candidateField);
        }
        $('#answer-checkbox-list').transition('fade up');
    }
    //Show the question area, submit button.
    $('#next-button-area').transition('fade up');
    $('#queation-area').transition('fade down');
    //Disable the next button.
    var nextButton=document.getElementById('next-button');
    nextButton.classList.add('disabled');
}

//Check question type
$(document).ready(function() {
    //Link next button.
    var nextButton=document.getElementById('next-button');
    nextButton.addEventListener("click", onNextPressed, false);
    //Link input box.
    var inputBox=document.getElementById('answer-line-text-input');
    inputBox.oninput=inputBoxNextCheck;
    //Reset the index.
    questionIndex=0;
    //Start the first question.
    prepareAndShowQuestion();
});
