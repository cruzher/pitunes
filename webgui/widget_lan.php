<?php
	$lan_link_status = trim(shell_exec('cat /sys/class/net/eth0/carrier'));
	$lan_ip = trim(shell_exec('/sbin/ifconfig eth0 |grep "inet addr" |cut -d ":" -f 2 |cut -d " " -f 1'));
	$wifi_nm = trim(shell_exec('/sbin/ifconfig eth0 |grep "Mask:" |cut -d ":" -f 4'));
	
	echo '<div class="settings_small">';
	if ($settings['lan_status'] == 1) { //DHCP
		echo '<img src="images/lanicon2.png" style="width: 80px;"><br>';
		echo '<b>LAN</b><p>';
		echo '<form method="post" action="action.php">';
		echo '<input type="radio" name="lan_status" value="1" checked>DHCP ';
		echo '<input type="radio" name="lan_status" value="2">Static<br>';
		echo '<div id="lan_box">';
		if ($lan_link_status == 0 ) {
			echo '<p>No Link';
		} else {
			echo '<span class="label">IP-address</span><br>';
			echo $lan_ip.'<br>';
			echo '<span class="label">Netmask</span><br>';
			echo '0.0.0.0<br>';
			echo '<span class="label">Gateway</span><br>';
			echo '0.0.0.0<br>';
		}
		echo '</div>';
		echo '</form>';
	}
	if ($settings['lan_status'] == 2) { //STATIC
		echo '<img src="images/lanicon2.png" style="width: 80px;">';
		echo '<form method="post" action="action.php">';
		echo '<input type="radio" name="lan_status" value="1">DHCP ';
		echo '<input type="radio" name="lan_status" value="2" checked>Static<p>';
		echo '<div id="lan_box">';
		echo '<input type="text" name="lan_ip" value="'.$settings['lan_ip'].'" placeholder="IP-address"><br>';
		echo '<input type="text" name="lan_netmask" value="'.$settings['lan_netmask'].'" placeholder="Netmask"><br>';
		echo '<input type="text" name="lan_gateway" value="'.$settings['lan_gateway'].'" placeholder="Gateway"><br>';
		echo '<input type="submit" value="Save">';
		echo '</div>';
		echo '</form>';
	}
	echo '</div>';
?>