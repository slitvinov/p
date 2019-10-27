def ang(x, y):
    return (x - 320)/5.8

def mov(x, y):
    if y < 280:
        return 10
    else:
        return -1
