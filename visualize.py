#!python3

import glob
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from calc_stats import read_all_tests
from calc_stats import read_all_test_case_names


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
    passed_time_series = pd.Series(passed_time, dtype='float32')
    failed_time_series = pd.Series(failed_time, dtype='float32')
    passed_vs_failed = pd.Series([passed, failed], index=['PASSED', "FAILED"])
    # print('===')
    # print(passed_time)
    # print(failed_time)
    # print(passed_vs_failed)
    # return

    fig = plt.figure()
    fig.suptitle(name)
    plt.subplot(1, 3, 1)
    passed_time_series.plot.hist(
        grid=True, bins=10, rwidth=0.9, color='#2ecc71')
    # plt.title(name)
    plt.xlabel('seconds')
    plt.ylabel('counts')
    plt.grid(axis='y', alpha=0.75)

    plt.subplot(1, 3, 2)
    failed_time_series.plot.hist(
        grid=True, bins=10, rwidth=0.9, color='#e74c3c')
    plt.xlabel('seconds')
    plt.ylabel('counts')
    plt.grid(axis='y', alpha=0.75)

    plt.subplot(1, 3, 3)
    passed_vs_failed.plot.bar(grid=True)
    plt.ylabel('counts')
    plt.xticks(rotation=0, horizontalalignment="center")
    plt.grid(axis='y', alpha=0.75)

    print('draw {name} figure'.format(name=name))
    # plt.show()
    plt.savefig('figures/{name}.png'.format(name=name.replace(' – tidb-operator e2e suite', '')))
    plt.close()


if __name__ == '__main__':
    # collect_all_tests()
    all_tests = read_all_tests()
    test_cases = read_all_test_case_names()
    # test_cases = [
    #     '[tidb-operator][Stability] [Feature: AdvancedStatefulSet][Feature: AutoFailover] operator with advanced statefulset and short auto-failover periods delete the failed pod via delete-slots feature of Advanced Statefulset after failover – tidb-operator e2e suite'
    # ]
    for test_case in test_cases:
        draw_hist(all_tests, test_case)
