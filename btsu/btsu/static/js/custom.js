$(document).ready(function() {
    $("#search_warning").hide();
    $("#progress_bar").hide();
    $("#search_btn").click(function(){
        $("#search_warning").show();
        $("#progress_bar").show();
    });
});