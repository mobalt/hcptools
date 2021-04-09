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

    def list_subjects(self, project):
        df = self.get_subjects(project)
        using_labels = {x.label: x.ID for x in df.itertuples()}
        using_id = {x.ID: x.ID for x in df.itertuples()}
        return AttrDict({**using_labels, **using_id})

    def get_subjects(self, project):
        return self.session.get_df(f"data/projects/{project}/subjects?format=csv")

    def list_experiments(self, project, subject=None):
        df = self.get_experiments(project, subject)
        using_labels = {x.label: x.ID for x in df.itertuples()}
        using_id = {x.ID: x.ID for x in df.itertuples()}
        return AttrDict({**using_labels, **using_id})

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

    def put_experiment(self, project, subject_label, experiment_label, xml=None):
        headers = {"Content-Type": "application/xml"}
        r = self.session.put(
            f"data/projects/{project}/subjects/{subject_label}/experiments/{experiment_label}?xsiType=xnat:mrSessionData",
            data=xml,
            headers=headers,
        )
        # status_code 201 - created, 200 - already exists
        assert (
            r.status_code == 201 or r.status_code == 200
        ), "Failure creating experiment."
        return r.content.decode()

    def experiment_xml(self, project, subject, experiment):
        r = self.session.get(
            f"data/projects/{project}/subjects/{subject}/experiments/{experiment}?format=xml&concealHiddenFields=true"
        )
        return r.content.decode()
