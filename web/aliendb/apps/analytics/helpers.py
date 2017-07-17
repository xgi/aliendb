def update_average(field, value, tracked):
    return (value + field * tracked) / (1 + tracked)
    