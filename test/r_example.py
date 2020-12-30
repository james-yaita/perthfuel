from r_base import get_prices
from r_base import fakeData


def assertEqual(a, b):
    assert a == b, '{} and {} does not match'.format(a, b)


def allCheaper():
    specimen = get_prices(day='Today')
    result = True

    for i in range(len(specimen) - 2):
        if specimen[i]['price'] > specimen[i + 1]['price']:
            result = False
    return result


def assertLessThanEqual(a, b):
    return a <= b


def allNumber2():
    result = True

    specimen = get_prices(day='Today',fakeData)

    for previous, current in zip(specimen, specimen[1:]):
        if not assertLessThanEqual(previous['price'],current['price']):
            result = Flase


    return result

def allNumber():
    result = True
    specimen = get_prices(day='Today')

    for i in range(len(specimen) - 1):
        if not (type(specimen[i]['price']) is int or float):
            result = False
    return result

print("Test Run: Start")
assert type(get_prices(day='Today')) is list

if not type(get_prices(day='Today')) is list:
    raise Exception('Result is not a list')


assert allNumber() is True
assert allNumber2() is True
assert allCheaper() is True


print("Test Run: End")
