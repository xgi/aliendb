import datetime

def update_average(field, value, tracked) -> float:
    """Updates a previously calculated average with a new value.

    Args:
        field: the current average;
        value: the new value to include in the average;
        tracked: the number of elements used to form the _original_ average

    Returns:
        float: the updated average
    """
    return (value + field * tracked) / (1 + tracked)

def timestamp_to_ms(timestamp) -> float:
    """Converts a Django DateTimeField to milliseconds since the Unix epoch.

    To account for variations between the exact time that data is retrieved,
    this function actually rounds the time to the nearest second.

    Args:
        timestamp: a Django DateTimeField to be converted

    Returns:
        float: the timestamp represented as milliseconds from the Unix epoch
    """
    epoch = datetime.datetime.utcfromtimestamp(0)
    seconds = int((timestamp - epoch).total_seconds())
    return seconds * 1000.0

def remove_near_elements(arr, time_difference, time_idx) -> list:
    """Remove list elements within a specified time difference.

    Args:
        arr: a list of arrays or tuples
        time_difference: the minimum time difference between elements
        time_idx: the index of each arr element with an integer time

    Returns:
        list: arr with certain elements removed, if necessary
    """
    new = []
    time_to_beat = 0
    for i in range(len(arr)):
        if arr[i][time_idx] >= time_to_beat:
            new.append(arr[i])
            time_to_beat = arr[i][time_idx] + time_difference
    return new