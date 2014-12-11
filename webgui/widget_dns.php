<?php
	echo '<div class="settings_small">';
	echo '<h3 style="font-size: 30px;">DNS</h3>';
	echo '<form id="dns">';
	echo '<input type="text" name="nameserver_one" value="'.$settings['nameserver_one'].'"><br>';
	echo '<input type="text" name="nameserver_two" value="'.$settings['nameserver_two'].'"><p>';
	echo '<input type="submit" name="dns" value="Save">';
	echo '</form>';
	echo '</div>';
?>