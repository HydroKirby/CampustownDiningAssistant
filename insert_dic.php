<?php
$data = file_get_contents('http://www.theodora.com/food/index.html');

$dom = new domDocument;

@$dom->loadHTML($data);
$dom->preserveWhiteSpace = false;
$tables = $dom->getElementsByTagName('table');

$rows = $tables->item(3)->getElementsByTagName('tr');

foreach ($rows as $row) {
        $cols = $row->getElementsByTagName('td');
        echo $cols->item(0)->nodeValue;
        
}

?>