	<?php
	error_reporting(E_ALL);
	ini_set('display_errors', '1');
	
	mysql_connect("localhost", "root", "pitunes");

	mysql_query("CREATE USER 'pitunes'@'localhost' IDENTIFIED BY  'pitunes';");
	mysql_query("GRANT USAGE ON * . * TO  'pitunes'@'localhost' IDENTIFIED BY  'pitunes' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0 ;");
	mysql_query("CREATE DATABASE IF NOT EXISTS  `pitunes` ;");
	mysql_query("GRANT ALL PRIVILEGES ON  `pitunes` . * TO  'pitunes'@'localhost';");
	mysql_close();

	mysql_connect("localhost", "pitunes", "pitunes");

	mysql_select_db("pitunes");

	//radiostations
	$radiostations = "CREATE TABLE radiostations (";
	$radiostations .= "id int AUTO_INCREMENT, ";
	$radiostations .= "name varchar(20), ";
	$radiostations .= "url varchar(200), ";
	$radiostations .= "PRIMARY KEY (id))";

	//settings
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
	$settings .= "spotify_status tinyint(4), ";
	$settings .= "spotify_user varchar(100), ";
	$settings .= "spotify_pass varchar(100), ";
	$settings .= "PRIMARY KEY (id))";

	//spotiy_playlists
	$spotify = "CREATE TABLE spotify_playlists (";
	$spotify .= "id int AUTO_INCREMENT, ";
	$spotify .= "name varchar(200), ";
	$spotify .= "alias varchar(20), ";
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
	$wifi_networks .= "gateway varchar(100), ";
	$wifi_networks .= "PRIMARY KEY (id))";
	
	mysql_query($radiostations);
	mysql_query($settings);
	mysql_query($spotify);
	mysql_query($wifi_networks);
	
	$mekk = mysql_num_rows(mysql_query("SELECT * FROM settings"));

	if (!$mekk) {
		$insert = "INSERT INTO settings(`airplay_status`, `airplay_name`, `nameserver_one`, `nameserver_two`, `lan_status`, `lan_ip`, `lan_gateway`, `lan_netmask`)";
		$insert .= "VALUES('0', 'piTunes', '8.8.8.8', '8.8.4.4', '1', '0.0.0.0', '0.0.0.0', '0.0.0.0')";

		mysql_query($insert);
	}
?>
