#? import our main class from humblimage module
from humblimage.main import humblimage
import schedule
import time

test = humblimage()


def work():
  test.postImage()

schedule.every(30).minutes.do(work)

while True:
  schedule.run_pending()
  time.sleep(1)