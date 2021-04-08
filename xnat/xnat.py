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

    def list_projects(self):
        df = self.get_projects()
        return AttrDict({x: x for x in df.id})

    def get_projects(self):
        return self.session.get_df(
            "data/projects?accessible=true&users=true&format=csv"
        )

    def get_subjects(self, project):
        return self.session.get_df(f"data/projects/{project}/subjects?format=csv")

    def get_experiments(self, project, subject=None):
        if subject is None:
            return self.session.get_df(
                f"data/projects/{project}/experiments?format=csv"
            )
        else:
            return self.session.get_df(
                f"data/projects/{project}/subjects/{subject}/experiments?format=csv"
            )

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
