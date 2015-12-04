<!DOCTYPE html>
<html>
<head>
    <link rel="icon" href="favicon.png" type="image/x-icon"/>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
	<link href="/style/style.css" rel="stylesheet" type="text/css" />
	<title>Tag Cloud: UIUC Campustown Dining Assistant</title>
</head>
<body>
<h1 id="header">UIUC Campustown Dining Assistant - Tag Cloud</h1>

<?php
require('cgi-bin/navbar.php');
?>

<div id="divTagC"><?php
// Create the tag cloud.
include("cgi-bin/TagManager.class.php");
$tManager = new TagManager();
$tags = $tManager->GetTagCloud();

$maxCount = NULL;
$minCount = NULL;
foreach($tags as $tag)
{
    $maxCount = ($tag->count > $maxCount) ? $tag->count : $maxCount;
    $minCount = ($tag->count < $minCount || $minCount == NULL) ? $tag->count: $minCount;
}

$maxCountThird = $maxCount / 3;
foreach($tags as $tag)
{
    if ($tag->count == $maxCount)
        $class = 'largeTag';
    else if ($tag->count >= $maxCountThird)
        $class = 'mediumTag';
    else
        $class = 'smallTag';
    echo '<span class="'. $class .
        '"><a href="tagcloud.php?tag='. $tag->name .'">'. $tag->name .
        '</a></span>
';
}
?>
</div>

<?php
// Create a search of the DB using the clicked tag.
$query = htmlspecialchars($_GET["tag"]);
if (!empty($query)) {
    $query = addslashes($query);
    $python = `python cgi-bin/runner.py query -w $query`;
    echo $python;
}
?>
</body>
</html>
