import pandas as pd
import io
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

    def get_df(self, url, auth=False, *args, **kwargs):
        r = self.get(url, auth=auth, *args, **kwargs)
        csv_buffer = io.StringIO(r.content.decode())
        return pd.read_csv(csv_buffer)

    def get_df_json(self, url, auth=False, *args, **kwargs):
        r = self.get(url, auth=auth, *args, **kwargs)
        return pd.DataFrame(r.json())

    def post_df(self, url, df, auth=False, *args, **kwargs):
        # fillna is important because json can't deal with pd.NaN
        json = df.fillna("").to_dict("records")
        r = self.post(url, json=json)
        if r.status_code != 200:
            print("Post not okay: ", url)
        return r

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
