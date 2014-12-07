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
					if(isset($_GET['settings'])) { echo '<a href="?settings"><div class="menu_item" style="border-color: orange;">Settings</div></a>'; } else { echo '<a href="?settings"><div class="menu_item">Settings</div></a>'; }
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