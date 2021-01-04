#!python3

import glob
import json

jenkins_data_dir = 'data/jenkins_api_data'
generated_data_dir = 'data/generated_data'


def collect_all_tests():
    all_list = []
    for filename in glob.glob('{data_dir}/*.json'.format(data_dir=jenkins_data_dir)):
        with open(filename, 'rt') as fp:
            tests = json.load(fp)
            all_list.extend(tests)
    with open('{data_dir}/all_tests.json'.format(data_dir=generated_data_dir), 'wt') as fp:
        json.dump(all_list, fp, ensure_ascii=False, indent=1)


def read_all_tests():
    with open('{data_dir}/all_tests.json'.format(data_dir=generated_data_dir), 'rt') as fp:
        return json.load(fp)


def gen_all_test_case_names(all_tests):
    names = set()
    for test in all_tests:
        names.add(test['name'])
    return list(names)


def read_all_test_case_names():
    with open('{data_dir}/all_test_case_names.json'.format(data_dir=generated_data_dir), 'rt') as fp:
        return json.load(fp)

if __name__ == '__main__':
    collect_all_tests()
    all_tests=read_all_tests()
    all_names=gen_all_test_case_names(all_tests)
    with open('{data_dir}/all_test_case_names.json'.format(data_dir=generated_data_dir), 'wt') as fp:
        json.dump(all_names, fp, ensure_ascii=False, indent=1)
