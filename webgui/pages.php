<?php
	//error_reporting(E_ALL);
	//ini_set('display_errors', '1');
	
	include('version.php');
	include('mysql.php');

	if (isset($_GET['general'])) {
		$settings = mysql_fetch_assoc(mysql_query("SELECT * FROM general"));

		echo '<br><b>AirPlay</b><br>';
		echo '<form method="post" action="action.php">';
		if ($settings['airplaystatus'] != 1) {
			echo '<input type="radio" name="airplaystatus" value="1">ON <input type="radio" name="airplaystatus" value="0" checked>OFF<br><br>';
		} else {
			echo '<input type="radio" name="airplaystatus" value="1" checked>ON <input type="radio" name="airplaystatus" value="0">OFF<br><br>';
		}
		echo 'Name<br>';
		echo '<input type="text" name="airplayname" value="'.$settings['airplayname'].'"><br>';

		echo '<input type="submit" name="general" value="Save">';
		echo '</form>';
	}

	if (isset($_GET['network'])) {
		if(isset($_GET['edit'])) {
			$edit = $_GET['edit'];
		} else {
			$edit = 0;
		}

		$lan = mysql_fetch_assoc(mysql_query("SELECT * FROM network"));
		//LAN
		echo '<h2>LAN</h2>';
		echo '<form method="post" action="action.php">';
		if ($lan['mode'] == "static") {
			echo '<input type="radio" name="mode" value="dhcp">DHCP <input type="radio" name="mode" value="static" checked>Static<br>';
		} else {
			echo '<input type="radio" name="mode" value="dhcp" checked>DHCP <input type="radio" name="mode" value="static">Static<br>';
		}
		echo 'IPadress<br>';
		echo '<input type="text" name="lanip" value="'.$lan['ipaddress'].'"><br>';
		echo 'Netmask<br>';
		echo '<input type="text" name="lannm" value="'.$lan['netmask'].'"><br>';
		echo 'Gateway<br>';
		echo '<input type="text" name="langw" value="'.$lan['gateway'].'"><br><p>';

		echo '<input type="submit" name="network" value="Save">';
		echo '</form>';

		//DNS
		echo '<h2>DNS Servers</h2><br>';
		echo 'Primary<br>';
		echo '<form method="post" action="action.php">';
		echo '<input type="text" name="dns1" value="'.$lan['dns1'].'"><br>';
		echo 'Secondary<br>';
		echo '<input type="text" name="dns2" value="'.$lan['dns2'].'"><br>';
		echo '<input type="submit" name="dns" value="Save">';

		echo '</form>';

		//WIFI
		$wlan = mysql_query("SELECT * FROM wirelessnetworks");
		echo '<form method="post" action="action.php">';
		echo '<h2>WiFi</h2>';
		echo '<table>';
		echo '<td width="200" class="header"><b>SSID</b></td>';
		echo '<td width="50" class="header"><b>Encryption</b></td>';
		echo '<td width="100" class="header"><b>Password</b></td>';
		echo '<td width="70" class="header"><b>Mode</b></td>';
		echo '<td width="100" class="header"><b>IPaddress</b></td>';
		echo '<td width="100" class="header"><b>Netmask</b></td>';
		echo '<td width="100" class="header"><b>Gateway</b></td>';
		echo '<td width="100" class="header"></td>';
		echo '<tr>';

		while ($array = mysql_fetch_assoc($wlan)) {
			if($array['id'] == $edit) {
				echo '<form method="post" action="action.php">';
				echo '<input type="hidden" name="ssid" value="'.$array['ssid'].'">';
				echo '<td>'.$array['ssid'].'</td>';
				if ($array['encryption'] == "wpa2") {
					echo '<td><select name="encryption"><option value="wpa2" selected>WPA2</option><option value="wep">WEP</option></select></td>';
				} else {
					echo '<td><select name="encryption"><option value="wpa2">WPA2</option><option value="wep" selected>WEP</option></select></td>';
				}
				echo '<td><input type="text" class="text" name="key" value="'.$array['key'].'"></td>';
				if ($array['mode'] == "dhcp") {
					echo '<td><select name="mode"><option value="dhcp" selected>DHCP</option><option value="static">Static</option></select></td>';
				} else {
					echo '<td><select name="mode"><option value="dhcp">DHCP</option><option value="static" selected>Static</option></select></td>';
				}
				echo '<td><input type="text" class="text" name="ipaddress" value="'.$array['ipaddress'].'"></td>';
				echo '<td><input type="text" class="text" name="netmask" value="'.$array['netmask'].'"></td>';
				echo '<td><input type="text" class="text" name="gateway" value="'.$array['gateway'].'"></td>';
				echo '<td><input type="submit" name="wifi" value="Save"></td>';
				echo '<tr></form>';
			} else {
				echo '<td>'.$array['ssid'].'</td>';
				echo '<td>'.$array['encryption'].'</td>';
				echo '<td>'.$array['key'].'</td>';
				echo '<td>'.$array['mode'].'</td>';
				echo '<td>'.$array['ipaddress'].'</td>';
				echo '<td>'.$array['netmask'].'</td>';
				echo '<td>'.$array['gateway'].'</td>';
				echo '<td><a href="?network&edit='.$array['id'].'">Edit</a> | <a href="action.php?remove='.$array['id'].'">Remove</a></td>';
				echo '<tr>';
			}
		}
		
		if (isset($_GET['scan'])) {			
			$wifiscan = array();
			exec('sudo /sbin/iwlist wlan0 scan', $wifiscan);
			$networks = array();
			foreach($wifiscan as $wifi) {
		
				$line = explode(":", $wifi);
				$a = str_replace(" ", "", $line[0]);
				$b = str_replace(" ", "", $line[1]);
				$b = str_replace("\"", "", $b);
				
				if ($a == "ESSID") { $ssid = $b; }
				if ($a == "Encryptionkey") { $encryption = $b; }				
				if ($a == "IE") { 
					if (strpos($b, 'WPA2')) {
						$network = array("ssid" => $ssid, "encryption" => $encryption, "key" => "wpa2");
						array_push($networks, $network);
					}
				}
			}
			
			echo '<td>&nbsp;</td><tr><td><b>Available Networks</b></td><tr>';
			foreach ($networks as $net) {
				echo '<form method="post" action="action.php">';
				echo '<input type="hidden" name="encryption" value="'.$net['key'].'">';
				echo '<td><input type="hidden" name="ssid" value="'.$net['ssid'].'">'.$net['ssid'].'</td>';
				if ($net['key'] == "wpa2") { echo '<td style="text-align: center">wpa2</td>';}
				echo '<td><input type="text" class="text" name="key" value=""></td>';
				echo '<td><select name="mode"><option value="dhcp" selected>DHCP</option><option value="static">Static</option></select></td>';
				echo '<td><input type="text" class="text" name="ipaddress" value="0.0.0.0"></td>';
				echo '<td><input type="text" class="text" name="netmask" value="0.0.0.0"></td>';
				echo '<td><input type="text" class="text" name="gateway" value="0.0.0.0"></td>';
				echo '<td><input type="submit" name="wifi" value="Add"></td>';
				echo '<tr></form>';
			}
			
			echo '</table>';
		} else {
			echo '<td>&nbsp;</td><tr><td><a href="?network&scan">Scan</a></td>';
			echo '</table>';
		}
	}
	
	
	//SYSTEM
	if (isset($_GET['system'])) {
		echo '<h2>Reboot system</h2>';
		echo '<form method="post" action="action.php">';
		echo '<input type="submit" name="reboot" value="Reboot">';
		echo '</form>';
		
		echo '<h2>Update system</h2>';
		echo 'Current version: <b>'.$currentversion.'</b><br>';
		echo '<form method="post" action="action.php">';
		echo '<input type="submit" name="update" value="Update">';
		echo '</form>';
		
	}
	
	
	//RADIO
	if (isset($_GET['radio'])) {
		$station = shell_exec('mpc current -f %name%');
		$song = shell_exec('mpc current -f %title%');
		
		if ($station == "") { $station = "NOT PLAYING";}
		
		echo '<h2>Radio</h2>';
		echo 'Station: '.$station.'<br>';
		echo 'Song: '.$song.'<br>';
		echo '<a href="action.php?radioprev">Prev</a> | ';
		echo '<a href="action.php?radioplay">Play</a> | ';
		echo '<a href="action.php?radiostop">Stop</a> | ';
		echo '<a href="action.php?radionext">Next</a><p>';
		
		echo '<form method="post" action="action.php">';
		echo '<table>';
		echo '<td><b>URL</b></td>';
		echo '<td width="100" class="header"></td>';
		echo '<tr>';
		$stations = mysql_query("SELECT * FROM radiostations");
		$id = 0;
		while ($array = mysql_fetch_assoc($stations)) {
			$id++;
			echo '<td>'.$array['url'].'</td>';
			echo '<td style="text-align: center">';
			echo '<a href="action.php?playstation='.$id.'">Play</a> | ';
			echo '<a href="action.php?removestation='.$array['id'].'">Remove</a>';
			echo '</td><tr>';
		}
		echo '<form method="post" action="action.php">';
		echo '<td><input type="text" name="url" style="width: 200px"></td>';
		echo '<td><input type="submit" name="radiostation" value="Add"></td>';
		echo '</table>';
		
	}

?>
