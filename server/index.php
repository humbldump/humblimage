<?php

//show all php errors
error_reporting(E_ALL);
ini_set('display_errors', 1);


require './humblimage/images.php';

$test = new images();

print_r(json_encode($test->SearchbyImageId("dVvLmfd6K_k")));