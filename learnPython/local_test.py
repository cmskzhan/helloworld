import time

def decor(f):
  starttime = time.time()
  f()
  endtime = time.time()
  print("child function run time is ", (endtime-starttime)*1000, "ms")
  return f

@decor
def funct():
  print("hello")
  time.sleep(2)
  print("world")


# if __name__ == '__main__':
#     funct()
