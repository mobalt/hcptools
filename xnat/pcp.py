import pandas as pd


class PipelineControlPanel:
    def __init__(self, xnat_instance, project, pipeline):
        self.xnat = xnat_instance
        self.project = project
        self.pipeline = pipeline
        self.api = f"{self.xnat.base_url}/xapi/pipelineControlPanel/project/{project}/pipeline/{pipeline}"

    def get_status(self):
        r = self.session.get(f"{self.api}/status?cached=true&condensed=false")
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            return df
        return None

    def update_cache(self, subset):
        endpoint_url = f"{self.api}/updateStatusEntities"
        entities = subset.fillna("").to_dict("records")
        r = self.session.post(endpoint_url, json=entities)
        return r.status_code == 200

    def set_status_to_reset(self, subset):
        endpoint_url = f"{self.api}/setValues?status=RESET"
        entities = subset.fillna("").to_dict("records")
        r = self.session.post(endpoint_url, json=entities)
        return r.status_code == 200

    def submit_pipeline(
        self,
        subset,
        parameters={
            "queuedLimit": "20",
            "overrideQueuedLimit": "false",
            "generateCinabStructure": "false",
            "resetCurrentActive": "false",
        },
    ):
        endpoint_url = f"{self.api}/pipelineSubmit"
        entities = subset.fillna("").to_dict("records")
        payload = dict(entities=entities, parameters=parameters)
        return self.session.post(endpoint_url, json=payload)

    def get_parameters(self):
        endpoint_url = f"{self.api}/submitParametersYaml"
        r = self.session.get(endpoint_url)
        return r.json()[0]

    def available_projects(self):
        r = self.session.get(
            f"{self.base_url}/data/projects?accessible=true&users=true&format=json"
        )
        return [x["id"] for x in r.json()["ResultSet"]["Result"]]

    def available_pipelines(self, project="CCF_MDD_STG"):
        r = self.session.get(
            f"{self.base_url}/xapi/pipelineControlPanel/project/{project}/statusSummary?includeSubgroupSummary=false"
        )
        return pd.DataFrame(r.json())
