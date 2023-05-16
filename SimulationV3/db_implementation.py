from datetime import datetime
from db_config import db


def find_server_no():
    # No of servers can be read
    employees_ref = db.collection(u'Employees')
    docs = employees_ref.stream()
    no_of_servers = 0
    for doc in docs:
        no_of_servers += 1
    print("No of servers: ", no_of_servers)


def print_customer_details(doc_id, arrival_time, process_time, priority):
    print("-------------------")
    print("Customer ID: ", doc_id)
    print("Arrival Time: ", arrival_time)
    print("Process Time: ", process_time)
    print("Priority: ", priority)


def print_metrics(total_customer, total_arrival_time, total_service_time, priority):
    print("-------------------")
    print("Total Customer: ", total_customer)
    print("Total Arrival Time: ", total_arrival_time)
    print("Total Service Time: ", total_service_time)
    print("Average Service Time: ", total_service_time/total_customer)
    print("Priority List: ", priority)
    print("Length of Priority List: ", len(priority))


def retrieve_data():

    total_customer = 0
    total_service_time = 0
    total_arrival_time = 0
    priority = []
    # All customer data can be read
    customers_ref = db.collection(u'Tickets')
    docs = customers_ref.stream()

    for doc in docs:
        total_customer += 1
        # Arrival time can be read as a string and converted to time object (seconds)
        arrival_time = doc.to_dict()['date_time']
        arrival_time = arrival_time.split('at')[1]
        arrival_time = arrival_time.strip()
        arrival_time = arrival_time.split(' ')[0]
        arrival_time = datetime.strptime(arrival_time, '%H:%M:%S').time()

        total_arrival_time += arrival_time.hour * 3600 + \
            arrival_time.minute * 60 + arrival_time.second

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

            total_service_time += process_time

        # Priority can be read as a string and converted to int and also added to a list
        priority_value = doc.to_dict()['priority']
        if priority_value is not None:
            priority.append(priority_value)

        # Print customer details
        print_customer_details(doc.id, arrival_time,
                               process_time, priority_value)

    # Print metrics
    print_metrics(total_customer, total_arrival_time,
                  total_service_time, priority)


def main():
    find_server_no()
    retrieve_data()


if __name__ == "__main__":
    main()
