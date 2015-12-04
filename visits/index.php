<?php
	session_start();
	require('../connect.php');
?>

<!DOCTYPE html>
<html>
<head>

    <link rel="icon" href="/favicon.png" type="image/x-icon"/>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
	<link href="/style/style.css" rel="stylesheet" type="text/css" />
	<title>Visits: UIUC Campustown Dining Assistant</title>
</head>
<body>
<h1 id="header">UIUC Campustown Dining Assistant - Visits</h1>
<?php
// Display the navigation bar.
require('../cgi-bin/navbar.php');

// Display the user's history.
$username = $_SESSION['username'];
if (!empty($username)) {
    echo "<p>This is your history of visits, ". $username. ".</p>";
    $python = `python ../cgi-bin/runner.py query -n $username -v`;
    echo $python;
} else {
    echo "<p>View your history of visited restaurants here.</p>";
    echo "<p>You are not logged in, so you can not view your history.</p>";
}
?>
</body>
</html>
