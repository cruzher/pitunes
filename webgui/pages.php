<?php
	
	include("mysql.php");

	if(isset($_GET['general'])) {
		$settings = mysql_fetch_assoc(mysql_query("SELECT * FROM settings"));

		echo '<h2>General Settings</h2>';

		echo '<h3>Airplay</h3>';
		echo '<form method="post" id="airplay">';
		if ($settings['airplay_status'] == 1) {
			echo '<input type="radio" name="airplay_status" value="1" checked>Enabled <input type="radio" name="airplay_status" value="0">Disabled<p>';
		} else {
			echo '<input type="radio" name="airplay_status" value="1">Enabled <input type="radio" name="airplay_status" value="0" checked>Disabled<p>';
		}
		echo '<b>Name</b><br>';
		echo '<input type="text" name="airplay_name" value="'.$settings['airplay_name'].'"><br>';
		echo '<input type="submit" name="airplay" value="Save">';
		echo '</form>';

		echo '<h3>DNS</h3>';
		echo '<form id="dns">';
		echo '<input type="text" name="nameserver_one" value="'.$settings['nameserver_one'].'"><br>';
		echo '<input type="text" name="nameserver_two" value="'.$settings['nameserver_two'].'"><br>';
		echo '<input type="submit" name="dns" value="Save">';
		echo '</form>';
	}

	if(isset($_GET['network'])) {
		$settings = mysql_fetch_assoc(mysql_query("SELECT * FROM settings"));
		echo '<h2>Network Settings</h2>';
		
		if ($settings['lan_status'] == 0) { //DISABLED
			echo '<h3>LAN</h3>';
			echo '<form method="post" action="action.php">';
			echo '<input type="radio" name="status" value="0" checked>Disabled ';
			echo '<input type="radio" name="status" value="1">DHCP ';
			echo '<input type="radio" name="status" value="2">Static<br>';
			echo '</form>';
			echo '<span class="footnote">In disabled-mode the network act as a DHCP-server for easy configuration</span><p>';
			echo '<span class="label">IP-address</span><br>';
			echo '192.168.1.1<br>';
			echo '<span class="label">Netmask</span><br>';
			echo '255.255.255.0<br>';
			echo '<span class="label">Gateway</span><br>';
			echo '0.0.0.0<br>';
		}
		if ($settings['lan_status'] == 1) { //DHCP
			echo '<h3>LAN</h3>';
			echo '<form method="post" action="action.php">';
			echo '<input type="radio" name="status" value="0">Disabled ';
			echo '<input type="radio" name="status" value="1" checked>DHCP ';
			echo '<input type="radio" name="status" value="2">Static<br>';
			echo '<span class="footnote">In disabled-mode the network act as a DHCP-server for easy configuration</span><p>';
			echo '<span class="label">IP-address</span><br>';
			echo '0.0.0.0<br>';
			echo '<span class="label">Netmask</span><br>';
			echo '0.0.0.0<br>';
			echo '<span class="label">Gateway</span><br>';
			echo '0.0.0.0<br>';
			echo '</form>';
		}
		if ($settings['lan_status'] == 2) { //STATIC
			echo '<h3>LAN</h3>';
			echo '<form method="post" action="action.php">';
			echo '<input type="radio" name="status" value="0">Disabled ';
			echo '<input type="radio" name="status" value="1">DHCP ';
			echo '<input type="radio" name="status" value="2" checked>Static<br>';
			echo '<span class="footnote">In disabled-mode the network act as a DHCP-server for easy configuration</span><p>';
			echo '<span class="label">IP-address</span><br>';
			echo '<input type="text" name="lan_ip" value="'.$settings['lan_ip'].'"><br>';
			echo '<span class="label">Netmask</span><br>';
			echo '<input type="text" name="lan_netmask" value="'.$settings['lan_netmask'].'"><br>';
			echo '<span class="label">Gateway</span><br>';
			echo '<input type="text" name="lan_gateway" value="'.$settings['lan_gateway'].'"><br>';
			echo '<input type="submit" name="lan" value="Save">';
			echo '</form>';
		}

	}

	if(isset($_GET['spotify'])) {
		$settings = mysql_fetch_assoc(mysql_query("SELECT * FROM settings"));

		echo '<h2>Spotify</h2>';

		
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
			//$playlists = array("Testing", "Mekking", "Albums Queen", "Tjohej!", "Albums Infected Mushroom");

			//loop through all playlists to se if the playlists exists in the database.
			echo '<table>';
			echo '<td width="15" class="head">LCD</td>';
			echo '<td width="150" class="head">Alias</td>';
			echo '<td width="300" class="head">Playlist</td><tr>';

			foreach ($playlists as $playlist) {
				//$playlist = str_replace("/n", "", $playlist);
				$lcd = mysql_fetch_assoc(mysql_query("SELECT * FROM spotify_playlists WHERE name='$playlist'"));
				
				if ($lcd) {
					echo '<td><a href="">yes</a></td>';
					echo '<td>'.$lcd['alias'].'</td>';
					echo '<td><b>'.$playlist.'</b></td>';
				} else {
					echo '<td><a href="">no</a></td>';
					echo '<td></td>';
					echo '<td>'.$playlist.'</td>';
				}
				
				echo '<tr>';
			}
			echo '</table>';
		}
	}
?>