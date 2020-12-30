#!python3

from datetime import datetime
import re
import requests

url_tpl = 'https://internal.pingcap.net/idc-jenkins/blue/rest/organizations/jenkins/pipelines/tidb-operator-pull-e2e-kind/runs/{job_num}/log/?start=0'

def parse_time(text):
    time_str = re.match(r'\[(.+)\]', text).group(1)
    time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    print(time)
    return time

def local_pv_time():
    job_num = 3632
    url = url_tpl.format(job_num=job_num)
    print(url)
    log = requests.get(url).text.splitlines()
    print('log downloaded')
    start_str = 'info: waiting for pods of daemonset kube-system/local-volume-provisioner are ready'
    end_str = 'info: all pods of daemonset kube-system/local-volume-provisioner are ready'
    for line in log:
        if start_str in line:
            start_time = parse_time(line)
            continue
        if end_str in line:
            end_time = parse_time(line)
            continue
    print('installing local-volume-provisioner takes {time}'.format(time=(end_time-start_time)))

if __name__ == '__main__':
    # TODO: parse start, end, static section, test section
    local_pv_time()
