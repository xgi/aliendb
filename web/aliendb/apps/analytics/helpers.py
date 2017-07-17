def update_average(field, value, tracked):
    field = (value + field * tracked) / (1 + tracked)
    