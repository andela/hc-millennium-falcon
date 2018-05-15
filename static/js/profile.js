$(function() {

    $(".member-remove").click(function() {
        var $this = $(this);

        $("#rtm-email").text($this.data("email"));
        $("#remove-team-member-email").val($this.data("email"));
        $('#remove-team-member-modal').modal("show");

        return false;
    });

    var $xm = $("#invite-team-member-modal");
    $xm.on("click", "#toggle-all", function() {
        var value = $(this).prop("checked");
        $xm.find(".toggle").prop("checked", value);
        console.log("bbb", value);

    });

});