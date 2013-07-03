<?php
	error_reporting(E_ALL);
	ini_set('display_errors', '1');

	exec('sudo update-rd.d shairport defaults');
	exec('sudo service shairport start');
?>
