
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
    $( "#update_system" ).submit(function( event ) {
        event.preventDefault();

        $("#update_button").attr('value', 'Updating...');

        $.post( "action.php", {"update_system": '1'}, function(data){
            alert(data.OK);
            $("#update_button").attr('value', 'Update now');
        }, "json");
    });

    //Bind event to changing network mode.
    $('input[type=radio][name=lan_status]').change(function() {
        if (this.value == '1') {
            $("#lan_box").empty();
            $("#lan_box").append('<span class="label">IP-address</span><br>');
            $("#lan_box").append('<span>0.0.0.0</span><br>');
            $("#lan_box").append('<span class="label">Netmask</span><br>');
            $("#lan_box").append('<span>0.0.0.0</span><br>');
            $("#lan_box").append('<span class="label">Gateway</span><br>');
            $("#lan_box").append('<span>0.0.0.0</span><br>');
            $("#lan_box").append('<input type="submit" value="Save">');
        }
        else if (this.value == '2') {
            $("#lan_box").empty();
            $("#lan_box").append('<input type="text" name="lan_ip" value="" placeholder="IP-address"><br>');
            $("#lan_box").append('<input type="text" name="lan_netmask" value="" placeholder="Netmask"><br>');
            $("#lan_box").append('<input type="text" name="lan_gateway" value="" placeholder="Gateway"><br>');
            $("#lan_box").append('<input type="submit" value="Save">');
        }
    });

});

function addPlaylist(id, playlist) {
    var alias = "";
    var lcd_id = "#"+id+"_lcd";
    var alias_id = "#"+id+"_alias";
    var playlist_id = "#"+id+"_playlist";

    if (playlist.length > 19 ) {
        var alias = prompt("\""+playlist+"\"exceeds 19 characters, please enter an alias.", "");
        while (alias.length == 0 || alias.length > 19) {
            var alias = prompt("Aliases can't be longer than 19 characters, please choose a shorter alias.", "");
        }
    } else {
        var alias = prompt("You can enter an alias for the playlist otherwise leave blank.", "");
    }

    if (alias.length == 0) {
        alias = playlist;
    }

    $.post( "action.php", {"add_playlist": '1', "playlist_alias": alias, "playlist_name": playlist});

    //Updating table on page.
    $(lcd_id).empty();
    $(lcd_id).append('<a href="javascript:removePlaylist('+id+', \''+playlist+'\');">yes</a>')
    $(alias_id).empty();
    $(alias_id).append('<span>'+alias+'</span>');
    $(playlist_id).empty();
    $(playlist_id).append('<span><b>'+playlist+'</b></span>');
}

function removePlaylist(id, playlist) {
    var lcd_id = "#"+id+"_lcd";
    var alias_id = "#"+id+"_alias";
    var playlist_id = "#"+id+"_playlist";

    //Removing playlist from DB
    $.post( "action.php", {"remove_playlist": '1', "playlist_name": playlist});

    //Updating table on page.
    $(lcd_id).empty();
    $(lcd_id).append('<a href="javascript:addPlaylist('+id+', \''+playlist+'\');">no</a>')
    $(alias_id).empty();
    $(playlist_id).empty();
    $(playlist_id).append('<span>'+playlist+'</span>');
}

function addRadiostation() {
    $('body').append('<div class="box_background"></div><div class="box_frame"></div>');

}
