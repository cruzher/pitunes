<?php
	mysql_connect("localhost", "pitunes", "pitunes");
	mysql_select_db("pitunes");
	
	$spotify = mysql_fetch_assoc(mysql_query("SELECT * FROM general WHERE group='spotify' AND setting='available_playlists'"));
	$playlists = explode($spotify['value'], ",");
	foreach ($playlist in $playlists) {
		echo $playlist.'
';
	}
	
	if (isset($_GET['radio'])) {
		$mysql = mysql_query("SELECT * FROM radiostations");
		while($radio = mysql_fetch_assoc($mysql)){
			echo $radio['url'].'
';
		}
	}
?>
