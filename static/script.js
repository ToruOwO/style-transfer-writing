$('#translateButton').click(function(){
    document.getElementById("shakespeareanEnglish").innerHTML = document.getElementById("modernEnglish").value;
});

$(function() {
    $('#translateButton').click(function() {
        console.log("clicked");
        $.ajax({
            type: "POST",
            url: "/translate",
            data: $('textarea#modernEnglish').val(),
            success: function(result) {
                console.log("ojbk");
            }
        });
    });
});