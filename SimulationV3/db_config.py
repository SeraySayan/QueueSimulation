import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

# Use a service account
cred = credentials.Certificate(
    'firestore491test-firebase-adminsdk-7l56g-2cd92c9238.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# No of servers can be read
employees_ref = db.collection(u'Employees')
docs = employees_ref.stream()
no_of_servers = 0
for doc in docs:
    no_of_servers += 1
print("No of servers: ", no_of_servers)

# All customer data can be read
customers_ref = db.collection(u'Tickets')
docs = customers_ref.stream()

total_customer = 0
total_wait_time = 0
total_service_time = 0
total_arrival_time = 0
priority = []
for doc in docs:
    # print(f'{doc.id} => {doc.to_dict()}')
    total_customer += 1

    arrival_time = str(doc.to_dict()['date_time'])
    arrival_timestamp = datetime.fromisoformat(arrival_time)
    total_arrival_time += arrival_timestamp.timestamp()
    process_time = doc.to_dict()['total_process_time']

    if process_time is not None:
        # if process_time has m and s in it
        if 'm' in process_time and 's' in process_time:
            process_time = process_time.split('m')
            process_time = float(process_time[0]) * \
                60 + float(process_time[1].split('s')[0])
        # if process_time has only s in it
        elif 's' in process_time:
            process_time = float(process_time.split('s')[0])

        total_service_time += process_time

    priority_value = doc.to_dict()['priority']
    if priority_value is not None:
        priority.append(priority_value)

    print("-------------------")
    print("Customer ID: ", doc.id)
    print("Arrival Time: ", arrival_time)
    print("Process Time: ", process_time)


print("-------------------")
print("Total Customer: ", total_customer)
print("Total Arrival Time: ", total_arrival_time)
print("Total Service Time: ", total_service_time)
print("Average Service Time: ", total_service_time/total_customer)
print("Priority List: ", priority)
print("Length of Priority List: ", len(priority))
