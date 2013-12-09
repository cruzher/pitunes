<?php
	
	include("mysql.php");

	if(isset($_GET['general'])) {
		$settings = mysql_fetch_assoc(mysql_query("SELECT * FROM settings"));

		echo '<h2>General Settings</h2>';

		echo '<h3>Airplay</h3>';
		echo '<form method="post" action="action.php">';
		if ($settings['airplay_status'] == 1) {
			echo '<input type="radio" name="enabled" value="1" checked>Enabled <input type="radio" name="enabled" value="0">Disabled<p>';
		} else {
			echo '<input type="radio" name="enabled" value="1">Enabled <input type="radio" name="enabled" value="0" checked>Disabled<p>';
		}
		echo '<b>Name</b><br>';
		echo '<input type="text" name="name" value="'.$settings['airplay_name'].'"><br>';
		echo '<input type="submit" name="airplay" value="Save">';
		echo '</form>';

		echo '<h3>DNS</h3>';
		echo '<input type="text" name="nameserver_one" value="'.$settings['nameserver_one'].'"><br>';
		echo '<input type="text" name="nameserver_two" value="'.$settings['nameserver_two'].'"><br>';
		echo '<span class="submit"><a href="javascript:saveDns();">Save</a></span>';
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

		echo '<form method="post" action="action.php">';
		if($settings['spotify_status'] == 1) {
			echo '<input type="radio" name="status" value="1" checked>Enabled <input type="radio" name="status" value="0">Disabled<br>';
		} else {
			echo '<input type="radio" name="status" value="1">Enabled <input type="radio" name="status" value="0" checked>Disabled<br>';
		}
		if($settings['spotify_status'] == 1) {
			echo '<b>Username</b><br>';
			echo '<input type="text" name="username" value="'.$settings['spotify_user'].'"><br>';
			echo '<b>Password</b><br>';
			echo '<input type="password" name="password" value="******"><br>';
		} else {
			echo '<b>Username</b><br>';
			echo '<input type="text" name="username"><br>';
			echo '<b>Password</b><br>';
			echo '<input type="password" name="password"><br>';
		}
		echo '<input type="submit" name="spotifysettings" value="Save">';
		echo '</form>';
	}
?>