from io import BytesIO

import paramiko
from paramiko import SSHClient
import pandas as pd
import xml.etree.ElementTree as ET


class SSH:
    def __init__(self, server, username="HCPpipeline", password=None, *args, **kwargs):
        self.server = server.host
        self.username = username
        self.password = password
        self.args = args
        self.kwargs = kwargs
        self.client = None
        self.reconnect()

    def reconnect(self):
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        client.connect(
            self.server,
            username=self.username,
            password=self.password,
            *self.args,
            **self.kwargs,
        )
        self.client = client

    def exec(self, command):
        # Command can be something like "cd /data/intradb && pwd" and result will be "/data/intradb"
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode()

    def write_file(self, content, filename, make_executable=False):
        ftp = self.client.open_sftp()
        ftp.putfo(BytesIO(content.encode()), filename)
        ftp.close()
        if make_executable:
            self.client.exec_command(f"chmod +x {filename}")

    def qstat(self):
        content = self.exec("qstat -lxfu HCPpipeline")
        jobs = []
        root = ET.fromstring(content)

        for job in root.findall("Job"):
            job_name = job.find("Job_Name").text
            entity, pipeline, step, _ = job_name.split(".")
            start_time = (
                job.find("start_time").text
                if job.find("start_time") is not None
                else ""
            )
            remaining_time = (
                job.find("Walltime").find("Remaining").text
                if job.find("Walltime") is not None
                else ""
            )

            jobs.append(
                dict(
                    entity=entity,
                    pipeline=pipeline,
                    step=step,
                    id=job.find("Job_Id").text,
                    state=job.find("job_state").text,
                    queue=job.find("queue").text,
                    created_time=job.find("ctime").text,
                    start_time=start_time,
                    remaining_time=remaining_time,
                    stdout=job.find("Output_Path").text,
                    stderr=job.find("Error_Path").text,
                )
            )

        df = pd.DataFrame(jobs)
        df.start_time = pd.to_datetime(df.start_time, unit="s")
        df.created_time = pd.to_datetime(df.created_time, unit="s")
        df.remaining_time = pd.to_numeric(df.remaining_time) / 3600

        df.stdout = df.stdout.str.slice(16)
        df.stderr = df.stderr.str.slice(16)
        return df

    def ls(self, args="", working_dir="."):
        results = self.exec(f"cd {working_dir} && ls {args}").split("\n")

        # sometimes extra blank lines appear, filter those out
        results = [x for x in results if x.strip()]

        return results
