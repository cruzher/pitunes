
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
        $('#box').append('<h2>Adding playlist</h2>');
        $('#box').append('<span class="box-text">The name of the playlist exceeds 19 characters and you need to enter an alias to show in the LCD</span>');
        $('#box').append('<form method="post" action="action.php" id="playlist_alias">');
        $('#box').append('<input type="text" name="playlist_alias">');
        $('#box').append('<input type="hidden" name="playlist_name" value="'+playlist+'">');
        $('#box').append('<input type="submit" value="Save">');
        $('#box').append('</form>');

        $( "#playlist_alias" ).submit(function( event ) {
            event.preventDefault();
            alert("mekk");
            $.post( "action.php", $( "#playlist_alias" ).serialize(), function(data) {
                alert(data.OK);
            }, "json");
        });
    } else {
        $.post( "action.php", {"playlist_alias": '', "playlist_name": playlist}, function(data) {
            alert(data.OK);
        }, "json");
    }
}

function removePlaylist(playlist) {

}

