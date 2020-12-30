#!python3

import glob
import json

import numpy as np
import pandas as pd

data_dir = 'jenkins_api_data'

def collect_all_tests():
    all_list = []
    for filename in glob.glob('{data_dir}/*.json'.format(data_dir=data_dir)):
        with open(filename, 'rt') as fp:
            tests = json.load(fp)
            all_list.extend(tests)
    with open('{data_dir}/all_tests.json'.format(data_dir=data_dir), 'wt') as fp:
        json.dump(all_list, fp, ensure_ascii=False, indent=1)

def read_all_tests():
    with open('{data_dir}/all_tests.json'.format(data_dir=data_dir), 'rt') as fp:
        return json.load(fp)

def draw_hist(all_tests, name):
    passed = 0
    failed = 0
    passed_time = []
    failed_time = []
    for test in all_tests:
        if test['name'] != name:
            continue
        if test['status'] == 'PASSED':
            passed += 1
            passed_time.append(test['duration'])
        elif test['status'] == 'FAILED':
            failed += 1
            failed_time.append(test['duration'])
    passed_time_series = pd.Series(np.array(passed_time))
    failed_time_series = pd.Series(np.array(failed_time))
    passed_time_series.plot.hist(grid=True, bins=20, rwidth=0.9, color='#607c8e')
    plt.title('Commute Times for 1,000 Commuters')
    plt.xlabel('Counts')
    plt.ylabel('Commute Time')
    plt.grid(axis='y', alpha=0.75)

if __name__ == '__main__':
    # collect_all_tests()
    all_tests = read_all_tests()
    draw_hist(all_tests, 'Up – tidb-operator')
