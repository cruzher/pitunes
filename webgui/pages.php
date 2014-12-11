<?php
	
	include("mysql.php");

	$settings = mysql_fetch_assoc(mysql_query("SELECT * FROM settings"));
	include("widget_spotify.php");
	include("widget_radio.php");
	include("widget_lan.php");
	include("widget_wifi.php");
	include("widget_dns.php");
	include("widget_airplay.php");
	include("widget_update.php");
	include("widget_reboot.php");



	if(isset($_GET['spotify'])) {
		$settings = mysql_fetch_assoc(mysql_query("SELECT * FROM settings"));

		echo '<div class="title">';
		echo '<img src="images/spotifyicon.jpeg" class="title_pic">';
		echo '</div>';

		
		if($settings['spotify_status'] == 0) {
			echo '<form method="post" action="action.php"><input type="hidden" name="spotify_signin" value="1">';
			echo '<b>Username</b><br>';
			echo '<input type="text" name="spotify_user"><br>';
			echo '<b>Password</b><br>';
			echo '<input type="password" name="spotify_pass"><br>';
			echo '<input type="submit" name="spotifysettings" value="Sign in">';
			echo '</form>';
		} else {
			echo '<form method="post" action="action.php">'.$settings['spotify_user'].'<input type="hidden" name="spotify_signout" value="1"><input type="submit" value="Sign out"></form>';

			//Get playlists from spotify
			exec("mpc lsplaylists", $playlists);
			//$playlists = array("Starred", "Albums Queen", "Albums Infected Mushroom", "Albums Sia");

			//loop through all playlists to se if the playlists exists in the database.
			echo '<table>';
			echo '<td width="15" class="head">LCD</td>';
			echo '<td width="150" class="head">Alias</td>';
			echo '<td width="300" class="head">Playlist</td><tr>';

			$i  = 0;
			foreach ($playlists as $playlist) {
				$lcd = mysql_fetch_assoc(mysql_query("SELECT * FROM spotify_playlists WHERE name='$playlist'"));
				
				if ($lcd) {
					echo '<td id="'.$i.'_lcd"><a href="javascript:removePlaylist('.$i.', \''.$playlist.'\');">yes</a></td>';
					echo '<td id="'.$i.'_alias">'.$lcd['alias'].'</td>';
					echo '<td id="'.$i.'_playlist"><b>'.$playlist.'</b></td>';
				} else {
					echo '<td id="'.$i.'_lcd"><a href="javascript:addPlaylist('.$i.', \''.$playlist.'\');">no</a></td>';
					echo '<td id="'.$i.'_alias"></td>';
					echo '<td id="'.$i.'_playlist">'.$playlist.'</td>';
				}
				
				echo '<tr>';
				$i++;
			}
			echo '</table>';
		}
	}

	if(isset($_GET['radiostations'])) {
		echo '<div class="title">';
		echo '<img src="images/radioicon.png" class="title_pic">';
		echo '</div>';
	}
?>