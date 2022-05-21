<?php

//show all php errors

use Klein\Klein;
use Klein\Request;
use Klein\Response;
use Klein\ServiceProvider;

error_reporting(E_ALL);
ini_set('display_errors', 1);

require './composer/vendor/autoload.php';
require './humblimage/images.php';

$route = new \Klein\Klein();


$route->with('/v1/', function () use ($route) {



  $route->respond('GET', '', function ($request, $response, $service, $app) use ($route) {

    $imageTest = (new images())->SearchbyId(3);

    $route->response()->json($imageTest);
  });



  /**
   * This route is responsive for image search
   * if the request is a GET request and all requested params is settled look for image on database
   * Required Params: method, value
   */
  $route->respond('GET', 'search', function (Request $request,Response $response,ServiceProvider $service, $app) use ($route) {

    //? if params not setted return 400 and an error
    if(!$request->param('type') && !$request->param('value')){ 
      $response->code(400);
      $response->json(array('error' => 'Params is wrong', 'isOk' => false));
      return;
    }

    //? set the methods for class search
    $serachMethods = [
      'id' => 'SearchbyId',
      'imageid' => 'SearchbyImageId',
      'tweetid' => 'SearchbyTweetId'
    ];

    //? Check if type param is in the methods
    if (!array_key_exists($request->param('type'), $serachMethods)) {
      $response->code(400);
      $response->json(array('error' => 'No type string', 'isOk' => false));
      return;
    }

    try {
      
      //? Get image by requested method and value
      $image = (new images())->{$serachMethods[$request->param('type')]}($request->param('value'));

      //? Return image
      $response->json([
        'image' => $image,
        'isOk' => true
      ]);

    } catch (\Exception $e) {

      //? If there is an error return 404 and an error
      $response->code(404);
      $response->json(array('error' => $e->getMessage(), 'isOk' => false));
    }
    

  });

  $route->respond('GET', '[i:id]', function ($request, $response, $service, $app) use ($route) {

    try {
      $imageTest = (new images())->SearchbyId($request->id);
      $route->response()->json($imageTest);
    } catch (\Exception $e) {
      //? If there is an error return 404 and an error
      $response->code(404);
      $response->json(array('error' => $e->getMessage(), 'isOk' => false));
    }
  });
});



$route->dispatch();
