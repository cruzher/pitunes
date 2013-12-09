<?php
	error_reporting(E_ALL);
	ini_set('display_errors', '1');
	
	mysql_connect("localhost", "pitunes", "pitunes");
	mysql_select_db("pitunes");

	//radiostations
	$radiostations = "CREATE TABLE radiostations (id int AUTO_INCREMENT, name varchar(20), url varchar(200) PRIMARY KEY (id))";

	/*//settings
	$settings = "CREATE TABLE settings (";
	$settings .= "id int AUTO_INCREMENT, ";
	$settings .= "airplay_status tinyint(4), ";
	$settings .= "airplay_name varchar(100), ";
	$settings .= "lan_status tinyint(4), ";
	$settings .= "lan_ip varchar(100), ";
	$settings .= "lan_netmask varchar(100), ";
	$settings .= "lan_gateway varchar(100), ";
	$settings .= "nameserver_one varchar(100), ";
	$settings .= "nameserver_two varchar(100), ";
	$settings .= "spotify_status tintint(4), ";
	$settings .= "spotify_user varchar(100), ";
	$settings .= "spotify_pass varchar(100) ";
	$settings .= "PRIMARY KEY (id))";

	//spotiy_playlists
	$spotify = "CREATE TABLE spotify_playlists (";
	$spotify .= "id int AUTO_INCREMENT, ";
	$spotify .= "name varchar(200), ";
	$spotify .= "alias varchar(20) ";
	$spotify .= "PRIMARY KEY (id))";

	//wifi_networks
	$wifi_networks = "CREATE TABLE wifi_networks (";
	$wifi_networks .= "id int AUTO_INCREMENT, ";
	$wifi_networks .= "ssid varchar(100), ";
	$wifi_networks .= "encryption varchar(10), ";
	$wifi_networks .= "password varchar(100), ";
	$wifi_networks .= "dhcp tinyint(4), ";
	$wifi_networks .= "ipaddress varchar(100), ";
	$wifi_networks .= "netmask varchar(100), ";
	$wifi_networks .= "gateway varchar(100) ";
	$wifi_networks .= "PRIMARY KEY (id))";*/
	
	mysql_query($radiostations);
	//mysql_query($settings);
	//mysql_query($spotify);
	//mysql_query($wifi_networks);
	
	/*$mekk = mysql_num_rows(mysql_query("SELECT * FROM settings"));

	if (!$mekk) {
		$insert = "INSERT INTO settings(";
		$insert .= "`airplay_status`, ";
		$insert .= "`airplay_name`, ";
		$insert .= "`nameserver_one`, ";
		$insert .= "`nameserver_two`";
		$insert .= ")VALUES(";
		$insert .= "'0', ";
		$insert .= "'piTunes', ";
		$insert .= "'8.8.8.8', ";
		$insert .= "'8.8.4.4')";

		mysql_query($insert);
	}*/
?>
