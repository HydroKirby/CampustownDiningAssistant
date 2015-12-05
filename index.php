<?php
	session_start();
	require('connect.php');
?>

<!DOCTYPE html>
<html>
<head>

    <link rel="icon" href="favicon.png" type="image/x-icon"/>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
	<link href="/style/style.css" rel="stylesheet" type="text/css" />
	<title>UIUC Campustown Dining Assistant</title>
	
	  <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
  	  <script src="autocomplete.js"></script>

</head>
<body>
<h1 id="header">UIUC Campustown Dining Assistant</h1>

<?php
require('cgi-bin/navbar.php');
?>

<p>Search for restaurants by tags in Champaign, Illinois. This is convenient
for all University of Illinois at Urbana-Champaign students.</p>

<?php
	if (@$_SESSION["username"]){
		echo "<p>Welcome, ". $_SESSION['username'] . ".</p>\n";
	}else{
		echo "<p>You are not logged in.</p>\n";
	}
?>

<form method="post" action="">
Search:
<input type="text" name="search"
value="<?php echo htmlspecialchars($_POST['search']) ?>" id="keyword">
<div id="results">
</div>
<input type="submit" name="submit">
</form>

<?php
// Run a search on our DB from the contents of the search box.
$query = htmlspecialchars($_POST["search"]);
if (!empty($query)) {
    $query = escapeshellcmd(addslashes($query));
    $username = $_SESSION['username'];
    if (!empty($username)) {
        $python = `python cgi-bin/runner.py query -u $query -n $username`;
    }
    else {
        $python = `python cgi-bin/runner.py query -u $query`;
    }
    echo $python;
} else {
    // Visit the restaurant clicked on by the user after a search.
    $query = escapeshellcmd(htmlspecialchars($_POST["visit"]));
    if (!empty($query)) {
        $restid = escapeshellcmd(htmlspecialchars($_POST["restid"]));
        $username = $_SESSION['username'];
        $python = `python cgi-bin/runner.py visit -v $username $restid`;
        $python = `$python`;
        echo $python;
        //echo "<p>" . $restid . "</p>"; 
        echo "<p>Have a nice visit!</p>";
    }
}
?>
</body>
</html>
