
import datetime
import time
import random

def tprint(message):
    now = datetime.datetime.now()
    print(f'\033[{92}m[{now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}]\033[0m {message}')

def stprint(prefix, message, min_chars=1, max_chars=2, delay=0.1):
    print(prefix, end='', flush=True)
    i = 0
    time.sleep(1)
    while i < len(message):
        # Number of characters to stream in this iteration
        num_chars = random.randint(min_chars, max_chars)
        
        # Extract substring
        substring = message[i:i+num_chars]
        print(substring, end='', flush=True)
        
        # Wait for a small delay
        time.sleep(delay)

        # Move index forward
        i += num_chars