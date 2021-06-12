import requests
import bs4
from info import URL, USERNAME, PASSWORD


class SchoologyScraper:
    def __init__(self, url: str, username: str, password: str) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.session = requests.Session()

    def login(self):
        # initial login page
        res = self.session.get(self.url)
        soup = bs4.BeautifulSoup(res.content, "html.parser")
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
        soup = bs4.BeautifulSoup(res.content, "html.parser")
        form = soup.find("form")
        url = form.attrs["action"]
        saml = form.find("input", {"name": "SAMLResponse"}).attrs["value"]
        relayState = form.find("input", {"name": "RelayState"}).attrs["value"]

        # log in again through the redirect
        res = self.session.post(
            url,
            data={"SAMLResponse": saml, "RelayState": relayState},
        )

    def homepage(self):
        res = self.session.get(self.url + "home")
        # TODO: use requests_html or scrapy to render javascript


if __name__ == "__main__":
    scraper = SchoologyScraper(URL, USERNAME, PASSWORD)
    scraper.login()
    scraper.homepage()
