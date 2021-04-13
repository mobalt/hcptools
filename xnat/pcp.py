import pandas as pd


class PipelineControlPanel:
    def __init__(self, xnat_instance, project, pipeline=None):
        self.xnat = xnat_instance
        self.project = project
        self.pipeline = pipeline
        self.api = f"xapi/pipelineControlPanel/project/{project}/pipeline/{pipeline}"

    def get_status(self):
        return self.xnat.session.get_df_json(
            f"{self.api}/status?cached=true&condensed=false"
        )

    def update_cache(self, subset):
        endpoint_url = f"{self.api}/updateStatusEntities"
        return self.xnat.session.post_df(endpoint_url, subset)

    def set_status_to_reset(self, subset):
        endpoint_url = f"{self.api}/setValues?status=RESET"
        return self.xnat.session.post_df(endpoint_url, subset)

    def submit_pipeline(
        self,
        subset,
        queuedLimit=20,
        generateCinabStructure=False,
        overrideQueuedLimit=False,
        resetCurrentActive=False,
    ):
        endpoint_url = f"{self.api}/pipelineSubmit"
        parameters = dict(
            queuedLimit=queuedLimit,
            overrideQueuedLimit=overrideQueuedLimit,
            generateCinabStructure=generateCinabStructure,
            resetCurrentActive=resetCurrentActive,
        )
        df_as_obj = subset.fillna("").to_dict("records")
        payload = dict(
            entities=df_as_obj,
            parameters=parameters,
        )
        return self.xnat.session.post(endpoint_url, json=payload)

    def get_pipeline_summary(self):
        return self.xnat.session.get_df_json(
            f"xapi/pipelineControlPanel/project/{self.project}/statusSummary?includeSubgroupSummary=false"
        )

    def get_pipeline_settings(self):
        return self.xnat.session.get_df_json(
            f"xapi/pipelineControlPanelConfig/{self.project}/pipelines"
        )
