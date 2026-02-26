import requests
from bs4 import BeautifulSoup
import sys

# python dvwa_login.py xxx.xxx.xxx.xxx


def dvwa_login(base_url: str):
    session = requests.Session()

    loginPage = session.get(f"{base_url}/login.php")
    soup = BeautifulSoup(loginPage.text, "html.parser")
    token = soup.find("input", {"name": "user_token"})["value"]
    loginData = {
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": token,
    }
    session.post(f"{base_url}/login.php", data=loginData, allow_redirects=True)

    securityPage = session.get(f"{base_url}/security.php")
    soupSecurity = BeautifulSoup(securityPage.text, "html.parser")
    tokenSecurity = soupSecurity.find("input", {"name": "user_token"})["value"]
    securityData = {
        "security": "low",
        "seclev_submit": "Submit",
        "user_token": tokenSecurity,
    }
    session.post(f"{base_url}/security.php", data=securityData, allow_redirects=True)

    cookies = session.cookies.get_dict()
    cookieString = "; ".join(f"{k}={v}" for k, v in cookies.items())

    return cookieString


if __name__ == "__main__":
    result = dvwa_login(base_url=sys.argv[1])
    print(result)
