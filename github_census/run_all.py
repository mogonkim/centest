#!/usr/bin/env python

import os,sys,platform
import json,hashlib
from collections import defaultdict
from util import *
from subprocess import call
import copy

def extract_fields(dataset,name,out_dir):
    data = {k: v[name] for k,v in dataset.iteritems() if type(v) == type({})}
    data["left_mono"] = data["data"]["left"]["mono"]
    data["left_rgb"] = data["data"]["left"]["rgb"]
    data["right_mono"] = data["data"]["right"]["mono"]
    data["right_rgb"] = data["data"]["right"]["rgb"]
    data["output_disp"] = os.path.join(out_dir,name + '_disp.pfm')
    data["output_conf"] = os.path.join(out_dir,name + '_conf.pfm')
    data["costs"] = os.path.join(out_dir,name + '_cost.pmm')
    return data

def run_alg(dataset,algorithm,out_dir):
    for name in dataset['names']:
        #print name
        data = extract_fields(dataset,name,out_dir)
        alg_copy = copy.deepcopy(data)
        alg_copy['gt'] = ''
        alg_copy['gt_mask'] = ''
        algorithm.update(alg_copy)
        cfg_path = os.path.join(out_dir,name + '_config.json')
        with open(cfg_path,'w') as fp:
            json.dump(algorithm,fp)

        with cd(algorithm['dir']):
            call([algorithm['command'],cfg_path])

saved_file = 'finished_results.json'
dataset_dir = '.'
metrics_dir = '.'
algs_dir = '.'
out_dir = 'out'

try:
    with open(saved_file) as fp:
        saved = json.load(fp)
except:
    saved = defaultdict(str)

datasets = loadFiles(dataset_dir,'dataset')
algorithms = loadFiles(algs_dir,'algorithm')
metrics = loadFiles(metrics_dir,'metric')

check_and_make_dir(out_dir)

results = {}
for dataset, algorithm in ((x, y) for x in datasets for y in algorithms):
    #print dataset, algorithm
    if algorithm['name'] not in results:
        results[algorithm['name']] =
    unique_name = '_'.join([dataset['name'],algorithm['name']])
    unique_out = os.path.join(out_dir,unique_name)
    unique_exists = os.path.exists(unique_out)
    check_and_make_dir(unique_out)

    hashkey = '_'.join([ hashlib.sha1(json.dumps(dataset)).hexdigest(), \
                        hashlib.sha1(json.dumps(algorithm)).hexdigest(), \
                        path_checksum([algorithm['command']] + algorithm['dependent_files']) ])
    if (not unique_exists) or (saved[unique_name] != hashkey):
        run_alg(dataset,algorithm,unique_out)
        saved[unique_name] = hashkey
        print unique_out,hashkey
    for metric in metrics:
        for name in dataset['names']:
            data = extract_fields(dataset,name,unique_out)
            metric.update(data)
            metric_cfg_path = os.path.join(out_dir,name + '_' +metric['name'] + '_cfg.json')
            metric_out_path = os.path.join(out_dir,name + '_' +metric['name'] + '_out.json')
            metric['output'] = metric_out_path

            #with open(metric_cfg_path,'w') as fp:
            #    json.dump(metric,fp)
            #print metric_cfg_path, name, unique_out
            call([metric['command'],metric_cfg_path])
            #with open(metric['output'],'r') as fp:
            #    res = json.load(fp)
            if name in results[unique_name]:
                results[unique_name][name].update(res)
            else:
                results[unique_name][name] = res
print results
with open(saved_file,'w') as fp:
    json.dump(saved,fp)
