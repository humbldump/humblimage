<?php

require __DIR__ . "/../composer/vendor/autoload.php";
require __DIR__."/enums.php";


/**
 * humblimage - images
 *
 * @category  Twitter Bot
 * @package   humblimage
 * @author    humbldump <humbldump@protonmail.com>
 * @copyright Copyright (c) 2022
 * @link      https://github.com/humbldump/humblimage
 * @version   0.1.0
 */
class images
{


  /**
   * @var string unique id of the image
   */
  public int $id = 0;

  /**
   * @var int Posted Tweet id of the image
   */
  public int $tweet_id = 0;

  /**
   * @var string Image id from unsplash
   */
  public string $image_id = "";

  /**
   * @var string Image description from unsplash
   */
  public ?string $image_description = "";

  /**
   * @var string Image alternative decsription from unsplash
   */
  public ?string $image_alt_description = "";

  /**
   * @var string Owner of the image id from unsplash
   */
  public string $owner_id = "";

  /**
   * @var string Owner username of unsplash
   */
  public ?string $owner_username = "";

  /**
   * @var string Owner fullname from unsplash
   */
  public ?string $owner_name = "";

  /**
   * @var string Owner twitter profile username
   */
  public ?string $owner_twitter_username = "";

  /**
   * @var DateTime of the Twitter post
   */
  public $postedat = null;





  /**
   * @var MysqliDB database connection
   */
  private MysqliDb $db;


  public function __construct() {
    
    /* Call Static DB method to connecy Database */
    $this->db = $this::connectDB();

  }

  public function SearchbyId(?string $id): ?images{
    $result = $this->db->where('id', $id)->getOne(enum::tables['images']);
    return $this->assignData($result);
  }

  public function SearchbyImageId(?string $image_id): ?images{
    $result = $this->db->where('image_id', $image_id)->getOne(enum::tables['images']);
    return $this->assignData($result);
  }

  public function SearchbyTweetId(?string $tweet_id): ?images{
    //todo: Currently returning ony one image, but we might be posted multiple image on one tweet
    $result = $this->db->where('tweet_id', $tweet_id)->getOne(enum::tables['images']);
    return $this->assignData($result);
  }


  /**
   * It saves the image to the database
   * 
   * @return bool if thereis no error on db query returns true.
   */
  public function saveImagetoDB(): bool{
    //? Inser images data to DB
    $result = $this->db->insert(enum::tables['images'], $this->getImageArray());

    //? Set id to the new image
    if (!is_numeric($this->id)) {
      throw new Exception("While saving this image, something went wrong", 110);
    }

    $this->id = $result;
    return $this->db->getLastErrno() == 0;
  }

  /**
   * It returns an array of the image's properties.
   * 
   * @return array An array of the properties of the object.
   */
  public function getImageArray(): array{
    return [
      'id' => $this->id,
      'tweet_id' => $this->tweet_id,
      'image_id' => $this->image_id,
      'image_description' => $this->image_description,
      'image_alt_description' => $this->image_alt_description,
      'owner_id' => $this->owner_id,
      'owner_username' => $this->owner_username,
      'owner_name' => $this->owner_name,
      'owner_twitter_username' => $this->owner_twitter_username,
      'postedat' => $this->postedat
    ];
  }



  /**
   * It takes an array of data and assigns it to the object's properties.
   * 
   * @param array|null $data The array of data to be assigned to the object.
   * 
   * @return ?images The object itself.
   */
  public function assignData(array $data = null): ?images{

    if ($data == null) {
      throw new Exception("Couldn't find the selected image...", 1);
    }

    foreach ($data as $key => $value) {
      if (property_exists($this, $key)) {
        $this->$key = $value;
      }
    }

    return $this;
  }

  public static function connectDB(): ?MysqliDb{
    return new MysqliDb ('localhost', getenv('mysql-user'), getenv('mysql-password'), getenv('mysql-db'), 3306);
  }
}
