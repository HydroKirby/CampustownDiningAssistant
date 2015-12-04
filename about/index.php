<!DOCTYPE html>
<html>
<head>
    <link rel="icon" href="../favicon.png" type="image/x-icon"/>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
	<link href="/style/style.css" rel="stylesheet" type="text/css" />
	<title>About: UIUC Campustown Dining Assistant</title>
</head>
<body>
<h1 id="header">UIUC Campustown Dining Assistant - About</h1>

<?php
require('../cgi-bin/navbar.php');
?>

<h2>Description</h2>
<p>The purpose of Campustown Dining Assistant is to help UIUC students learn more about dining and restaurant choices around the campustown area.</p>
<h2>Usefulness</h2>
<p>Yelp itself exists, but our search engine focuses primarily on options within
the Champaign-Urbana area. As such, its interface is more streamlined compared to related services. Users can start narrowing down their choices by type of restaurant directly from the home page.</p>
<h2>Realness</h2>
<p>Our data comes from Yelp by way of the Yelp API.</p>
<h2>Basic Functions</h2>
<p>The database has real information in it because it comes from Yelp.</p>
<p>Data is inserted and updated automatically the moment you make a search query. When making a query, the Yelp database is first queried. Any new restaurants are added to our database. Any restaurants that already exist in our system are udated. A hidden web page allows us to delete restaurants.</p>
<p>You can search our database from the front page. This involves a join of multiple tables because the output prints the tags related to restaurants and other information related to them.</p>
<h2>Advanced Functions</h2>
<p>The first advanced search feature is weighted searching. Campus Dining Assistant retains a history of restaurants that the user has visited. As long as they are logged in, search results on tags will be weighted and sorted to resemble restaurants that the user had visited in the past. For example, searching for "dinner" looks for all restaurants in the database and subsequently weights those results more strongly if the user had visited restaurants with similar tags to it in the past.</p>
<p>The second advanced feature is autocompletion in the search box. As you begin to type in the search box, suggestions will appear from the tags in the database and from a dictionary of words.</p>

<h2>Creators</h2>
<ul>
<li>Larry Resnik (lsresni2)</li>
<li>Alice (Hung-Yu) Chen (hchen136)</li>
<li>Richard Shen (rnshen2)</li>
<li>Victor Rocha (varocha2)</i>
</ul>

<h2>Original Project Links</h2>
<ul>
<li><a href="https://wiki.cites.illinois.edu/wiki/display/cs411fa15/Overview">CS 411 Database Systems Fall 2015 Homepage</a></li>
<li><a href="https://wiki.cites.illinois.edu/wiki/display/cs411fa15/Project+Track+1">Project Requirements</a></li>
<li><a href="https://wiki.cites.illinois.edu/wiki/display/cs411fa15/Team+Zer0+Project+Description">Original Project Description</a></li>
</ul>

<h2>References and Sources</h2>
<p>Data is gathered from <a href="http://www.yelp.com/">Yelp</a> using the <a href="https://www.yelp.com/developers/documentation">Yelp API.</a></p>
<p>The following references were used.</p>
<ul>
<li>Making the default value of a date field in MySQL be the current date. <a href="http://stackoverflow.com/a/1552804">Stack Overflow</a>.</li>
<li>Making the tag cloud was referenced from <a href="http://www.peachpit.com/guides/content.aspx?g=webdesign&seqNum=302">Mariz Jordan's Web Design Reference Guide</a>.</li>
<li>The base code for our login system was referenced from <a href="https://www.youtube.com/watch?v=nxV3nMLg0gg">Giannis Marinakis' PHP Forum web video series</a>.</li>
<li>The basis for our autocomplete advanced feature comes from <a href="http://markonphp.com/autocomplete-php-jquery-mysql-part1/">this tutorial</a>.</li>
<li>The food dictionary words for our autocomplet advanced feature come from <a href="http://www.enchantedlearning.com/wordlist/food.shtml">Food and Eating Vocabulary Word List</a>.</li>
</ul>

<p>This project was finalized in December 2015.</p>
</body>
</html>