
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
    var html = '<image src="images/radioicon.png" style="margin-top: 10px; width: 80px"><p>';
    html += '<input type="text" name="stationname" placeholder="Name" style="width: 300px;"><br>';
    html += '<input type="text" name="stationurl" placeholder="url" style="width: 300px;"><br>';
    html += '<input type="submit" name="addradio" value="Add Radiostation">';

    openBox({'html': html, 'width':350, 'height':180, });
}

function addPlaylist() {
    var html = '<image src="images/spotifyicon.jpeg" style="margin-top: 10px; width: 80px"><p>';
    html += '<select name="playlist">';
    html += '<option value="1">Starred</option>';
    html += '</select>';
    html += '<input type="text" name="playlistalias" placeholder="Name" style="width: 300px;"><br>';
    html += '<input type="submit" name="addplaylist" value="Add playlist">';

    openBox({'html': html, 'width':350, 'height':180, });
}

function openBox(opts) {
    var htmlinput   = opts.html || "No Input";
    var height      = opts.height || 200;
    var width       = opts.width || 200;
    var marginleft  = (width / 2) * -1;
    var margintop   = (height / 2) * -1;

    $('body').append('<a href="javascript:closeBox();" id="removebox"><div class="box_background"></div></a><div class="box_frame" style="width: '+width+'; height: '+height+'; margin-left: '+marginleft+'; margin-top: '+margintop+';">'+htmlinput+'</div>');
    $('.box_background').fadeIn(function(){
        $('.box_frame').fadeIn();
    });
   
}

function closeBox() {
    $('.box_frame').fadeOut(function(){
        $('.box_background').fadeOut(function(){
            $('#removebox').remove();
            $('.box_frame').remove();
        });  
    });
}
