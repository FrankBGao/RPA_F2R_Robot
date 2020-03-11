$(document).ready(function () {
    $("#sendCommand").click(function () {
        $("#result").text("waiting");
        var value ={
            Command: $("#Command").val()
        };
        $.post("/Commander",value, function returnResult(result,statue) {
             $("#result").text(result)
        });

    });
    $("#SaveCommand").click(function () {
        $("#result").text("Saving");
        var value ={
                Command:$("#Command").val(),
                Name:$("#commandName").val()
        };
        $.post("/Save",value, function returnResult(result,statue) {
             $("#result").text(result)
        });

    });

    $("a[id^='RunThis']").click(function () {
        $("#result").text("waiting");
        var value ={
            Command: this.parentElement.innerText.replace(/RunThis\n/,"")
        };
        $.post("/Commander",value, function returnResult(result,statue) {
             $("#result").text(result)
        });

    });
});