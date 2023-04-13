import random
import numpy as np
import matplotlib.pyplot as plt


class Customer:
    def __init__(self, id):
        self.id = id
        self.arrival_time = 0.0
        self.service_time = 0.0
        self.service_start_time = 0.0
        self.departure_time = 0.0  # leaving time from bank
        self.wait_time = 0.0  # time spent in queue

    def __repr__(self):
        return f"Customer {self.id}"


class Queue:
    def __init__(self):
        self.customers = []

    def enqueue(self, customer):
        self.customers.append(customer)
        # print customer details for debugging
        print_customer_details(customer)

    def dequeue(self):
        if not self.customers:
            return None

        customer = self.customers.pop(0)  # FIFO
        print("Dequeue method called. CUSTOMER SHOULD BE SERVED. (DEQUEUE)")
        print_customer_details(customer)
        return customer


def simulate_MMn(simulation_customer_number, arrival_rate, service_rate, num_servers):

    print(f"MMC queue simulation started.")
    queue = Queue()
    servers_busy = [False] * num_servers
    next_departure_time = [float('inf')] * num_servers
    tot_next = []

    # arrival rate : Poisson arrival rate (λ)
    # arrival_interval time (1/λ)
    arrival_interval = 1 / arrival_rate
    print(
        f"Arrival rate: {arrival_rate}, arrival interval: {arrival_interval:.2f}")

    service_interval = 1 / service_rate
    next_arrival_time = random.expovariate(arrival_rate)
    tot_next.append(next_arrival_time)
    time = 0  # current time
    queue_history = []  # queue length history
    total_customers = 0  # total number of customers in the system
    total_wait_time = 0  # total wait time
    total_customers_waiting = 0  # total number of customers waiting in queue
    next_service_start_time = [float('inf')] * num_servers
    total_service_time = 0.0  # total service time

    while total_customers < simulation_customer_number:

        print(f"TIME: {time:.2f}")
        print(f"\nNEXT ARRIVAL TIME: {next_arrival_time:.2f}")
        print(f"NEXT DEPARTURE TIME: {next_departure_time}")

        # handle arrival event
        if time >= next_arrival_time:

            customer = create_customer(
                total_customers, next_arrival_time, service_interval)
            total_service_time += customer.service_time

            served = False
            # check if any server is free
            for i in range(num_servers):
                if not servers_busy[i]:
                    servers_busy[i] = True
                    customer.service_start_time = customer.arrival_time
                    customer.departure_time = customer.service_start_time + customer.service_time
                    next_departure_time[i] = customer.departure_time
                    customer.wait_time = 0.0
                    next_service_start_time[i] = customer.departure_time

                    served = True
                    print(
                        "\n\nServer is not busy. CUSTOMER SHOULD BE SERVED immediately.")
                    print(
                        f"Next departure time for server {i}: {next_departure_time[i]:.2f}")

                    # print customer details for debugging
                    print_customer_details(customer)

                    break

            # if all servers are busy
            if not served:

                customer.service_start_time = min(next_service_start_time)
                customer.departure_time = customer.service_start_time + customer.service_time
                customer.wait_time = customer.service_start_time - customer.arrival_time
                next_service_start_time[next_service_start_time.index(
                    customer.service_start_time)] = customer.departure_time

                queue.enqueue(customer)

                total_customers_waiting += 1  # increment total number of customers waiting in queue
                total_wait_time += customer.wait_time   # increment total wait time
                print(
                    f"Total customers waiting: {total_customers_waiting}, total wait time: {total_wait_time:.2f}")

            total_customers += 1
            print(f"\n\nTotal customers in the system: {total_customers}")
            next_arrival_time = time + random.expovariate(arrival_rate)
            tot_next.append(next_arrival_time-time)
            print(f"NEXT ARRIVAL TIME: {next_arrival_time:.2f}")

         # handle departure event
        for i in range(num_servers):
            if time >= next_departure_time[i]:
                customer = queue.dequeue()
                if customer is not None:  # if queue is not empty

                    next_departure_time[i] = customer.departure_time
                    print(
                        f"Next departure time for server {i}: {next_departure_time[i]:.2f}")

                else:  # if queue is empty
                    servers_busy[i] = False
                    next_departure_time[i] = float('inf')
                    print(f"Server {i} is now idle.")

        # append queue length to history
        queue_history.append(len(queue.customers))
        # print queue length history
        print(f"\n\nQUEUE HISTORY: {queue_history}")
        print(f"QUEUE LENGTH: {len(queue.customers)}")  # print queue length
        print(f"QUEUE CUSTOMERS: {queue.customers}")  # print queue customers
        time += 0.1
        print("*************************************************************************")

    print("MMn queue simulation ended.")

    # mean of service time
    print(
        f"Mean of service time: {total_service_time/simulation_customer_number:.2f}\n\n")

    calculateMetrics(queue_history, queue, total_service_time,
                     arrival_rate, num_servers, service_rate, total_wait_time, total_customers_waiting, tot_next, time)

    plotGraph(queue_history)


def print_customer_details(customer):
    print(f"\n\nCustomer {customer.id} details:")
    print(f"Arrival time: {customer.arrival_time:.2f}")
    print(f"Service time: {customer.service_time:.2f}")
    print(f"Service start time: {customer.service_start_time:.2f}")
    print(f"Departure time: {customer.departure_time:.2f}")
    print(f"Wait time: {customer.wait_time:.2f}")


def create_customer(total_customers, next_departure_time, service_interval):
    customer = Customer(total_customers + 1)
    customer.service_time = random.expovariate(service_interval)
    customer.arrival_time = next_departure_time
    return customer


def calculateMetrics(queue_history, queue, total_service_time, arrival_rate, num_servers, service_rate, total_wait_time, total_customers_waiting, tot_next, time):
    # calculate performance metrics
    avg_queue_length = np.mean(len(queue.customers))
    avg_service_time = np.mean(total_service_time)
    avg_wait_time = avg_queue_length / \
        (arrival_rate * num_servers - service_rate)
    avg_system_time = avg_service_time + avg_wait_time
    utilization = arrival_rate / (service_rate * num_servers)

    # print results
    print("Simulation results:")
    print(f"Average queue length (Lq): {avg_queue_length: }")
    print(f"Average service time: {avg_service_time: }")
    print(f"Average wait time (Wq): {avg_wait_time: }")
    print(f"Average system time: {avg_system_time: }")
    print(f"Utilization: {utilization: }")

    # Calculate performance measures
    avg_inter_arrival_time = sum(
        tot_next) / len(tot_next)  # mean of next arrival time

    print(f"Average inter-arrival time: {avg_inter_arrival_time:.2f}")

    print("Yeniiii")
    # average queue length
    Lq = total_wait_time/time
    print(f"Average queue length (Lq): {Lq:.2f}")

    # calculate confidence interval
""" z = 1.96  # 95% confidence interval
    std_dev = np.std(len(queue.customers))
    n = len(queue.customers)
    margin_of_error = z * (std_dev / np.sqrt(n))
    print(f"Margin of error: {margin_of_error:.2f}")
    print(
        f"Confidence interval: {avg_queue_length - margin_of_error:.2f} - {avg_queue_length + margin_of_error:.2f}")
        """


def plotGraph(queue_history):
    # plot the queue length over time
    plt.plot(queue_history)
    plt.title("Queue length over time")
    plt.xlabel("Time (min)")
    plt.ylabel("Queue length")
    plt.show()


if __name__ == "__main__":
    simulate_MMn(10, 2, 3, 3)
