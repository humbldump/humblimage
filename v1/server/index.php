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

  $route->respond('GET', '[i:id]', function (Request $request,Response $response,ServiceProvider $service, $app) use ($route) {

    try {
      $imageTest = (new images())->SearchbyId($request->id);
      $route->response()->json($imageTest);
    } catch (\Exception $e) {
      //? If there is an error return 404 and an error
      $response->code(404);
      $response->json(array('error' => $e->getMessage(), 'isOk' => false));
    }
  });

  $route->respond('GET', 'savePostedImage', function (Request $request,Response $response,ServiceProvider $service, $app) use ($route) {

    //Check if imageData passed
    if(!$request->param('imageData')){
      $response->code(400);
      $response->json(array('error' => 'No image', 'isOk' => false));
      return;
    }

    $servedData = json_decode($request->param('imageData'), true);

    $imageObj = [];
    $res = [];

    //? Loop through all posted images
    foreach ($servedData['images'] as $key => $value) {
      $imageObj[$key] = new images(); //? Create new images object

      $imageObj[$key]->assignData(
        array_merge( //? Merge updated postedat and tweet id with current image data
          [
            "tweet_id" => $servedData['tweet_id'],
            "postedat" => date('Y-m-d h:i:s', $servedData['postedat']),
          ],
          $servedData['images'][$key] //? image data
        )
      );

      $res[$key] = $imageObj[$key]->saveImagetoDB(); //? Save image
    }

    //if there was an error while saving return 400 and an error
    if (in_array(false, $res)) {
      $response->code(500);
      $response->json(array('error' => 'Error while saving image', 'isOk' => false));
      return;
    }
    
    //? Return Response
    $response->json(array('isOk' => true));
  });

});



$route->dispatch();
