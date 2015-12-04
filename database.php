<?php

// We will use PDO to execute database stuff. 
// This will return the connection to the database and set the parameter
// to tell PDO to raise errors when something bad happens
function getDbConnection() {
  $db = new PDO(DB_DRIVER . ":dbname=" . DB_DATABASE . ";host=" . DB_SERVER . ";charset=utf8", DB_USER, DB_PASSWORD);
  $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION); 
  return $db;
}


// This is the 'search' function that will return all possible rows starting with the keyword sent by the user
function searchForKeyword($keyword) {
    $db = getDbConnection();
     //$stmt = $db->prepare("SELECT DISTINCT tag_name FROM `tags` WHERE tag_name LIKE ? ORDER BY tag_name");
     //$stmt = $db->prepare("SELECT DISTINCT word FROM `dictionary` WHERE word LIKE ? ORDER BY word");
    $stmt = $db->prepare("SELECT DISTINCT tag_name FROM `tags` WHERE tag_name LIKE ? ORDER BY tag_name");
    $stmt2 = $db->prepare("SELECT DISTINCT word FROM `dictionary` WHERE word LIKE ? ORDER BY word");
    
    $keyword = $keyword . '%';
    $stmt->bindParam(1, $keyword, PDO::PARAM_STR, 100);
    $stmt2->bindParam(1, $keyword, PDO::PARAM_STR, 100);

    $isQueryOk = $stmt->execute();
    $isQueryOk2 = $stmt2->execute();
  
    $results = array();
    
    if ($isQueryOk && $isQueryOk2) {
      $results = $stmt->fetchAll(PDO::FETCH_COLUMN) + $stmt2->fetchAll(PDO::FETCH_COLUMN);
    } else {
      trigger_error('Error executing statement.', E_USER_ERROR);
    }

    $db = null; 

    return $results;
}
?>