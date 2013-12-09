<?php

	function shairportConfig($airplayname, $airplaystatus) {
		$shairport = "/etc/init.d/shairport";
		$general = mysql_fetch_assoc(mysql_query("SELECT * FROM settings"));
                
		//DEBUG
		/*
		echo $airplayname.'<br>';
		echo 'DB: '.$general['airplayname'].'<br>';
		echo $airplaystatus.'<br>';
		echo 'DB: '.$general['airplaystatus'].'<br>';
		*/
		
		if ($airplayname != $general['airplay_name']) {
			exec('sudo sed -i "/AIRPINAME=/ c\AIRPINAME='.$airplayname.'" '.$shairport);
			print '<br>';
		}
		if ($airplaystatus != $general['airplay_status']) {
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
		$mekk = mysql_query("UPDATE settings SET `airplay_status`='$airplaystatus', `airplay_name`='$airplayname'");
	}
?>