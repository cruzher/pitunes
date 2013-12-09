
$( "#airplay" ).submit(function( event ) {

	event.preventDefault();

	var $form = $( this ),
    airplay_status = $form.find( "input[name='enabled']" ).val(),
    airplay_name = $form.find( "input[name='name']" ).val(),
    url = $form.attr( "action" );

    var posting = $.post( url, {"airplay": 1, "airplay_status": airplay_status, "airplay_name": airplay_name } );

    posting.done(function( data ) {
    	//Do stuff
    	alert(data);
  	});
});