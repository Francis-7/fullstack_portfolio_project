$(document).ready(function() {
    // Set iframe attributes when the show instance method is called
    $("#videoModal").on("show.bs.modal", function(event) {
        let button = $(event.relatedTarget); // Button that triggered the modal
        let url = button.data("video");      // Extract url from data-video attribute
        $(this).find("iframe").attr({
            src : url,
            allow : "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
        });
    });

    // Remove iframe attributes when the modal has finished being hidden from the user
    $("#videoModal").on("hidden.bs.modal", function() {
        $("#videoModal iframe").removeAttr("src allow");
    });
});