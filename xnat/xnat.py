import pandas as pd

from utils import AttrDict
from xnat.pcp import PipelineControlPanel
from xnat.session import XnatSession


class Xnat:
    def __init__(self, server, credentials):
        self.session = XnatSession(server.base_url, credentials)
        self.session.login()

    def pcp(self, project, pipeline):
        return PipelineControlPanel(self, project, pipeline)

    def available_projects(self):
        r = self.session.get("data/projects?accessible=true&users=true&format=json")
        return AttrDict({x["id"]: x["id"] for x in r.json()["ResultSet"]["Result"]})

    def get_resources(self, experiment_id):
        url = f"REST/experiments/{experiment_id}/resources"
        r = self.session.get(url, auth=True)
        results = r.json()["ResultSet"]["Result"]
        df = pd.DataFrame(results)
        return df.drop(
            columns=[
                "cat_desc",
                "cat_id",
                "format",
                "category",
                "element_name",
                "content",
                "tags",
            ]
        )
