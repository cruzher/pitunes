<?php
	$current_ssid = trim(shell_exec('/sbin/iwconfig wlan0 |grep ESSID |cut -d "\"" -f 2'));
	$wifi_ip = trim(shell_exec('/sbin/ifconfig wlan0 |grep "inet addr" |cut -d ":" -f 2 |cut -d " " -f 1'));
	$wifi_nm = trim(shell_exec('/sbin/ifconfig wlan0 |grep "Mask:" |cut -d ":" -f 4'));
	$wifi_available = shell_exec('/sbin/iwlist wlan0 scan |grep ESSID: |cut -d ":" -f2 |cut -d "\"" -f2');
	$wifi_networks = preg_split('/\n/', trim($wifi_available));
	echo '<div class="settings_small">';
	echo '<img src="images/wifiicon.png" style="width: 80px;"><p>';
	echo '<select name="ssid">';
	if ($current_ssid == ""){
		echo '<option value="not" selected>- - Not Connected - -</option>';
	}
	foreach ($wifi_networks as $network) {
		if ($network == $current_ssid) {
			echo '<option value="'.$network.'" selected>'.$network.'</option>';
		} else {
			echo '<option value="'.$network.'">'.$network.'</option>';
		}
	}
	echo '</select>';
	echo '<div id="wifi_box">';
		echo '<span class="label">IP-address</span><br>';
		echo $wifi_ip.'<br>';
		echo '<span class="label">Netmask</span><br>';
		echo $wifi_nm.'<br>';
		echo '<span class="label">Gateway</span><br>';
		echo '0.0.0.0<br>';
		echo '</div>';
	echo '</div>';
?>