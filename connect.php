<?php
$servername = "engr-cpanel-mysql.engr.illinois.edu";
$username = "campusdi_rests";
$password = "rests";
$dbname = "campusdi_rests";

// Create connection
$connect = mysqli_connect($servername, $username, $password, $dbname);

mysqli_select_db($connect, "campusdi_rests") or die("Connection failed");

?>