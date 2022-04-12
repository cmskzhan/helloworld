import threading
import time
import datetime
# list1 = []

# def fun1(a):

#   time.sleep(1)# complex calculation takes 1 seconds
#   list1.append(a)

# thread1 = threading.Thread(target = fun1, args = (1, ))
# thread1.start()

# thread2 = threading.Thread(target = fun1, args = (6, ))
# thread2.start()

# # thread1.join()
# # thread2.join()

# print("List1 is: ", list1)

t1 = datetime.datetime.now()
list1 = []

def fun1(a):
  time.sleep(2)# complex calculation takes 1 seconds
  list1.append(a)

list_thread = []

for each in range(10):
    thread1 = threading.Thread(target = fun1, args = (each, ))
    list_thread.append(thread1)
    thread1.start()



print("List1 is: ", list1)
print("threads are:", list_thread)

for th in list_thread:
  th.join()

print("List1 is: ", list1)
print("threads are:", list_thread)

t2 = datetime.datetime.now()
print("Time taken", t2 - t1)
