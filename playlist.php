<?php
	mysql_connect("localhost", "pitunes", "pitunes");
	mysql_select_db("pitunes");
	
	if (isset(getopt('spotify:'))) {
		$spotify = mysql_fetch_assoc(mysql_query("SELECT available_playlists FROM general"));
		$playlists = explode(",", $spotify['available_playlists']);
		foreach ($playlists as $playlist) {
			echo $playlist.'
';
		}
	}
	
	if (isset($_GET['radio'])) {
		$mysql = mysql_query("SELECT * FROM radiostations");
		while($radio = mysql_fetch_assoc($mysql)){
			echo $radio['url'].'
';
		}
	}
?>
