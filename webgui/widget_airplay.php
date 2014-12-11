<?php
	echo '<div class="settings_small">';
	echo '<img src="images/AirplayIcon.png" style="width: 80px;"><br>';
	echo '<b>AirPlay</b><p>';
	echo '<form method="post" id="airplay">';
	echo '<input type="text" name="airplay_name" value="'.$settings['airplay_name'].'"><br>';
	if ($settings['airplay_status'] == 1) {
		echo '<input type="radio" name="airplay_status" value="1" checked>Enabled <input type="radio" name="airplay_status" value="0">Disabled<p>';
	} else {
		echo '<input type="radio" name="airplay_status" value="1">Enabled <input type="radio" name="airplay_status" value="0" checked>Disabled<p>';
	}
	echo '<input type="submit" value="Save">';
	echo '</form></div>';
?>