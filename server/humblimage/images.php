<?php

require __DIR__ . "../composer/vendor/autoload";



class images
{
  use mysqliDB;


  /**
   * @var string unique id of the image
   */
  public int $id;

  /**
   * @var int Posted Tweet id of the image
   */
  public int $tweet_id;

  /**
   * @var string Image id from unsplash
   */
  public string $image_id;

  /**
   * @var string Image description from unsplash
   */
  public string $image_description;

  /**
   * @var string Image alternative decsription from unsplash
   */
  public string $image_alt_descriotion;

  /**
   * @var string Owner of the image id from unsplash
   */
  public string $owner_id;

  /**
   * @var string Owner username of unsplash
   */
  public string $owner_username;

  /**
   * @var string Owner fullname from unsplash
   */
  public string $owner_name;

  /**
   * @var string Owner twitter profile username
   */
  public string $owner_twitter_username;

  /**
   * @var DateTime of the Twitter post
   */
  public DateTime $postedat;
}
