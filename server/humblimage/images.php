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

  public function SearchbyId(int $id): ?images{
    $result = $this->db->where('id', $id)->getOne(enum::tables['images']);
    return $this->assignData($result);
  }

  public function SearchbyImageId(string $image_id): ?images{
    $result = $this->db->where('image_id', $image_id)->getOne(enum::tables['images']);
    return $this->assignData($result);
  }

  public function SearchbyTweetId(int $tweet_id): ?images{
    $result = $this->db->where('tweet_id', $tweet_id)->getOne(enum::tables['images']);
    return $this->assignData($result);
  }


  public function saveImagetoDB(): bool{
    return $this->db->getLastErrno() == 0;
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
