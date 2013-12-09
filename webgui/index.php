<html>
	<head>
		<title>piTunes</title>
		<link rel="stylesheet" href="style.css" type="text/css" />
		<script type="text/javascript" charset="utf-8" src="jquery-1.4.4.js"></script>
		<script type="text/javascript" src="pitunes.js"></script>
		
	</head>
	<body>
		<div id="frame">
			<div id="header"><h1>piTunes</h1></div>
			
			<div id="menu">
				<?php
					if(isset($_GET['general'])) { echo '<a href="?general"><div class="menu_item" style="border-color: orange;">General</div></a>'; } else { echo '<a href="?general"><div class="menu_item">General</div></a>'; }
					if(isset($_GET['network'])) { echo '<a href="?network"><div class="menu_item" style="border-color: orange;">LAN</div></a>'; } else { echo '<a href="?network"><div class="menu_item">LAN</div></a>'; }
					if(isset($_GET['wirelessnetwork'])) { echo '<a href="?wirelessnetwork"><div class="menu_item" style="border-color: orange;">Wireless LAN</div></a>'; } else { echo '<a href="?wirelessnetwork"><div class="menu_item">Wireless LAN</div></a>'; }
					if(isset($_GET['radiostations'])) { echo '<a href="?radiostations"><div class="menu_item" style="border-color: orange;">Radiostations</div></a>'; } else { echo '<a href="?radiostations"><div class="menu_item">Radiostations</div></a>'; }
					if(isset($_GET['spotify'])) { echo '<a href="?spotify"><div class="menu_item" style="border-color: orange;">Spotify</div></a>'; } else { echo '<a href="?spotify"><div class="menu_item">Spotify</div></a>'; }
					if(isset($_GET['system'])) { echo '<a href="?system"><div class="menu_item" style="border-color: orange;">System</div></a>'; } else { echo '<a href="?system"><div class="menu_item">System</div></a>'; }
				?>
			</div>
			
			<div id="content">
				<?php include('pages.php'); ?>
			</div>
		</div>
	</body>
</html>