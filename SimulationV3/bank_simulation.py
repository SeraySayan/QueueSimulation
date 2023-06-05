from customer import Customer
from server import Server
from bankqueue import Queue
import os
import numpy as np
from database import Database


class BankSimulation:
    servers = []  # This list holds the servers
    queue = []  # This list holds the customers that are in the queue
    list_customers = []  # This list holds the customers that are not in the service
    # This list holds the customers that are in the any service
    after_service_start_list = []
    total_served_customers = 0
    total_service_time = 0
    total_wait_time = 0
    total_waiting_customers = 0
    num_servers = 0
    arrival_rate = 0
    service_rate = 0
    simulation_customer_number = 0
    simulation_time = 0
    total_entry_time = 0
    total_exit_time = 0
    priority_list = []

    def __init__(
        self, simulation_customer_number, arrival_rate, service_rate, num_servers, priority_list
    ):
        self.num_servers = num_servers
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.simulation_customer_number = simulation_customer_number
        self.priority_list = priority_list

    def initialize_servers(self):
        for i in range(self.num_servers):
            self.servers.append(Server(i + 1))

    def initialize_queue(self):
        self.queue = Queue()

    # This method generates the customers and sorts them according to their arrival time
    def initialize_customers(self):
        for i in range(self.simulation_customer_number):
            if i == 0:
                arrival_time = np.random.exponential(
                    scale=1 / self.arrival_rate)
            else:
                arrival_time = np.random.exponential(
                    scale=1 / self.arrival_rate) + self.list_customers[i-1].arrival_time
            service_time = np.random.exponential(scale=1 / self.service_rate)
            self.list_customers.append(
                Customer(i + 1, arrival_time, service_time, self.priority_list[i]))
        self.list_customers.sort(key=lambda x: x.arrival_time)

    def initialize_simulation(self):
        self.initialize_servers()
        self.initialize_queue()
        self.initialize_customers()

    # This method checks if the all servers are busy or not
    def all_servers_busy(self):
        for i in range(len(self.servers)):
            if self.servers[i].is_available:
                return False
        return True

    def calculate_metrics(self):
        print(f"\n**********************************************************\n")

        print("Calculating metrics...")
        print(f"Total customers: {self.total_served_customers}")
        print(f"Total service time: {self.total_service_time}")
        print(f"Total wait time: {self.total_wait_time}")
        print(f"Total waiting customers: {self.total_waiting_customers}")
        print(f"\n**********************************************************\n")
        print(
            f"Average service time: {self.total_service_time/self.total_served_customers}")
        if self.total_waiting_customers == 0:
            print("Average wait time: 0")
        else:
            print(
                f"Average wait time: {self.total_wait_time/self.total_waiting_customers}"
            )

        print(
            f"Average number of customers in the queue: {(self.total_wait_time/self.simulation_time)}"
        )
        # Average number of customers in the system
        print(
            f"Average number of customers in the system : {self.total_service_time/self.simulation_time}"
        )
        print(f"Simulation Time: {self.simulation_time}")
        print(f"Total exit time: {self.total_exit_time}")

        print(f"\n**********************************************************\n")

        rho = self.arrival_rate / (self.num_servers * self.service_rate)
        print(f"Rho : {rho}")

        print(f"Gelmesi gereken result : {rho/(1-rho)}")

        print(f"Alinan sonuc: {self.total_exit_time/self.simulation_time}")

        print(f"\n**********************************************************\n")

        # waiting time in the system
        print(
            f"Waiting time in the system: {self.total_wait_time+self.total_service_time}"
        )

        # average waiting time in the system
        print(
            f"Average waiting time in the system (Ws OK): {(self.total_wait_time+self.total_service_time)/self.total_served_customers}"
        )

        # average number of customers in the system
        print(
            f"Average number of customers in the system (Ls) (OK): {(self.total_service_time/self.simulation_time)+(self.total_wait_time/self.simulation_time)}"
        )

        # average waiting time in the queue
        print(
            f"Average waiting time in the queue (Wq)(ok): {(self.total_wait_time/self.total_waiting_customers)}"
        )

        # average number of customers in the queue
        print(
            f"Average number of customers in the queue (Lq): {self.total_wait_time/self.simulation_time}"
        )


