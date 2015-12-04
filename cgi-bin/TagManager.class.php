<?

class TagManager
{
  private $connection;
  private $h;
  private $u;
  private $p;
  private $db;
  
  public function TagManager()
  {
    $this->h = "engr-cpanel-mysql.engr.illinois.edu";
    $this->u = "campusdi_rests";
    $this->p = "rests";
    $this->db = "campusdi_rests";
  }
  
  private function connect()
  {
    $this->connection = new mysqli($this->h, $this->u, $this->p, $this->db);
    if (mysqli_connect_error()) {
        'Could not connect to MySQL: ' . mysqli_connect_error();
    }
  }
  
  private function complete()
  {
    @mysqli_close($this->connection);
  }
  
  public function GetTagCloud()
  {
    $this->connect();
    $query = "SELECT tag_name AS name, COUNT(rest_id) AS count FROM tags GROUP BY tag_name";
    $result = mysqli_query($this->connection, $query) or die(mysqli_error($this->connection));
    $tags = array();
    while($row = mysqli_fetch_object($result))
    {
      array_push($tags, $row);
    }
    $this->complete();
    return $tags;
  }
  
}

?>

