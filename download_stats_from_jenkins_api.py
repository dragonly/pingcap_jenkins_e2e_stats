#!python3

import json
import os
import requests


url_tpl = 'https://internal.pingcap.net/idc-jenkins/blue/rest/organizations/jenkins/pipelines/tidb-operator-pull-e2e-kind/runs/{job_num}/tests/'
data_dir = 'data/jenkins_api_data'

def download_job_test_result(job_num):
    result = []
    url = url_tpl.format(job_num=job_num)
    body = requests.get(url).text
    try:
        test_list = json.loads(body)
    except:
        print(body)
        continue
    if not isinstance(test_list, list):
        print(test_list)
        continue
    for test in test_list:
        result.append({
            'name': test['name'],
            'duration': test['duration'],
            'state': test['state'],
            'status': test['status'],
            'stdout_href': 'https://internal.pingcap.net/idc-jenkins' + test['_links']['stdOut']['href']
        })
    filename = '{data_dir}/{job_num}.json'.format(data_dir=data_dir, job_num=job_num)
    with open(filename, 'wt') as fp:
        json.dump(result, fp, ensure_ascii=False, indent=1)
    print('job {job_num} done'.format(job_num=job_num))

if __name__ == '__main__':
    for job_num in range(3650, 1, -1):
        download_job_test_result(job_num)
