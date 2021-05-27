import requests
import hashlib
import sys


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching {res.status_code}, check the api and try again.')
    return res


def get_pass_leak_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    hashpass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    q_char, tail = hashpass[:5], hashpass[5:]
    response = request_api_data(q_char)
    return get_pass_leak_count(response, tail)


def main(line):
    count = pwned_api_check(line)
    if count:
        print(f'{line} has been leaked {count} times. Change it ... ')
    else:
        print('Your password Not found. continue using the same password..!')


if __name__ == '__main__':
    myfile = open("test.txt", "r")
    for line in myfile:
        main(line)
    myfile.close()
