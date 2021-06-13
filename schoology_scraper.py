import requests
from bs4 import BeautifulSoup
import json


class SchoologyScraper:
    def __init__(self, url: str, username: str, password: str) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.login()

    def login(self):
        """
        Login to schoology.
        This method is run on the creation of a SchoologyScraper object.
        """
        # initial login page
        res = self.session.get(self.url)
        soup = BeautifulSoup(res.content, "html.parser")
        url = soup.find(id="options").attrs["action"]

        # login in
        res = self.session.post(
            url,
            data={
                "UserName": self.username,
                "Password": self.password,
                "AuthMethod": "FormsAuthentication",
            },
        )
        soup = BeautifulSoup(res.content, "html.parser")
        form = soup.find("form")
        url = form.attrs["action"]
        saml = form.find("input", {"name": "SAMLResponse"}).attrs["value"]
        relayState = form.find("input", {"name": "RelayState"}).attrs["value"]

        # log in again through the redirect
        res = self.session.post(
            url,
            data={"SAMLResponse": saml, "RelayState": relayState},
        )

        return res.url == self.url + "home"

    def get_assignments(self, t_from: int, t_to: int):
        """
        Returns a list of assignments within the given timeframe.
        All time is in seconds from epoch.

        Keyword arguments:
        t_from -- The time that the calendar will start at
        t_to -- The time that the calendar will end at
        """
        res = self.session.get(self.url + "user-calendar")
        res = self.session.get(
            f"{res.url}?ajax=1&start={t_from}&end={t_to}&_=1623553551138"
        )
        data = json.loads(res.content)

        return data
