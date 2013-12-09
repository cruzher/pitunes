<?php
	error_reporting(E_ALL);
	ini_set('display_errors', '1');
	
	include("mysql.php");
	
	mysql_query("CREATE TABLE general (id int AUTO_INCREMENT, airplaystatus varchar(100), airplayname varchar(100), PRIMARY KEY (id))");
	mysql_query("CREATE TABLE network (id int AUTO_INCREMENT, mode varchar(10), ipaddress varchar(100), netmask varchar(100), gateway varchar(100), dns1 varchar(100), dns2 varchar(100), PRIMARY KEY (id))");
	mysql_query("CREATE TABLE radiostations (id int AUTO_INCREMENT, url text, PRIMARY KEY (id))");
	mysql_query("CREATE TABLE wirelessnetworks (`id` int AUTO_INCREMENT, `ssid` varchar(100), `encryption` varchar(10), `key` varchar(100), `mode` varchar(100), `ipaddress` varchar(100), `netmask` varchar(100), `gateway` varchar(100), PRIMARY KEY (id))");
	
	$mekk = mysql_num_rows(mysql_query("SELECT * FROM general"));
	if (!$mekk) {
		mysql_query("INSERT INTO general(`airplaystatus`, `airplayname`, `dns1`, `dns2`)VALUES('0', 'unknown', '8.8.8.8', '0.0.0.0')");
	}
	
	$mekk2 = mysql_num_rows(mysql_query("SELECT * FROM network"));
	if (!$mekk2) {
		mysql_query("INSERT INTO network(`mode`, `ipaddress`, `netmask`, `gateway`)VALUES('static', '192.168.0.10', '255.255.255.0', '192.168.0.10')");
	}	
?>
