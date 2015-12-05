<?php
ob_start();
session_start(); 
?>

<!DOCTYPE html>
<html>
<head>

	<link rel="icon" href="favicon.png" type="image/x-icon"/>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
	<link href="/style/style.css" rel="stylesheet" type="text/css" />
	<title>Login: UIUC Campustown Dining Assistant</title>

</head>
<body>
<h1 id="header">UIUC Campustown Dining Assistant - Login</h1>

<?php
require('cgi-bin/navbar.php');
?>

<form action="login.php" method="POST">
Username: <input type="text" name="username">
<br>Password: <input type="password" name="password">	
<br><input type="submit" name="submit" value="Login"> or <a href="/register.php/">Register</a>
</form>

<?php
require('connect.php');
$username = $_POST['username'];
$password = $_POST['password'];

if(isset($_POST['submit'])){
	$username = escapeshellcmd(htmlspecialchars($username));
	$password = escapeshellcmd(htmlspecialchars($password));
	if($username && $password){
		$query = mysqli_query($connect, "SELECT * FROM users WHERE name='".$username."' and pass='".$password."'");
		//echo 'free user sql = '.$check.'<br/>';
		//$rows = mysqli_num_rows($check);

	if($query)
  		$numrows = mysqli_num_rows($query);
	else
 		die("Something failed.");
	
		if(mysqli_num_rows($query) != 0){
			//echo "Username Found";
			while ($row = mysqli_fetch_assoc($query)){
				$db_username = $row['name'];
				$db_password = $row['pass'];			
			}
			
			if($username == $db_username && $password = $db_password){ 
				echo "Logged In";
				$_SESSION["username"] = $username; 
                		header("Location: http://campusdining.web.engr.illinois.edu/index.php");
		                die();
			}else{
				die("Incorrect Password.");
			}
			
		}else{
			die("Username Not Found or Incorrect Password.");
		}
	}else{
		echo "Please fill all fields.";
	}
}
?>

<!--  https://www.youtube.com/watch?v=nxV3nMLg0gg -->
<!--  https://www.youtube.com/watch?v=V3TkYlNbU-s -->

</body>
</html>
