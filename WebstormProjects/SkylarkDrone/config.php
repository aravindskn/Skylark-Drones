define('DB_HOSTNAME','localhost');
define('DB_USER','root');
define('DB_PASS','');
define('DB_NAME','skylark');
$link=mysqli_connect(DB_HOSTNAME,DB_USER,DB_PASS,DB_NAME) or die("Error connecting to the database");