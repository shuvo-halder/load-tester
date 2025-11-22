<<<<<<< HEAD
import requests
import threading
import time
import random
from datetime import datetime, timedelta


TARGET_URL = "http://odoo.acquirespot.xyz"
DURATION = 600  
CONCURRENT_USERS = 20 
REQUEST_INTERVAL = 1


start_time = datetime.now()
end_time = start_time + timedelta(seconds=DURATION)
total_requests = 0
successful_requests = 0
failed_requests = 0

def make_request():
    global total_requests, successful_requests, failed_requests
    
    while datetime.now() < end_time:
        try:
            response = requests.get(TARGET_URL, timeout=10)
            total_requests += 1
            
            if response.status_code == 200:
                successful_requests += 1
                print(f"Succesfull Request: {response.status_code}, Time: {response.elapsed.total_seconds():.2f}s")
            else:
                failed_requests += 1
                print(f"Failled Request: {response.status_code}")
                
        except Exception as e:
            failed_requests += 1
            print(f"Error: {str(e)}")
            
        time.sleep(REQUEST_INTERVAL)

def main():
    print(f"Starting load testing {TARGET_URL} ")
    print(f"Time: {DURATION} Seconds")
    print(f"Active Users: {CONCURRENT_USERS}")
    
    threads = []
    
    
    for _ in range(CONCURRENT_USERS):
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()
    
    
    while datetime.now() < end_time:
        elapsed = (datetime.now() - start_time).total_seconds()
        remaining = DURATION - elapsed
        print(f"Taking times: {elapsed:.1f}s, Remaining Time: {remaining:.1f}s")
        time.sleep(10)
    
    
    for thread in threads:
        thread.join()
    
    
    print("\nReport Load Testing")
    print(f"Total Request: {total_requests}")
    print(f"Succesfully Request: {successful_requests}")
    print(f"Failled Request: {failed_requests}")
    print(f"Successfull rate: {(successful_requests/total_requests)*100:.2f}%")

if __name__ == "__main__":
    main()
=======
import requests
import threading
import time
import random
from datetime import datetime, timedelta


TARGET_URL = "http://103.131.144.51:8089"  
DURATION = 600  
CONCURRENT_USERS = 20 
REQUEST_INTERVAL = 1


start_time = datetime.now()
end_time = start_time + timedelta(seconds=DURATION)
total_requests = 0
successful_requests = 0
failed_requests = 0

def make_request():
    global total_requests, successful_requests, failed_requests
    
    while datetime.now() < end_time:
        try:
            response = requests.get(TARGET_URL, timeout=10)
            total_requests += 1
            
            if response.status_code == 200:
                successful_requests += 1
                print(f"Succesfull Request: {response.status_code}, Time: {response.elapsed.total_seconds():.2f}s")
            else:
                failed_requests += 1
                print(f"Failled Request: {response.status_code}")
                
        except Exception as e:
            failed_requests += 1
            print(f"Error: {str(e)}")
            
        time.sleep(REQUEST_INTERVAL)

def main():
    print(f"Starting load testing {TARGET_URL} ")
    print(f"Time: {DURATION} Seconds")
    print(f"Active Users: {CONCURRENT_USERS}")
    
    threads = []
    
    
    for _ in range(CONCURRENT_USERS):
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()
    
    
    while datetime.now() < end_time:
        elapsed = (datetime.now() - start_time).total_seconds()
        remaining = DURATION - elapsed
        print(f"Taking times: {elapsed:.1f}s, Remaining Time: {remaining:.1f}s")
        time.sleep(10)
    
    
    for thread in threads:
        thread.join()
    
    
    print("\nReport Load Testing")
    print(f"Total Request: {total_requests}")
    print(f"Succesfully Request: {successful_requests}")
    print(f"Failled Request: {failed_requests}")
    print(f"Successfull rate: {(successful_requests/total_requests)*100:.2f}%")

if __name__ == "__main__":
    main()
>>>>>>> 0c6de57fd0856ca893190f47687de645576055e1
