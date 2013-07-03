<?php
	error_reporting(E_ALL);
	ini_set('display_errors', '1');	
	
	include('mysql.php');

	if (isset($_GET['remove'])) {
		$id = $_GET['remove'];
		mysql_query("DELETE FROM wirelessnetworks WHERE id='$id'");
		header("location: index.php?network");
	}
	
	//////////////////
	//RADIO FUNTIONS//
	//////////////////
	if (isset($_GET['removestation'])) {
		$id = $_GET['removestation'];
		mysql_query("DELETE FROM radiostations WHERE id='$id'");
		exec('mpc del '.$id);
		header("location: index.php?radio");
	}
	if (isset($_GET['playstation'])) {
		$id = $_GET['playstation'];
		exec('mpc play '.$id);
		header("location: index.php?radio");
	}
	if (isset($_GET['radioprev'])) {
		exec('mpc prev');
		header("location: index.php?radio");
	}
	if (isset($_GET['radioplay'])) {
		exec('mpc play');
		header("location: index.php?radio");
	}
	if (isset($_GET['radiostop'])) {
		exec('mpc stop');
		header("location: index.php?radio");
	}
	if (isset($_GET['radionext'])) {
		exec('mpc next');
		header("location: index.php?radio");
	}
	
	////////////////////////////
	//ADD OR SAVE WIFI NETWORK//
	////////////////////////////
	if (isset($_POST['wifi'])) {
		$ssid		= $_POST['ssid'];
		$encryption	= $_POST['encryption'];
		$key		= $_POST['key'];
		$mode		= $_POST['mode'];
		$ipaddress	= $_POST['ipaddress'];
		$netmask	= $_POST['netmask'];
		$gateway	= $_POST['gateway'];

		//Update Database
		$exists = mysql_num_rows(mysql_query("SELECT * FROM wirelessnetworks WHERE ssid='$ssid'"));
		if ($exists) {
			$mekk = mysql_query("UPDATE wirelessnetworks SET `encryption`='$encryption', `key`='$key', `mode`='$mode', `ipaddress`='$ipaddress', `netmask`='$netmask', `gateway`='$gateway' WHERE ssid='$ssid'");
		} else {
			$mekk = mysql_query("INSERT INTO wirelessnetworks(`ssid`, `encryption`, `key`, `mode`, `ipaddress`, `netmask`, `gateway`) VALUES('$ssid', '$encryption', '$key', '$mode', '$ipaddress', '$netmask', '$gateway')");
		}

		//Write Config files
		rewriteNetConfig();

		header("location: index.php?network");
	}
	
	/////////////////////////
	//SAVE NETWORK SETTINGS//
	/////////////////////////
	if (isset($_POST['network'])) {
		$lan_mode 	= $_POST['mode'];
		$lan_ip 	= $_POST['lanip'];
		$lan_netmask 	= $_POST['lannm'];
		$lan_gateway 	= $_POST['langw'];

		$mekk = mysql_query("UPDATE network SET mode='$lan_mode', ipaddress='$lan_ip', gateway='$lan_gateway', netmask='$lan_netmask'");

		rewriteNetConfig();

		header("location: index.php?network");
	}
	
	/////////////////////
	//SAVE DNS SETTINGS//
	/////////////////////
	if (isset($_POST['dns'])) {
		$dns1 	= $_POST['dns1'];
		$dns2 	= $_POST['dns2'];

		$mekk = mysql_query("UPDATE network SET dns1='$dns1', dns2='$dns2'");

		rewriteNetConfig();

		header("location: index.php?network");
	}
	
	/////////////////////////
	//SAVE GENERAL SETTINGS//
	/////////////////////////
	if (isset($_POST['general'])) {
		$airplayname = $_POST['airplayname'];
		$airplaystatus = $_POST['airplaystatus'];
		$dns1 = $_POST['dns1'];
		$dns2 = $_POST['dns2'];
		
		shairportConfig($airplayname, $airplaystatus);
		
		//WRITE CONFIG
		rewriteGeneralConfig();
		
		header("location: index.php?general");
	}
	///////////////////
	//ADD RADIOSTATON//
	///////////////////
	if (isset($_POST['radiostation'])) {
		$url = $_POST['url'];
		
		//UPDATE DB
		$exists = mysql_num_rows(mysql_query("SELECT * FROM radiostations WHERE url='$url'"));
		if (!$exists) {
			$mekk = mysql_query("INSERT INTO radiostations(`url`) VALUES('$url')");
		}
		exec('mpc add '.$url);
		
		header("location: index.php?radio");
	}
	/////////////////
	//REBOOT SYSTEM//
	/////////////////
	if (isset($_POST['reboot'])) {
		exec('sudo reboot');
	}
	if (isset($_POST['update'])) {
		exec("/home/pi/piduino/update.sh");
		header("location: index.php?system");
	}

	///////////////////
	//CONFIG FUNTIONS//
	///////////////////
	function rewriteNetConfig($airplaynamechanged=false, $airplaystatuschanged=false) {
		//Config files
		$interfaces		= "/etc/network/interfaces";
		$wpa_supplicant 	= "/etc/wpa_supplicant/wpa_supplicant.conf";
		$resolv			= "/etc/resolv.conf";


		
		//LAN SETTINGS
		$network = mysql_fetch_assoc(mysql_query("SELECT * FROM network"));
                shell_exec('sudo echo "auto lo" > '.$interfaces);
                shell_exec('sudo echo "iface lo inet loopback" >> '.$interfaces);
                shell_exec('sudo echo "" >> '.$interfaces);
                if ($network['mode'] == "static") {
                        shell_exec('sudo echo "iface eth0 inet static" >> '.$interfaces);
                        shell_exec('sudo echo "    address '.$network['ipaddress'].'" >> '.$interfaces);
                        shell_exec('sudo echo "    netmask '.$network['netmask'].'" >> '.$interfaces);
                        shell_exec('sudo echo "    gateway '.$network['gateway'].'" >> '.$interfaces);
                } else {
                        shell_exec('sudo echo "auto eth0" >> '.$interfaces);
                        shell_exec('sudo echo "iface eth0 inet dhcp" >> '.$interfaces);
                }
                shell_exec('sudo echo "" >> '.$interfaces);
                shell_exec('sudo echo "allow-hotplug wlan0" >> '.$interfaces);
                shell_exec('sudo echo "iface wlan0 inet manual" >> '.$interfaces);
                shell_exec('sudo echo "wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf" >> '.$interfaces);
                shell_exec('sudo echo "" >> '.$interfaces);
                shell_exec('sudo echo "iface default inet dhcp" >> '.$interfaces);
                
                //DNS SETTINGS
                shell_exec('sudo echo "#piduino edited" > '.$resolv);
                shell_exec('sudo echo "domain lan" >> '.$resolv);
                shell_exec('sudo echo "search lan" >> '.$resolv);
                shell_exec('sudo echo "nameserver '.$network['dns1'].'" >> '.$resolv);
                shell_exec('sudo echo "nameserver '.$network['dns2'].'" >> '.$resolv);

                
                //WIFI SETTINGS
		$wifinetworks = mysql_query("SELECT * FROM wirelessnetworks");
		shell_exec('sudo echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" > '.$wpa_supplicant);
                shell_exec('sudo echo "update_config=1" >> '.$wpa_supplicant);
                while($array = mysql_fetch_assoc($wifinetworks)) {
			if ($array['mode'] == "static") {
				shell_exec('sudo echo "" >> '.$interfaces);
                                shell_exec('sudo echo "iface '.str_replace(" ", "", $array['ssid']).' inet static" >> '.$interfaces);
                                shell_exec('sudo echo "    address '.$array['ipaddress'].'" >> '.$interfaces);
                                shell_exec('sudo echo "    netmask '.$array['netmask'].'" >> '.$interfaces);
                                shell_exec('sudo echo "    gateway '.$array['gateway'].'" >> '.$interfaces);
                        }

                        if ($array['encryption'] == "wpa2") {
                                shell_exec('sudo echo "network={" >> '.$wpa_supplicant);
                                shell_exec('sudo echo "    ssid=\"'.$array['ssid'].'\"" >> '.$wpa_supplicant);
                                shell_exec('sudo echo "    psk=\"'.$array['key'].'\"" >> '.$wpa_supplicant);
                                shell_exec('sudo echo "    proto=RSN" >> '.$wpa_supplicant);
                                shell_exec('sudo echo "    key_mgmt=WPA-PSK" >> '.$wpa_supplicant);
                                shell_exec('sudo echo "    pairwise=CCMP" >> '.$wpa_supplicant);
                                shell_exec('sudo echo "    auth_alg=OPEN" >> '.$wpa_supplicant);
                                shell_exec('sudo echo "    id_str=\"'.str_replace(" ", "", $array['ssid']).'\"" >> '.$wpa_supplicant);
                                shell_exec('sudo echo "}" >> '.$wpa_supplicant);
                        }
                }
	}
	
	function shairportConfig($airplayname, $airplaystatus) {
		$shairport = "/etc/init.d/shairport";
		$general = mysql_fetch_assoc(mysql_query("SELECT * FROM general"));
                
		//DEBUG
		/*
		echo $airplayname.'<br>';
		echo 'DB: '.$general['airplayname'].'<br>';
		echo $airplaystatus.'<br>';
		echo 'DB: '.$general['airplaystatus'].'<br>';
		*/
		
		if ($airplayname != $general['airplayname']) {
			exec('sudo sed -i "/AIRPINAME=/ c\AIRPINAME='.$airplayname.'" '.$shairport);
			print '<br>';
		}
                if ($airplaystatus != $general['airplaystatus']) {
			if ($airplaystatus == 1) {
				exec('sudo update-rd.d shairport defaults');
				print '<br>';
				exec('sudo service shairport start');
				print '<br>';
			} else {
				exec('sudo service shairport stop');
				print '<br>';
				exec('sudo update-rd.d shairport remove');
				print '<br>';
			}
                } elseif ($airplaystatus == 1) {
                	exec('sudo service shairport restart');
                	print '<br>';
                }
                
                //UPDATE DB
		$mekk = mysql_query("UPDATE general SET `airplaystatus`='$airplaystatus', `airplayname`='$airplayname'");
	}
	
	function rewriteGeneralConfig() {
	}
?>
