import time
from timeit import main

start_time = time.time()
# Call the main function
main()
end_time = time.time()

print(f"Total time taken: {end_time - start_time} seconds")