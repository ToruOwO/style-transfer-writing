var translateButton = document.getElementById("translateButton");

$('#sButton').click(function(){
    console.log("s-rized");
    translateButton.value = "Shakespearize";
    document.getElementById('text-one').innerHTML = "When I say:";
    document.getElementById('text-two').innerHTML = "Shakespeare says:";
});

$('#mButton').click(function(){
    console.log("modernized");
    translateButton.value = "Modernize";
    document.getElementById('text-one').innerHTML = "When Shakespeare says:";
    document.getElementById('text-two').innerHTML = "He meant:";
});

$('#translateButton').click(function(){
    document.getElementById("modernEnglish").innerHTML = document.getElementById("shakespeareanEnglish").value;
});

$(function() {
    $('#translateButton').click(function() {
        console.log("clicked");
        $.ajax({
            type: "POST",
            url: "/translate",
            data: $('textarea#shakespeareanEnglish').val(),
            success: function(result) {
                console.log("ojbk");
            }
        });
    });
});