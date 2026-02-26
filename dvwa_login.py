import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup

load_dotenv()

username = os.getenv(key="LOGIN_USERNAME", default="")
password = os.getenv(key="LOGIN_PASSWORD", default="")


def dvwa_login(baseURL: str):
    session = requests.Session()

    # login
    loginPage = session.get(f"{baseURL}/login.php")
    soupLogin = BeautifulSoup(loginPage.text, "html.parser")
    token = soupLogin.find("input", {"name": "user_token"})["value"]
    loginData = {
        "username": username,
        "password": password,
        "Login": "Login",
        "user_token": token,
    }

    session.get(f"{baseURL}/login.php", data=loginData, allow_redirects=True)

    # load secuirty page and change security lvl
    securityPage = session.get(f"{baseURL}/security.php")
    soupSecurity = BeautifulSoup(securityPage.text, "html.parser")
    tokenSecurity = soupSecurity.find("input", {"name": "user_token"})["value"]
    secuirtyData = {
        "security": "low",
        "seclev_submit": "submit",
        "user_token": tokenSecurity,
    }
    session.post(f"{baseURL}/security.php", data=secuirtyData, allow_redirects=True)

    # get cookies
    cookies = session.cookies.get_dict()
    cookieString = "; ".join(f"{k}={v}" for k, v in cookies.items())
    return cookieString
