import threading
import time
from utilities import update_prices_for_exchanges


def update_exchanges():
    """
        function that should be called every minute to check for price changes in currencies
    """
    for i in range(6):
        threading.Thread(target=update_prices_for_exchanges).start()
        time.sleep(10)
