$(function() {

    $(".member-remove").click(function() {
        var $this = $(this);

        $("#rtm-email").text($this.data("email"));
        $("#remove-team-member-email").val($this.data("email"));
        $('#remove-team-member-modal').modal("show");

        return false;
    });

});

$(function() {

    $("#monthly").click(function() {      

        $("#monthly").val(true);
        $("#weekly").val(false);
        $("#daily").val(false);
    });

    $("#weekly").click(function() {
        $("#monthly").val(false);
        $("#weekly").val(true);
        $("#daily").val(false);        
    });

    $("#daily").click(function() {
        
        
        $("#rtm-email").text($this.data("email"));
        $("#remove-team-member-email").val($this.data("email"));
        $('#remove-team-member-modal').modal("show");

        return false;
    });

});
