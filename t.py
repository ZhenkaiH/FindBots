from queue import PriorityQueue

q = PriorityQueue()
q.put((7,'lori'))
q.put((-1,'Jseon'))
q.put((10,'King'))

i = 0
while i<q.qsize():
    print(q.get())