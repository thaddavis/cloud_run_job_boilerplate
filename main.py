import json
import os
import sys

from helpers.test import test

import numpy as np

# Retrieve Job-defined env vars
TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)
# Retrieve User-defined env vars
SLEEP_MS = os.getenv("SLEEP_MS", 0)
FAIL_RATE = os.getenv("FAIL_RATE", 0)

# Define main script
def main():
    """
    Testing
    """
    print(f"Starting Task #{TASK_INDEX}, Attempt #{TASK_ATTEMPT}...")
    test()

    arr = np.array([1, 2, 3, 4, 5])
    # Print the array
    print("Array:", arr)
    # Basic Operations
    print("Sum:", np.sum(arr))           # Sum of elements
    print("Mean:", np.mean(arr))         # Mean of elements
    print("Max:", np.max(arr))           # Maximum value
    print("Min:", np.min(arr))           # Minimum value

    print(f"Completed Task #{TASK_INDEX}.")

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        message = (
            f"Task #{TASK_INDEX}, " + f"Attempt #{TASK_ATTEMPT} failed: {str(err)}"
        )

        print(json.dumps({"message": message, "severity": "ERROR"}))
        sys.exit(1)  # Retry Job Task by exiting the process