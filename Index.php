<?php

/*
 * CODE BELOW INPLEMENTS SEARCH BAR ON WEBSERVER
 *
 * STILL NEED TO FILL IN HOSTNAMES BELOW TO CONNECT TO DATABASE
 *
 * STILL NEED TO EDIT SEARCH BARS TO MATCH VARIABLES IN DATABASE
 *
 * MAY NEED TO MESS WITH HOW WE PRINT OUTPUT
 *
 * CURRENTLY HAVE IT SET SO WE CAN SEARCH BY ID, FIRSTNAME, OR LASTNAME
 *
 * USER LOGIN IS JUST SET TO "admin' PWORD: "password"
 *
 * BASED ON DEMO AT https://youtu.be/PBLuP2JZcEg
 *
 */


/**
 * Created by PhpStorm.
 * User: joeltopps
 * Date: 2018-12-02
 * Time: 00:08
 */

//Link to sqli database STILL NEED TO FILL IN HOST NAMES
mysqli_connect("","admin", "password") or die(mysqli_error());
mysqli_select_db("") or die("Could not find database!");

//connect
if(isset($_POST['search'])){
    $searchq = $_POST['search'];
    $searchq = preg_replace("#[^0-9a-z]#i","",$searchq);

    $query = mysqli_query("SELECT * FROM cadets WHERE id LIKE '%$searchq%' firstname LIKE '%$searchq%' OR lastname LIKE '%$searchq%'");
    $count = mysqli_num_rows($query);
    if($count == 0){
        $output = 'No results found!';

    }
    else{
        while($row = mysqli_fetch_array($query)) {
            $fname = $row['firstname'];
            $lname = $row['lastname'];
            $id = $row['id'];

            $output .= '<div>'.fname.' '.$lname.'</div>';
        }
    }
}
?>
<html>
<title? Search</title>

</head>
<body>
<form action="index.php" method="post">
    <input type="text" name="search" placeholder="Search for Cadet..." />
    <input type="submit" value="Search" />
</form>

<?php
print("$output");
?>
</body>

</html>