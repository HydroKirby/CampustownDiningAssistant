<!DOCTYPE html>
<html>
<head>

    <link rel="icon" href="favicon.png" type="image/x-icon"/>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
	<link href="/style/style.css" rel="stylesheet" type="text/css" />
	<title>Register: Campustown</title>

</head>
<body>
<h1 id="header">UIUC Campustown Dining Assistant - Register</h1>

<!--  https://www.youtube.com/watch?v=y4-5XgHH1PI -->

<?php
require('cgi-bin/navbar.php');
?>

	<form action="register.php" method="POST">
	Username: <input type="text" name="username">
	<br>Password: <input type="password" name="password">	
	<br>Confirm Password: <input type="password" name="repassword">		
	<br>Email: <input type="text" name="email">		
	<br><input type="submit" name="submit" value="Register"> or <a href="/login.php">Login</a>
	</form>

<?php
require('connect.php');
$username = $_POST['username'];
$password = $_POST['password'];
$repass = $_POST['repassword'];
$email = $_POST['email'];

if(isset($_POST['submit'])){
	// Sanitize the inputs.
	if (!empty($username))
		$username = escapeshellcmd(htmlspecialchars($username));
	if (!empty($password))
		$password = escapeshellcmd(htmlspecialchars($password));
	if (!empty($repass))
		$repass = escapeshellcmd(htmlspecialchars($repass));
	if (!empty($email))
		$email = escapeshellcmd(htmlspecialchars($email));

	if (!empty($username) && !empty($password) && !empty($repass) && !empty($email)) {
		if ($password != $repass) {
			echo "The passwords do not match.";
		}elseif($query = mysqli_query($connect,
			"INSERT INTO users (name, pass, email) VALUES('".$username."', '".$password."', '".$email."')"))
		{
			echo "Success";
		
		}else{
			echo "Error: This username is already registered.";
		}
	}else{
		echo "Please fill in all the fields.";
	}
}
?>
</body>
</html>
