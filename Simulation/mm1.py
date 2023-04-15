import random


class Customer:
    def __init__(self, id):
        self.id = id
        self.arrival_time = 0.0
        self.service_time = 0.0
        self.service_start_time = 0.0
        self.departure_time = 0.0
        self.wait_time = 0.0


    def __repr__(self):
        return f"Customer {self.id}"


class Queue:
    def __init__(self):
        self.customers = []

    def enqueue(self, customer, time):
        customer.arrival_time = time
        self.customers.append(customer)
        print("Enqueue method called.")
        print(f"Customer {customer.id} arrived at time {time:.2f}.")

    def dequeue(self, time):
        if not self.customers:
            return None

        customer = self.customers.pop(0)
        print("Dequeue method called.")
        print(
            f"Customer {customer.id} waited {customer.wait_time:.2f} seconds and departed at time {time:.2f}.")
        # queue dan çkış

        return customer


def simulate_MM1(sim_time, arrival_rate, service_rate):
    print("MM1 queue simulation started.")

    queue = Queue()
    total_customers = 0
    total_wait_time = 0
    total_customers_waiting = 0
    server_busy = False
    next_departure_time = float('inf')
    arrival_interval = 1 / arrival_rate
    service_interval = 1 / service_rate
    next_arrival_time = random.expovariate(arrival_interval)
    print(f"Next arrival time: {next_arrival_time:.2f}")
    time = 0
    queue_history = []
    total_t = 0  # initialize total_t

    while time < sim_time:
        print(f"Time: {time:.2f}")
        print(f"Next arrival time: {next_arrival_time:.2f}")
        print(f"Next departure time: {next_departure_time:.2f}")

        # handle arrival event
        if time >= next_arrival_time:
            customer = Customer(total_customers + 1)
            customer.service_time = random.expovariate(service_interval) + 0.3
            print(
                f"Customer {customer.id} service time: {customer.service_time:.2f}")
            customer.arrival_time = time
            print(
                f"Customer {customer.id} arrival time: {customer.arrival_time:.2f}")

            if not server_busy:
                server_busy = True
                next_departure_time = time + customer.service_time
                customer.service_start_time = time
                customer.departure_time = next_departure_time
                customer.wait_time = 0
                print(f"Next departure time: {next_departure_time:.2f}")

            else:
                if len(queue.customers) >= 1:
                    # print last customer in queue departure time
                    print(
                        f"Last customer in queue departure time: {queue.customers[-1].departure_time:.2f}")

                    customer.service_start_time = queue.customers[-1].departure_time
                    print(
                        f"Service start time: {customer.service_start_time:.2f}")

                    customer.departure_time = customer.service_start_time + customer.service_time
                    print(f"Departure time: {customer.departure_time:.2f}")

                else:
                    customer.service_start_time = next_departure_time
                    print(
                        f"Service start time: {customer.service_start_time:.2f}")

                    customer.departure_time = next_departure_time + customer.service_time
                    print(f"Departure time: {customer.departure_time:.2f}")

                customer.wait_time = customer.service_start_time - customer.arrival_time
                print(f"Wait time: {customer.wait_time:.2f}")
                queue.enqueue(customer, time)
                total_customers_waiting += 1
                print(f"Total customers waiting: {total_customers_waiting}")

            total_customers += 1
            print(f"Total customers: {total_customers}")
            next_arrival_time = time + random.expovariate(arrival_rate)
            print(f"Next arrival time: {next_arrival_time:.2f}")

            # print customer details for debugging
            print(
                f"Customer {customer.id} arrival time: {customer.arrival_time:.2f}")
            print(
                f"Customer {customer.id} service time: {customer.service_time:.2f}")
            print(
                f"Customer {customer.id} departure time: {customer.departure_time}")
            print(
                f"Customer {customer.id} wait time: {customer.wait_time:.2f}")

        # handle departure event
        if time >= next_departure_time:
            customer = queue.dequeue(time)

            if customer:

                total_wait_time += customer.wait_time
                # update total_t
                total_t += customer.departure_time - customer.arrival_time
                print(f"Total wait time: {total_wait_time:.2f}")
                next_departure_time = customer.departure_time
                print(f"Next departure time: {next_departure_time:.2f}")
                # print customer details for debugging
                print(
                    f"Customer {customer.id} arrival time: {customer.arrival_time:.2f}")
                print(
                    f"Customer {customer.id} service time: {customer.service_time:.2f}")
                print(
                    f"Customer {customer.id} departure time: {customer.departure_time:.2f}")
                print(
                    f"Customer {customer.id} wait time: {customer.wait_time:.2f}")

            else:
                server_busy = False
                next_departure_time = float('inf')
                print("Server is now idle.")

        # update queue history
        queue_history.append(queue)
        # print(f"Queue history: {queue_history}")
        print(f"Queue length: {len(queue.customers)}")
        print(f"Queue customers: {queue.customers}")

        # update time
        time += 0.1

    # compute statistics
    util = 1 - (queue_history.count([]) / len(queue_history))
    avg_wait_time = total_wait_time / total_customers
    queue_lengths = [len(q.customers) for q in queue_history]
    avg_queue_len = sum(queue_lengths) / len(queue_lengths)
    max_queue_len = max(queue_lengths)
    # calculate average time in the system
    avg_t = total_t / time
    print("enver hocanın dedigi")
    print(avg_t)

    # print statistics
    print(f"\nSimulation finished at time {time:.2f}.")
    print(f"Total customers served: {total_customers}")
    print(f"Total waiting time: {total_wait_time:.2f}")
    print(f"Average waiting time: {avg_wait_time:.2f}")
    print(f"Server utilization: {util:.2f}")
    print(f"Average queue length: {avg_queue_len:.2f}")
    print(f"Maximum queue length: {max_queue_len}")
    print(f"Total customers that had to wait: {total_customers_waiting}")


# simulate for 10 seconds, arrival rate of 1/4, service rate of 1/3
simulate_MM1(1000, 1.5, 0.8)
