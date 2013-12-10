
$(document).ready(function() {
    $( "#airplay" ).submit(function( event ) {
    	event.preventDefault();

        $.post( "action.php", $( "#airplay" ).serialize(), function(data) {
            alert(data.OK);
        }, "json");

    });

    $( "#dns" ).submit(function( event ) {
        event.preventDefault();

        $.post( "action.php", $( "#dns" ).serialize(), function(data) {
            alert(data.OK);
        }, "json");

    });

});

function addPlaylist(playlist) {
    if (playlist.length > 19 ) {
        $('body').append('<div id="box_background"></div>');
        $('body').append('<div id="box"></div>');
        $('#box').append('<h1>Add playlist to LCD</h1>');
        $('#box').append('<span class="center">The name of the playlist exceeds 19 characters and you need to enter an alias to show in the LCD</span>');
    }
}

function removePlaylist(playlist) {

}

