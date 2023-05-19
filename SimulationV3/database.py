from db_config import db
from datetime import datetime


class Database:
    total_customer = 0
    arrival_rate = 0
    service_rate = 0
    no_of_servers = 0
    priority_list = []
    total_service_time = 0
    total_arrival_time = 0
    arrival_interval_list = []
    arrival_interval_list.append(0)

    def __init__(self, total_customer, arrival_rate, service_rate, no_of_servers, priorty_list):
        self.total_customer = total_customer
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.no_of_servers = no_of_servers
        self.priorty_list = priorty_list

    def print_metrics(self, total_customer, arrival_rate, service_rate, no_of_servers, priority_list, total_service_time,
                      total_arrival_time, arrival_interval_list):
        print("-------------------")
        print("Total Customer: ", total_customer)
        print("Total Arrival Time: ", total_arrival_time)
        print("Total Service Time: ", total_service_time)
        print("Average Service Time: ", total_service_time/total_customer)
        print("Priority List: ", priority_list)
        print("Length of Priority List: ", len(priority_list))
        print("Arrival Interval List: ", arrival_interval_list)
        print("Length of Arrival Interval List: ", len(arrival_interval_list))
        print("Arrival Rate: ", arrival_rate)
        print("Service Rate: ", service_rate)
        print("No of servers: ", no_of_servers)

        print("-------------------")

    def create_arrival_rate(self, arrival_interval_list):
        sum_arrival = 0
        for i in range(len(arrival_interval_list)):
            sum_arrival += arrival_interval_list[i]

        arrival_rate = sum_arrival/len(arrival_interval_list)
        # convert into hours
        arrival_rate = 1/(arrival_rate/3600)
        print("Arrival Rate: ", arrival_rate)

        return arrival_rate

    def create_service_rate(self, total_service_time, total_customer):
        service_rate = total_service_time/total_customer
        # convert into hours
        service_rate = 1/(service_rate/3600)
        print("Service Rate: ", service_rate)

        return service_rate

    def find_server_no(self):
        # No of servers can be read
        employees_ref = db.collection(u'Employees')
        docs = employees_ref.stream()
        for doc in docs:
            self.no_of_servers += 1
        print("No of servers: ", self.no_of_servers)

    def retrieve_data(self):
        # All customer data can be read
        customers_ref = db.collection(u'Tickets')
        docs = customers_ref.stream()

        for doc in docs:
            self.total_customer += 1
            # Arrival time can be read as a string and converted to time object (seconds)
            arrival_time = doc.to_dict()['date_time']
            arrival_time = arrival_time.split('at')[1]
            arrival_time = arrival_time.strip()
            arrival_time = arrival_time.split(' ')[0]
            arrival_time = datetime.strptime(arrival_time, '%H:%M:%S').time()
            arrival_time = arrival_time.hour * 3600 + \
                arrival_time.minute * 60 + arrival_time.second
            self.total_arrival_time += arrival_time
            self.arrival_interval_list.append(
                abs(arrival_time - self.arrival_interval_list[-1]))

            # Process time can be read as a string and converted to time object (seconds)
            process_time = doc.to_dict()['total_process_time']
            if process_time is not None:
                # if process_time has min and s in it
                if 'min' in process_time and 's' in process_time:
                    process_time = process_time.split('min')
                    process_time[1] = process_time[1].split('s')[0]
                    process_time = float(process_time[0]) * \
                        60 + float((process_time[1].split('s'))[0])
                # if process_time has only s in it
                elif 's' in process_time:
                    process_time = float(process_time.split('s')[0])

                self.total_service_time += process_time

            # Priority can be read as a string and converted to int and also added to a list
            priority_value = doc.to_dict()['priority']
            if priority_value is not None:
                self.priority_list.append(priority_value)

            # Print customer details
            print_customer_details(doc.id, arrival_time,
                                   process_time, priority_value)


def print_customer_details(doc_id, arrival_time, process_time, priority):
    print("-------------------")
    print("Customer ID: ", doc_id)
    print("Arrival Time: ", arrival_time)
    print("Process Time: ", process_time)
    print("Priority: ", priority)
    print("-------------------")


main = Database(0, 0, 0, 0, [])
main.find_server_no()
main.retrieve_data()

main.arrival_rate = main.create_arrival_rate(main.arrival_interval_list)
main.service_rate = main.create_service_rate(
    main.total_service_time, main.total_customer)

main.print_metrics(main.total_customer, main.arrival_rate, main.service_rate, main.no_of_servers, main.priority_list, main.total_service_time,
                   main.total_arrival_time, main.arrival_interval_list)
