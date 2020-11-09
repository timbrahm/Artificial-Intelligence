from priorityQueue import PriorityQueue

newQ = PriorityQueue()

newQ.push("hi", 7)
newQ.push("bye", 10)
newQ.push("hello", 1)
newQ.push("hi", 20)
newQ.push("happy", 40)

if "happy" not in newQ.entry_finder:
    newQ.push("happy", 100)

# print(newQ.pq)
# print(newQ.entry_finder)
# print(newQ.counter)
print(newQ.pop())
print(newQ.pop())
print(newQ.pop())
print(newQ.pop())

print(len(newQ.pq))
print(newQ.entry_finder)
print(newQ.counter)

# for node in newQ.entry_finder:
#     print(node)
#     print(newQ.entry_finder[node])
