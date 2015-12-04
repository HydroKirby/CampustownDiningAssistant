<!DOCTYPE html>
<html>
<head>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
	<link href="/style/style.css" rel="stylesheet" type="text/css" />
	<title>UIUC Campustown Dining Assistant - Python Test</title>
</head>
<body>
<h1>UIUC Campustown Dining Assistant - Python Test</h1>

<ul id="navbar">
<li><a href="http://campusdining.web.engr.illinois.edu/">Homepage</a></li>
<li><a href="http://campusdining.web.engr.illinois.edu/about/">About</a></li>
</ul>

<p>This page inputs a user into the MySQL database.</p>

<?php
error_reporting(E_ALL);
ini_set('display_errors', '1');

$servername = "engr-cpanel-mysql.engr.illinois.edu";
$username = "campusdi_rests";
$password = "rests";
$dbname = "campusdi_rests";

echo "<br>Connecting.";
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if (mysqli_connect_error()) {
    die("Failed to connect. " . mysqli_connect_error());
} else {
    echo "Connected Successfully";
}

echo "<br>Attempting to read users.";
$sql="SELECT * FROM users";
$result = mysqli_query($conn, $sql);
echo "<br>Printing entries.";
foreach ($result as $row) {
    echo "<br>" . $row['name'] . " has email address " . $row['email'];
}

echo "<br>Attempting to insert a user.";
$sql="INSERT INTO users (name, email, pass) VALUES ('n', 'e', 'p')";
$result = mysqli_query($conn, $sql);
if ($result) {
    echo "<br>Inserted a user.";
} else {
    echo "<br>Failed to insert.";
}
?>

</body>
</html>

