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