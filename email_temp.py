import random

import requests
from bs4 import BeautifulSoup


class EmailTemp:
    def __init__(self):
        self.base_url = 'https://tempmail.plus/api'
        self.pin = "101010"
        self.hostnames = [
            "mailto.plus",
            "fexpost.com",
            "fexbox.org",
            "mailbox.in.ua",
            "rover.info",
            "chitthi.in",
            "fextemp.com",
            "any.pink",
            "merepost.com",
        ]

    def create_email(self, username):
        url = self.base_url + '/box'

        # get random hostname
        hostname = random.choice(self.hostnames)
        email = f"{username}@{hostname}"

        data = {
            "pin": self.pin,
            "ttl_minutes": 10080,
            "email": email
        }

        header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        response = requests.post(url, data=data, headers=header)

        print(response.json())

        if response.status_code == 200:
            return email
        else:
            return None

    def get_emails(self, email):
        params = {
            'email': email,
            'first_id': '0',
            'epin': self.pin,
            'limit': 20
        }

        url = f'{self.base_url}/mails'
        response = requests.get(url, params=params)

        print(response.json())

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_mail(self, email, mail_id):
        params = {
            'email': email,
            'first_id': '0',
            'epin': self.pin,
        }

        url = f'{self.base_url}/mails/{mail_id}'
        response = requests.get(url, params=params)

        print(response.json())

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_verification(self, email):
        resp = self.get_emails(email)

        if not resp:
            return None

        mail_list = resp.get('mail_list', [])

        if mail_list:
            for mail in mail_list:
                if mail.get("subject") == 'Verify your W3GG account email':
                    mail_id = mail.get("mail_id", 0)
                    mail = self.get_mail(email, mail_id)
                    if mail:
                        return mail.get('html', None)
        return None

    def verify_email(self, email):
        html = self.get_verification(email)
        verify_link = None

        if html:
            soup = BeautifulSoup(html, 'html.parser')

            # find a href tag, with class button
            for link in soup.findAll('a', {'class': 'button'}):
                try:
                    verify_link = link.get('href', None)
                except KeyError:
                    pass

        return verify_link
