#!python3

import json
import os

import requests

from calc_stats import read_all_tests

url_tpl = 'https://internal.pingcap.net/idc-jenkins/blue/rest/organizations/jenkins/pipelines/tidb-operator-pull-e2e-kind/runs/{job_num}/tests/'
api_data_dir = 'data/jenkins_api_data'
failure_data_dir = 'data/failure_summary'

def download_job_test_result(job_num):
    result = []
    url = url_tpl.format(job_num=job_num)
    body = requests.get(url).text
    try:
        test_list = json.loads(body)
    except:
        print(body)
        return
    if not isinstance(test_list, list):
        print(test_list)
        return
    for test in test_list:
        result.append({
            'name': test['name'],
            'duration': test['duration'],
            'state': test['state'],
            'status': test['status'],
            'stdout_href': 'https://internal.pingcap.net/idc-jenkins' + test['_links']['stdOut']['href'],
            'job_num': job_num,
        })
    filename = '{api_data_dir}/{job_num}.json'.format(api_data_dir=api_data_dir, job_num=job_num)
    with open(filename, 'wt') as fp:
        json.dump(result, fp, ensure_ascii=False, indent=1)
    print('job {job_num} done'.format(job_num=job_num))

def _get_log_failure_summary(url):
    body = requests.get(url).text
    lines = body.split('\n')
    failure_sources = []
    for i, line in enumerate(lines):
        if '[Fail]' in line:
            failure_sources.append({
                'it': line,
                'source': lines[i+1]
            })
    return failure_sources

def download_all_failure_summaries(all_tests):
    for test in all_tests:
        name = test['name']
        if name != 'Test – tidb-operator':
            continue
        url = test['stdout_href']
        job_num = test['job_num']
        print(url)
        summary = _get_log_failure_summary(url)
        print(summary)
        if summary != []:
            filename = '{failure_data_dir}/{job_num}.json'.format(failure_data_dir=failure_data_dir, job_num=job_num)
            with open(filename, 'wt') as fp:
                json.dump(summary, fp, ensure_ascii=False, indent=1)

if __name__ == '__main__':
    # for job_num in range(3650, 1000, -1):
    #     download_job_test_result(job_num)

    all_tests = read_all_tests()
    download_all_failure_summaries(all_tests)
