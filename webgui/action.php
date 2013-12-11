<?php
	//ini_set('display_errors', '1');

	include("mysql.php");


	if(isset($_POST['airplay_status'])) {
		$airplay_status = $_POST['airplay_status'];
		$airplay_name = $_POST['airplay_name'];

		//Write Shairport config
		
		//Turn service ON or OFF
		
		//Activate or Deactivate service on boot

		//Update Database
		mysql_query("UPDATE settings SET `airplay_status`='$airplay_status', `airplay_name`='$airplay_name'");

		//Return response
		echo '{"OK":"Airplay settings saved!"}';
	}

	if(isset($_POST['nameserver_one'])) {
		$nameserver_one = $_POST['nameserver_one'];
		$nameserver_two = $_POST['nameserver_two'];

		//Write DNS config

		//Update Database
		mysql_query("UPDATE settings SET `nameserver_one`='$nameserver_one', `nameserver_two`='$nameserver_two'");

		//Return response
		echo '{"OK":"DNS settings saved!"}';
	}

	if(isset($_POST['spotify_signout'])) {

		//Write spotify settings to mopidy config

		//Update Database
		mysql_query("UPDATE settings SET `spotify_status`='0', `spotify_user`='', `spotify_pass`=''");

		//empty spotify_playlists database

		header("location: index.php?spotify");
	}

	if(isset($_POST['spotify_signin'])) {
		$spotify_user = $_POST['spotify_user'];
		$spotify_pass = $_POST['spotify_pass'];

		//Write spotify settings to mopidy config

		//Update Database
		mysql_query("UPDATE settings SET `spotify_status`='1', `spotify_user`='$spotify_user', `spotify_pass`='$spotify_pass'");

		header("location: index.php?spotify");
	}

	if(isset($_POST['add_playlist'])) {
		$playlist_alias = $_POST['playlist_alias'];
		$playlist_name = $_POST['playlist_name'];

		//Insert into Database
		mysql_query("INSERT INTO spotify_playlists (`alias`, `name`)VALUES('$playlist_alias', '$playlist_name')");
	}

	if(isset($_POST['remove_playlist'])){
		$playlist_name = $_POST['playlist_name'];

		//Remove from database
		mysql_query("DELETE FROM spotify_playlists WHERE name='$playlist_name'");
	}

	if(isset($_POST['update_system'])) {
		//exec("(cd /home/pi/pitunes && git pull)", $update);

		echo '{"OK":"Update Complete!"}';
	}


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