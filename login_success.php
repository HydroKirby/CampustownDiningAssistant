<!DOCTYPE html>
<?php
// Code by http://www.phpeasystep.com/phptu/6.html

// Check if session is not registered, redirect back to main page.
// Put this code in first line of web page.
session_start();
if(!session_is_registered(myusername)){
    header("location:main_login.php");
}
?>
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

<p>Login successful</p>
</body>
</html>
