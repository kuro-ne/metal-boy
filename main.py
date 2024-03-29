import datetime
import os
import sqlite3
import sys
import time

import names

from db import DB
from email_temp import EmailTemp
from w3gg import W3GGSignUp
from dotenv import load_dotenv

load_dotenv()


def run():
    w3gg = W3GGSignUp()
    temp_mail = EmailTemp()
    db = DB()

    ref_code = db.get_active_referral_code()
    if not ref_code:
        print("No active referral code")
        return
    print("Referral Code: ", ref_code)

    name = names.get_full_name()
    username = name.lower().replace(" ", "")

    email = temp_mail.create_email(username)

    password = "12345678"

    w3gg.sign_up(email, password, ref_code)
    print(f"Name: {name}\nUsername: {username}\nEmail: {email}\nPassword: {password}\nRef Code: {ref_code}")

    verify_link = None
    for i in range(10):
        time.sleep(5)
        verify_link = temp_mail.verify_email(email)
        if verify_link:
            print("Verification Link : {} ".format(verify_link))
            break
        print("Waiting for email")

    if verify_link:
        w3gg.open_link(verify_link, name, username)

    data = {
        "name": name,
        "email": email,
        "password": password,
        "referral_code": ref_code,
        "registered": True,
        "verified": verify_link is not None,
        "created_at": datetime.datetime.now(),
    }

    db.insert(data)

    try:
        db.mongo_client.close()
        print("closed mongo client")
    except Exception as e:
        print(f"Error close mongo client : {e}")

    print("Done")


def main():
    n: int = int(float(os.getenv("NUM_LOOP", "1")))

    for i in range(n):
        print(f"Run {i + 1}")
        try:
            run()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
            continue

    # exit
    print("Done")

    sys.exit()


if __name__ == '__main__':
    main()