def simulation(simulation_customer_number, arrival_rate, service_rate, num_servers, priority_list):
    bankSimulation = BankSimulation(
        simulation_customer_number, arrival_rate, service_rate, num_servers, priority_list
    )
    bankSimulation.initialize_simulation()
    print("Simulation started.")
    arrived_customer_number = 0
    print(bankSimulation.list_customers)
    print("Simulation started.")
    """for i in range(len(bankSimulation.list_customers)):
        bankSimulation.list_customers[i].print_customer_details()
    print(bankSimulation.simulation_customer_number)
    print(bankSimulation.total_served_customers)
    print(bankSimulation.after_service_start_list)
    print(bankSimulation.queue)"""
    while bankSimulation.total_served_customers < bankSimulation.simulation_customer_number:
        print(f"Simulation time: {bankSimulation.simulation_time}")
        print(
            f"Total served customers: {bankSimulation.total_served_customers}")
        print(
            f"Total waiting customers: {bankSimulation.total_waiting_customers}")
        print(f"Total service time: {bankSimulation.total_service_time}")
        print(f"Total wait time: {bankSimulation.total_wait_time}")

        # Complete Service Event
        print("complete service event")

        """ This loop checks the customers service time.
                If a customer service time + start time is equal to
                current time, server that assigned for that customer
                will be free again. Also that customer will become served. """
        print(bankSimulation.after_service_start_list)

        if len(bankSimulation.after_service_start_list) != 0:
            after_service_start_loop = 0
            while after_service_start_loop < len(bankSimulation.after_service_start_list):
                customer = bankSimulation.after_service_start_list[after_service_start_loop]
                print(bankSimulation.simulation_time)
                print(customer.service_start_time + customer.service_time)
                if (customer.service_start_time + customer.service_time) <= bankSimulation.simulation_time:
                    print("complete service is done\n\n")

                    bankSimulation.servers[customer.server_no -
                                           1].is_available = True
                    customer.departure_time = bankSimulation.simulation_time
                    customer.wait_time = customer.service_start_time - customer.arrival_time
                    bankSimulation.total_wait_time += customer.wait_time
                    bankSimulation.total_served_customers += 1
                    bankSimulation.total_exit_time += (
                        customer.departure_time - customer.arrival_time)
                    bankSimulation.total_service_time += customer.service_time
                    # After the service is done, customer will be removed from the list.
                    bankSimulation.after_service_start_list.pop(
                        after_service_start_loop)
                    print(bankSimulation.after_service_start_list)
                after_service_start_loop += 1
        # Arrival Event
        """ This loop checks the customers arrival time. If a customer arrival time is equal to current time,
        servers are checked. If any server is available customer will be added to the after_service_list. This menas that
        customer is being served. If all servers are busy, customer will be added to the queue according to its priority."""
        print("arrival event")
        arrival_loop = 0
        while arrival_loop < len(bankSimulation.list_customers):
            if bankSimulation.simulation_time >= bankSimulation.list_customers[0].arrival_time:
                print("arrival yapar\n")
                arrived_customer_number += 1
                if bankSimulation.all_servers_busy() and (bankSimulation.queue.size) != 0:
                    arrived_customer = bankSimulation.list_customers[0]
                    bankSimulation.queue.enqueue(arrived_customer)
                    bankSimulation.total_waiting_customers += 1
                    bankSimulation.list_customers.pop(0)
                    bankSimulation.queue.print_queue_details()

                else:
                    # Serving the customer to server directly (No queue option)
                    for i in range(len(bankSimulation.servers)):
                        if bankSimulation.servers[i].is_available:
                            arrived_customer = bankSimulation.list_customers[0]
                            bankSimulation.list_customers.pop(0)

                            arrived_customer.server_no = i + 1
                            arrived_customer.arrival_time = bankSimulation.simulation_time
                            arrived_customer.service_start_time = bankSimulation.simulation_time
                            bankSimulation.after_service_start_list.append(
                                arrived_customer)
                            bankSimulation.servers[i].is_available = False
                            print(bankSimulation.after_service_start_list)
                            print("serving the customer to server directly\n\n")
                            break
            arrival_loop += 1

        # Start Service Event
        """ This loop checks the servers. If a server is available and queue is not empty, customer is taken from the queue 
        will be sended to that server and also be added to after_start_list. Customer's service start time will be set to current time. """
        print("start service event")
        # In here, the customers in the queue will be sended to the counters.
        for i in range(len(bankSimulation.servers)):

            if bankSimulation.servers[i].is_available == True and bankSimulation.queue.size() != 0:
                print("start service yapar\n\n")
                customer = bankSimulation.queue.dequeue()
                customer.server_no = i+1
                customer.service_start_time = bankSimulation.simulation_time
                bankSimulation.after_service_start_list.append(customer)
                bankSimulation.servers[i].is_available = False

        bankSimulation.simulation_time += 0.0005

    print("Simulation ended.")

    bankSimulation.calculate_metrics()


if __name__ == "__main__":
    # It is used to get the current directory
    current_directory = os.getcwd()

    filename = "output_file.txt"

    # It is used to create the output file in the current directory
    output_file = os.path.join(current_directory, filename)
    database = Database(0, 0, 0, 0, [])
    database.retrieve_data(filename)

    database.arrival_rate = database.create_arrival_rate(
        database.arrival_interval_list)
    database.service_rate = database.create_service_rate(
        database.total_service_time, database.total_customer)

    simulation(database.total_customer, database.arrival_rate,
               database.service_rate, database.no_of_servers, database.priority_list)

    # simulation(1024, 3, 4, 1)
