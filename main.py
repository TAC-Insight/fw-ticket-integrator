import time
import schedule
from query import run_query

# Initial run
run_query()

# Schedule the query to run every minute
schedule.every(1).minutes.do(run_query)

# Run loop
while True:
    schedule.run_pending()
    time.sleep(1)
