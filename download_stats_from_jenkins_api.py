#!python3

import json
import os
import requests


url_tpl = 'https://internal.pingcap.net/idc-jenkins/blue/rest/organizations/jenkins/pipelines/tidb-operator-pull-e2e-kind/runs/{job_num}/tests/?{test_param}&limit=101'
test_params = [
    'state=REGRESSION',
    'status=FAILED&state=%21REGRESSION',
    'status=SKIPPED',
    'state=FIXED',
    'status=PASSED'
]
data_dir = 'jenkins_api_data'

if __name__ == '__main__':
    for job_num in range(3650, 1, -1):
        result = []
        for param in test_params:
            url = url_tpl.format(job_num=job_num, test_param=param)
            body = requests.get(url).text
            try:
                obj_list = json.loads(body)
            except:
                print(body)
                continue
            if isinstance(obj_list, dict):
                print(obj_list)
                continue
            for obj in obj_list:
                result.append({
                    'name': obj['name'],
                    'duration': obj['duration'],
                    'state': obj['state'],
                    'status': obj['status'],
                    'stdout_href': 'https://internal.pingcap.net/idc-jenkins' + obj['_links']['stdOut']['href']
                })
        filename = '{data_dir}/{job_num}.json'.format(data_dir=data_dir, job_num=job_num)
        with open(filename, 'wt') as fp:
            json.dump(result, fp, ensure_ascii=False, indent=1)
        print('job {job_num} done'.format(job_num=job_num))
