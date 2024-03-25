from threading import Thread, Lock, Semaphore
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

class BoundedBuffer:
    def __init__(self, size):
        self.buffer = []
        self.size = size
        self.lock = Lock()
        self.empty = Semaphore(0)
        self.full = Semaphore(size)

    def insert(self, item):
        self.full.acquire()
        self.lock.acquire()
        self.buffer.append(item)
        self.lock.release()
        self.empty.release()

    def remove(self):
        self.empty.acquire()
        self.lock.acquire()
        item = self.buffer.pop()
        self.lock.release()
        self.full.release()
        return item

def producer(buffer):
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)
        with open('all.txt', 'a') as f:
            f.write(str(num) + '\n')
        buffer.insert(num)

def customer(buffer, parity, filename):
    while True:
        num = buffer.remove()
        if num % 2 == parity:
            with open(filename, 'a') as f:
                f.write(str(num) + '\n')

if __name__ == "__main__":
    buffer = BoundedBuffer(BUFFER_SIZE)
    producer_thread = Thread(target=producer, args=(buffer,))
    customer_thread1 = Thread(target=customer, args=(buffer, 0, 'even.txt'))
    customer_thread2 = Thread(target=customer, args=(buffer, 1, 'odd.txt'))

    producer_thread.start()
    customer_thread1.start()
    customer_thread2.start()

    producer_thread.join()
    customer_thread1.join()
    customer_thread2.join()
