#? import our main class from humblimage module
# from humblimage.main import humblimage
# import schedule
# import time

# test = humblimage()


# def work():
#   test.postImage()

# schedule.every(30).minutes.do(work)

# while True:
#   schedule.run_pending()
#   time.sleep(1)


import argparse
import time

from schedule import every, repeat, run_pending
from humblimage.main import humblimage, logging


def main():
  #? parse arguments
  _p = argparse.ArgumentParser(description='HumblImage')

  #? Post only one image
  _p.add_argument('--single', '-s', action='store_true', help='Post a single image')

  #? Loop given time in minutes
  _p.add_argument('--interval', '-i', type=int, default=30, help='Interval between posts in minutes')

  args = _p.parse_args()
  image = humblimage()

  if args.single == True:
    image.logger.log(45, "Begining to post single image...")
    image.postImage()
  else:
    
    image.logger.log(45, f"Begining to post images every {args.interval} minutes...")

    #? schedule the job
    @repeat(every(float(args.interval)).minutes)
    def scheduledWork():
      image.postImage()
    
    while True:
      run_pending()
      time.sleep(1)


if __name__ == "__main__":
    main()
