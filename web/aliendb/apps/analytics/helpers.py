def update_average(field, value, tracked) -> float:
    """Updates a previously calculated average with a new value.

    Args:
        field: the current average;
        value: the new value to include in the average;
        tracked: the number of elements used to form the _original_ average;

    Returns:
        float: the updated average
    """
    return (value + field * tracked) / (1 + tracked)
