<?php
	error_reporting(E_ALL);
	ini_set('display_errors', '1');

	exec('sudo /sbin/iwlist wlan0 scan', $wifiscan);
	print_r($wifiscan);
?>
