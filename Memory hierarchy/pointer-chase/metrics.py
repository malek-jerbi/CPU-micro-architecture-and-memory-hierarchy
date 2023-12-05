import csv
import datetime
import math
import time


class Address(object):
    def __init__(self, address_line, zipcode):
        self.address_line = address_line
        self.zipcode = zipcode


class Payment(object):
    def __init__(self, dollars, cents, time):
        self.dollars = dollars
        self.cents = cents
        self.time = time


class Users(object):
    def __init__(self, user_ids, names, ages, addresses, payments):
        self.user_ids = user_ids
        self.names = names
        self.ages = ages
        self.addresses = addresses
        self.payments = payments


def average_age(users):
    total = 0
    for age in users.ages:
        total += age
    return total / len(users.ages)


def average_payment_amount(users):
    amount = 0
    count = 0
    for payment in users.payments:
        count += len(payment)
        for p in payment:
            amount += p.dollars + p.cents / 100
    return amount / count


def stddev_payment_amount(users):
    mean = average_payment_amount(users)
    squared_diffs = 0
    count = 0
    for payment in users.payments:
        count += len(payment)
        for p in payment:
            amount = p.dollars + p.cents / 100
            diff = amount - mean
            squared_diffs += diff * diff
    return math.sqrt(squared_diffs / count)


def load_data():
    users = None
    with open('users.csv') as f:
        uids = []
        addresses = []
        names = []
        ages = []

        addresses = []
        payments = []
        for line in csv.reader(f):
            uid, name, age, address_line, zip_code = line
            addresses.append(Address(address_line, zip_code))
            uids.append(int(uid))
            names.append(name)
            ages.append(int(age))
            payments.append([])
        users = Users(uids, names, ages, addresses, payments)
    with open('payments.csv') as f:
        for line in csv.reader(f):
            amount, timestamp, uid = line
            payment = Payment(
                dollars=float(int(amount)//100),
                cents=float(amount) % 100,
                time=datetime.datetime.fromisoformat(timestamp))
            users.payments[int(uid)].append(payment)
    return users


if __name__ == '__main__':
    t = time.perf_counter()
    users = load_data()
    print(f'Data loading: {time.perf_counter() - t:.3f}s')
    t = time.perf_counter()
    assert abs(average_age(users) - 59.626) < 0.01
    assert abs(stddev_payment_amount(users) - 288684.849) < 0.01
    assert abs(average_payment_amount(users) - 499850.559) < 0.01
    print(f'Computation {time.perf_counter() - t:.3f}s')
