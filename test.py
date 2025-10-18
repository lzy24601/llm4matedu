from utils.cal_time import timer


@timer
def test():
    return 1 + 1


print(test.__name__)
test()
