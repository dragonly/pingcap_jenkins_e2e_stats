#!python3

import json

import requests


def is_job_aborted_at_run_stage(url):
    body = requests.get(url).text
    pipeline = json.loads(body)
    if len(pipeline) < 5:
        return False
    run_stage = pipeline[4]
    print(run_stage)
    if run_stage['displayName'] != 'Run':
        return False
    return run_stage['result'] == 'ABORTED' and run_stage['durationInMillis'] > 3600000

if __name__ == '__main__':
    url_tpl = 'https://internal.pingcap.net/idc-jenkins/blue/rest/organizations/jenkins/pipelines/tidb-operator-pull-e2e-kind/runs/{job_num}/nodes/'
    for job_num in range(1604, 3700):
        url = url_tpl.format(job_num=job_num)
        aborted = is_job_aborted_at_run_stage(url)
        print(job_num, aborted)
        if aborted:
            exit()
