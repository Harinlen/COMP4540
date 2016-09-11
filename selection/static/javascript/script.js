//Disable the dimmer.
$.fn.dimmer.settings.closable=false;
//Initial rating widget.
$('#rating-widget-integer').rating();
$('#reading-count-down').progress();
$('#experiment-progress').progress();
$('#rating-widget-integer-radio')
.form({
    fields: {
        rating: {
            identifier: 'rating-field'
        }
    }
});
// slider Helper.
var sliderHelper=0;
$('#rating-widget-slider').range({
    min:0,
    max:100,
    start:50,
    onChange: function(val) {sliderHelper=val;}
});

var supportedWidgets=["rating-widget-boolean",
                      "rating-widget-boolean-group",
                      "rating-widget-integer-radio",
                      "rating-widget-integer",
                      "rating-widget-slider"];
var testIndex;
var testResult=[];

function updateProgress() {
    var currentValue=$('#reading-count-down').progress('get value');
    var totalValue=$('#reading-count-down').progress('get total');
    if(totalValue==currentValue) {
        $('#reading-count-down').transition({
            animation : 'fade left',
            onComplete : function() {
                $('#hint-text').transition('fade left');
                $('#'+supportedWidgets[testList[testIndex]]).transition({
                    animation : 'fade right',
                    onComplete : function() {
                        $('#next-image').transition('fade down');
                    }
                });
            }
        });
        return;
    }
    $('#reading-count-down').progress('increment');
    window.setTimeout(updateProgress, 1000);
}

function onStartClick() {
    //Hide the dimmer.
    $('#instruction-dimmer').dimmer('hide');
    //Start test case.
    window.setTimeout(function(){
        setTestCases();
    }, 1000);
}

function onNextClick() {
    //Check the current value is valid or not.

    $('#obvserve-item').transition('fade down');
    $('#hint-text').transition('scale');
    $('#'+supportedWidgets[testList[testIndex]]).transition('scale');
    $('#next-image').transition({
        animation : 'fade up',
        onComplete : function() {
            //Prepare the score variables.
            var imageScore=0;
            //Check current index value.
            if(testList[testIndex]==0) {
                //Boolean widget.
                var targetWidget=document.getElementById("rating-widget-boolean");
                if(targetWidget.classList.contains("active")) {
                    imageScore=100;
                }
            }
            else if (testList[testIndex]==1) {
                //Boolean group.
                var targetWidget=document.getElementById("rating-group-button-like");
                if(targetWidget.classList.contains("red")) {
                    imageScore=100;
                }
            }
            else if(testList[testIndex]==2) {
                //Integer radio.
                if($('#rating-radio-1').checkbox('is checked')==true) {
                    imageScore=20;
                }
                else if($('#rating-radio-2').checkbox('is checked')==true) {
                    imageScore=40;
                }
                else if($('#rating-radio-3').checkbox('is checked')==true) {
                    imageScore=60;
                }
                else if($('#rating-radio-4').checkbox('is checked')==true) {
                    imageScore=80;
                }
                else if($('#rating-radio-5').checkbox('is checked')==true) {
                    imageScore=100;
                }
            }
            else if(testList[testIndex]==3){

                //Integer heart.
                imageScore=$("#rating-widget-integer").rating("get rating")*10;
            }
            else if(testList[testIndex]==4){
                //Slider.
                imageScore=sliderHelper;
            }
            testResult.push(imageScore);

            //Increase the index.
            testIndex=testIndex+1;
            //Check the index.
            if(testIndex<testList.length) {
                //Increase the progress bar.
                $('#experiment-progress').progress('increment');
                //Reset the count down.
                $('#reading-count-down').progress('reset');
                //Start to view next image.
                startNewIteration();
            }
            else {
                //Increase the progress bar.
                $('#experiment-progress').progress('increment');
                // Show submit dimmer.
                $('#submit-dimmer').dimmer('show');
                alert(testResult);
            }
        }
    });
}

function startNewIteration() {
    //Reset the widget.
    //  Boolean button.
    document.getElementById("rating-widget-boolean").classList.remove("active");
    //  Boolean button group.
    document.getElementById("rating-group-button-like").classList.remove("red");
    document.getElementById("rating-group-button-dislike").classList.remove("black");
    //  Integer.
    $("#rating-widget-integer").rating("set rating", 5);
    //  Slider.
    $('#rating-widget-slider').range("set value", 50);
    //Update the image src.
    document.getElementById("obvserve-item").src=testImage[testIndex];
    document.getElementById("hint-text").innerHTML=testHintText[testIndex];
    //Wait for one second, then launch the animation.
    window.setTimeout(function(){
        //Start animations.
        $('#reading-count-down').transition('scale');
        $('#obvserve-item').transition({
            animation : 'fade down',
            onComplete : function() {
                window.setTimeout(updateProgress, 1000);
            }
        });
    }, 1000);
}

function setTestCases() {
    //Reset the current index.
    testIndex=0;
    //Update the experiment progress bar.
    var testListLength=testList.length;
    $('#experiment-progress').progress({progress: 0,
                                       total: testListLength});
    //Start new iteration.
    startNewIteration();
}

function startUp() {
    //Update the animations.
    $('#rating-widget-boolean').transition('hide');
    $('#rating-widget-boolean-group').transition('hide');
    $('#rating-widget-integer').transition('hide');
    $('#reading-count-down').transition('hide');
    $('#next-image').transition('hide');
    $('#obvserve-item').transition('hide');
    $('#rating-widget-slider').transition('hide');
    $('#submit-generating').transition('hide');
    $('#submit-downloading').transition('hide');
    $('#rating-widget-integer-radio').transition('hide');
    $('#hint-text').transition('hide');
    $('#submit-dimmer').dimmer('hide');

    $('#rating-widget-boolean').state({
        text: {
            inactive : '<i class="heart icon"></i>Like',
            active : '<i class="heart icon"></i>Like'
        }
    });

    var groupLikeButton=document.getElementById("rating-group-button-like");
    var groupDislikeButton=document.getElementById("rating-group-button-dislike");
    groupLikeButton.addEventListener("click", function(){
        groupDislikeButton.classList.remove("black");
        groupLikeButton.classList.add("red");
    }, false);
    groupDislikeButton.addEventListener("click", function(){
        groupDislikeButton.classList.add("black");
        groupLikeButton.classList.remove("red");
    }, false);

    //Initial start button.
    var startButton=document.getElementById("start-experiment");
    startButton.addEventListener("click", onStartClick, false);

    //Initial switch button.
    var nextButton=document.getElementById("next-image");
    nextButton.addEventListener("click", onNextClick, false);

    //Show the instruction dimmer.
    $('#instruction-dimmer').dimmer('show');
}

$(document)
    .ready(startUp);
