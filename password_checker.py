import requests
import hashlib
import sys


def reques_api_data(queryChar):
    url = "https://api.pwnedpasswords.com/range/" + queryChar
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f"Error fetching : {res.status_code},check the api and try again")
    return res


def get_password_leaks_cnt(hashes, hash_to_check):
    list_of_hashes = hashes.text.splitlines()
    for item in list_of_hashes:
        sub_list = item.split(":")
        if sub_list[0] == hash_to_check:
            return int(sub_list[1])
    return 0


def pwned_api_check(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1_password[:5], sha1_password[5:]
    response = reques_api_data(first5_char)
    return get_password_leaks_cnt(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(
                f"{password} was hacked {count} number of times, you should probably change it!")
        else:
            print(f"Your password is safe,carry on!")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
