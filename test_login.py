import utils.account_switcher as account_switcher
from config.accounts import ACCOUNTS
import time

if __name__ == "__main__":
    #account_switcher.logout()
    time.sleep(5)
    account_switcher.login(ACCOUNTS[0]["username"], ACCOUNTS[0]["password"])