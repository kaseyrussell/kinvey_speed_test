""" Testing Kinvey's REST API
    KJR, GoodLux Tech. 7/2014 """
import json
import glob
import random
import datetime
import numpy as np
import matplotlib.pyplot as plt
import sys
import cPickle
import os.path
import base64
import REST_test


dataset_filenames = glob.glob("datasets/*.json")
dataset_lengths   = [int(f.split("samples")[0].split("_")[-1]) for f in dataset_filenames]
datasets = dict( fnames=dataset_filenames, lengths=dataset_lengths )

with open("endpoints.json", 'ra') as fobj:
    d         = json.load(fobj)
    endpoints = d['endpoints']
    colors    = d['linecolors']

with open("account_sunspritedev.json", 'ra') as fobj:
    d        = json.load(fobj)
    username = d['username']
    password = d['password']
auth_token   = base64.b64encode(username+":"+password)
rest_header  = { "Authorization": "Basic " + auth_token,
                                "X-Kinvey-API-Version": "3",
                                "Content-Type": "application/json"
                            }

plt.close(1)
fig, axa = plt.subplots(3,3, num=1)
fig.subplots_adjust(hspace=0.7, wspace=0.7)
fig.show()

axa[0,0].set_title("elapsed17")
axa[0,1].set_title("elapsed25")
axa[0,2].set_title("elapsed28")
axa[1,0].set_title("elapsed29")
axa[1,1].set_title("elapsed30")
axa[1,2].set_title("elapsed31")
axa[2,0].set_title("elapsed32")
axa[2,1].set_title("elapsed37")
axa[2,2].set_title("end")

elapsed15 = [] 
elapsed16 = [] 
elapsed17 = [] 
elapsed25 = [] 
elapsed28 = [] 
elapsed29 = [] 
elapsed30 = [] 
elapsed31 = [] 
elapsed32 = [] 
elapsed37 = [] 
end       = [] 



time_start_test = datetime.datetime.now()
print "Starting test at: {0}".format(time_start_test)
num_tests = 50
fname     = "results_num-{1}.pkl".format("random",num_tests)
data      = []


for i in range(num_tests):
    print "test {0}".format(i)
    t = REST_test.Test([rest_header]*len(endpoints), endpoints, datasets, endpoint_number=1)
    t.run()
    t.save(data)
    if t.did_pass: 
        if t.timing.has_key("elapsed15"):
            elapsed15.append(t.timing['elapsed15'])

        if t.timing.has_key("elapsed16"):
            elapsed16.append(t.timing['elapsed16'])

        if t.timing.has_key("elapsed17"):
            elapsed17.append(t.timing['elapsed17'])
            axa[0,0].plot(t.num_records, t.timing['elapsed17'], 'ok')

        if t.timing.has_key("elapsed25"):
            elapsed25.append(t.timing['elapsed25'])
            axa[0,1].plot(t.num_records, t.timing['elapsed25'], 'ok')

        if t.timing.has_key("elapsed28"):
            elapsed28.append(t.timing['elapsed28'])
            axa[0,2].plot(t.num_records, t.timing['elapsed28'], 'ok')

        if t.timing.has_key("elapsed29"):
            elapsed29.append(t.timing['elapsed29'])
            axa[1,0].plot(t.num_records, t.timing['elapsed29'], 'ok')

        if t.timing.has_key("elapsed30"):
            elapsed30.append(t.timing['elapsed30'])
            axa[1,1].plot(t.num_records, t.timing['elapsed30'], 'ok')

        if t.timing.has_key("elapsed31"):
            elapsed31.append(t.timing['elapsed31'])
            axa[1,2].plot(t.num_records, t.timing['elapsed31'], 'ok')

        if t.timing.has_key("elapsed32"):
            elapsed32.append(t.timing['elapsed32'])
            axa[2,0].plot(t.num_records, t.timing['elapsed32'], 'ok')

        if t.timing.has_key("elapsed37"):
            elapsed37.append(t.timing['elapsed37'])
            axa[2,1].plot(t.num_records, t.timing['elapsed37'], 'ok')

        if t.timing.has_key("end"):
            end.append(t.timing['end'])
            axa[2,2].plot(t.num_records, t.timing['end'], 'ok')

time_end_test = datetime.datetime.now()
print "ending test at: {0}".format(time_end_test)
print "elapsed time: {0}".format(time_end_test - time_start_test)

with open(fname, 'wb') as fobj:
    cPickle.dump(data, fobj)

for ax in axa.flatten():
    ax.set_xlabel("Number of records")
    ax.set_ylabel("Time (ms)")
    while len(ax.get_xticks()) > 4:
        ax.set_xticks(ax.get_xticks()[::2])
    while len(ax.get_yticks()) > 5:
        ax.set_yticks(ax.get_yticks()[::2])

fig.suptitle("Number of tests: {0}".format(num_tests))
fig.canvas.draw()
fig.savefig( os.path.splitext(fname)[0] + ".png", dpi=300 )
