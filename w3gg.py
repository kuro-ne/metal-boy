import time

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright


# Use Playwright to sign up for a new account to W3GG.io

class W3GGSignUp:
    def __init__(self):
        self.base_url = "https://w3gg.io"
        self.HEADLESS = True

    def sign_up(self, email, password, referral_code):
        with sync_playwright() as pw:
            # create browser instance
            browser = pw.chromium.launch(
                # we can choose either a Headful (With GUI) or Headless mode:
                headless=self.HEADLESS,
            )
            # create context
            # using context we can define page properties like viewport dimensions
            context = browser.new_context(

                # most common desktop viewport is 720p
                viewport={"width": 1280, "height": 720}

                # most common desktop viewport is 1920x1080
                # viewport={"width": 1920, "height": 1080}
            )
            # create page aka browser tab which we'll be using to do everything
            page = context.new_page()

            # navigate to the website
            page.goto(self.base_url)

            # wait for page to load
            page.wait_for_timeout(5)

            # go to the sign up page with referral code
            url_ref = self.base_url + "/ref/" + referral_code
            page.goto(url_ref)

            # wait for page to load
            page.wait_for_timeout(5)

            # fill in the sign up form
            page.click('input[type="text"]')
            # page.fill('input[type="text"]', email)
            page.get_by_placeholder('Email').press_sequentially(email)
            time.sleep(1)

            page.click('input[type="password"]')
            # page.fill('input[type="password"]', password)
            page.get_by_placeholder('Password').press_sequentially(password)
            time.sleep(1)

            # click the sign up button class=w-full btn-primary
            page.click('button[class="w-full btn-primary"]')
            time.sleep(5)
            page.wait_for_timeout(30)

            time.sleep(10)

    def open_link(self, link, fullname=None, username=None):
        with sync_playwright() as pw:
            # create browser instance
            browser = pw.chromium.launch(
                # we can choose either a Headful (With GUI) or Headless mode:
                headless=self.HEADLESS,
            )
            # create context
            # using context we can define page properties like viewport dimensions
            context = browser.new_context(
                # most common desktop viewport is 720p
                viewport={"width": 1280, "height": 720}

                # viewport={"width": 1920, "height": 1080}
            )
            # create page aka browser tab which we'll be using to do everything
            page = context.new_page()

            # navigate to the website
            page.goto(link)

            # wait for page to load
            page.wait_for_timeout(30)

            time.sleep(10)

            # update profile
            # https://w3gg.io/dashboard/user?position=setting
            profile_url = f"{self.base_url}/dashboard/user?position=setting"
            page.goto(profile_url)
            page.wait_for_timeout(10)

            # fill in the profile form
            page.get_by_placeholder("Full name").click()
            page.get_by_placeholder("Full name").press_sequentially(fullname)
            time.sleep(1)
            page.get_by_placeholder("Username").click()
            page.get_by_placeholder("Username").press_sequentially(username)
            time.sleep(1)

            # click the update button
            page.click('button[class="btn-primary btn-medium gap-2"]')

            page.wait_for_timeout(5)

            time.sleep(5)
