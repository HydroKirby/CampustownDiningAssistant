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

<?php
$servername = "engr-cpanel-mysql.engr.illinois.edu";
$username = "campusdi_rests";
$password = "rests";
$dbname = "campusdi_rests";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if (mysqli_connect_error()) {
    die("Failed to connect. " . mysqli_connect_error());
} else {
    echo "Connected Successfully";
}
try{
    if (isset($_POST['login'])) {
        // The user selected to log in.
        // username and password sent from form
        $myusername=$_POST['myusername'];
        $mypassword=$_POST['mypassword'];

        // To protect MySQL injection (more detail about MySQL injection)
        $myusername = stripslashes($myusername);
        $mypassword = stripslashes($mypassword);
        $myusername = mysqli_real_escape_string($conn, $myusername);
        $mypassword = mysqli_real_escape_string($conn, $mypassword);

        $sql="SELECT COUNT(id) FROM users WHERE name='$myusername' and pass='$mypassword'";
        $result = mysqli_query($conn, $sql);
        $count = mysqli_num_rows($result);

        // If result matched $myusername and $mypassword, table row must be 1 row
        if ($count==1){
            $_SESSION["myusername"]=$myusername;
            $_SESSION["mypassword"]=$mypassword;
            header('Location: login_success.php');
            exit;
        } else {
            echo "Wrong Username or Password";
        }
    } else if (isset($_POST['register'])) {
        // The user selected to register.
        // username and password sent from form
        $regusername=$_POST['regusername'];
        $regemail=$_POST['regemail'];
        $regpassword=$_POST['regpassword'];
        $regpassword2=$_POST['regpassword2'];

        // To protect MySQL injection (more detail about MySQL injection)
        $regusername = stripslashes($regusername);
        $regemail = stripslashes($regemail);
        $regpassword = stripslashes($regpassword);
        $regpassword2 = stripslashes($regpassword2);
        $regusername = mysqli_real_escape_string($conn, $regusername);
        $regemail = mysqli_real_escape_string($conn, $regemail);
        $regpassword = mysqli_real_escape_string($conn, $regpassword);
        $regpassword2 = mysqli_real_escape_string($conn, $regpassword2);

        $sql="SELECT COUNT(id) FROM users WHERE name='$regusername' and email='$regemail'";
        $result = mysqli_query($conn, $sql);
        $count = mysqli_num_rows($result);

        // Make sure the name and email are not taken.
        if ($count==0){
            // Register $myusername, $mypassword and redirect to file "login_success.php"
            $sql="INSERT INTO users VALUES (name, email, password) WHERE name='$regusername', email='$regemail', password='$regpassword'";
            $result = mysqli_query($conn, $sql);
           header('Location: login_success.php');
        } else {
            echo "Username is already in use or password is incorrect.";
        }
    }
} catch(PDOException $e) {
    // Print PDOException message
    echo $e->getMessage();
}
?>

</body>
</html>