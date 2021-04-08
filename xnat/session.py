import re
from requests.auth import HTTPBasicAuth
from requests import Session


class XnatSession(Session):
    def __init__(self, base_url, credentials, *args, **kwargs):
        super(XnatSession, self).__init__(*args, **kwargs)
        self.base_url = base_url
        self.credentials = credentials
        self.csrf = None

    def request(self, method, url, auth=False, *args, **kwargs):
        # url = urljoin(self.prefix_url, url)
        url = self.base_url + url
        if auth:
            kwargs["auth"] = HTTPBasicAuth(*self.credentials)
        return super(XnatSession, self).request(method, url, *args, **kwargs)

    def login(self):
        print(f"Logging in to: {self.base_url}")

        try:
            r = self.post("login", auth=True)
            if r.status_code == 404:
                print("Server is down. No response.")
                return None
            assert r.status_code == 200, "Server is not responding."

            content = r.content.decode()
            self.csrf = re.search("csrfToken = '(.+?)'", content).group(1)
            return self

        except ConnectionError as err:
            print("Server is down. Proxy responded.")
            return None
