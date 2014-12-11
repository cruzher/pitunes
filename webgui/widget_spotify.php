<?php
	echo '<div class="settings_big">';
	echo '<img src="images/spotifyicon.jpeg" style="width: 80px;"><br>';
	echo '<b>Spotify</b><p>';

	echo '<span style="position: absolute; left: 480px; top: 34px; font-size: 12px;"><a href="">Add Playlist</a></span>';
	echo '<span style="position: absolute; left: 480px; top: 54px; font-size: 12px;"><a href="">Sign out</a></span>';

	if ($settings['spotify_status'] == 0){
		echo '<input type="text" name="username" placeholder="Username"><br>';
		echo '<input type="password" name="password" placeholder="Password"><br>';
		echo '<input type="submit" name="spotify_signin" Value="Sign in">';
	} else {
		$playlists = mysql_query("SELECT * FROM spotify_playlists");
		while ($playlist = mysql_fetch_assoc($playlists)){
			echo '<div class="playlist_item">'.$playlist['alias'].' <a href=""><img src="images/crossicon.png" class="crossicon"></a></div>';
		}
	}
	echo '</div>';
?>