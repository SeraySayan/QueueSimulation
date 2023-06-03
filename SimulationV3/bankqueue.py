class Queue:
    def __init__(self):
        self.customers = []

    # It checks if the queue is empty

    def isEmpty(self):
        return self.customers == []

# It adds a new customer to the queue with priority (if customer priority is 1, it will be the first in the queue)
    def enqueue(self, customer):
        # adding customer with priority
        if self.isEmpty():
            self.customers.append(customer)
        else:
            for i in range(len(self.customers)):
                if customer.priority < self.customers[i].priority:
                    self.customers.insert(i, customer)
                    print("Enqueue priority ")
                    priorities = []
                    for i in range(len(self.customers)):
                        priorities.append(self.customers[i].priority)
                    print(priorities)

                    for i in range(len(self.customers)):
                        self.customers[i].print_customer_details()
                    return
            self.customers.append(customer)
            print("Enqueue normal")
# It removes the first customer in the queue

    def dequeue(self):
        if not self.customers:
            return None

        customer = self.customers.pop(0)  # FIFO
        print("Dequeue method called. CUSTOMER SHOULD BE SERVED. (DEQUEUE)")
        return customer
# It returns the size of the queue

    def size(self):
        return len(self.customers)
# It prints the queue details

    def print_queue_details(self):
        print(f"Queue details:")
        print(f"Queue: {self.customers}")
        print(f"Queue size: {self.size()}")
