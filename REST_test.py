""" Module for running speed tests on Kinvey's REST API
    KJR, GoodLux Tech. 7/2014 """
import requests
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

kinvey_okay = 201

class Test(object):
    def __init__(self, rest_headers, endpoints, datasets, endpoint_number=None, dataset_number=None):
        self.headers = rest_headers

        self.en = endpoint_number if endpoint_number is not None else random.randint(0,len(endpoints)-1)
        self.endpoint = endpoints[self.en]

        if dataset_number is None:
            self.dn = random.randint(0,len(datasets['fnames'])-1)
        elif type(dataset_number) == int:
            self.dn = dataset_number
        elif len(dataset_number) == 2:
            self.dn = random.randint(dataset_number)
        else:
            raise ValueError, "dataset_number is invalid."

        self.dataset     = datasets['fnames'][self.dn]
        self.num_records = datasets['lengths'][self.dn]

        with open(self.dataset, 'ra') as fobj:
            self.payload = fobj.read()

        self.timing      = dict()

    def run(self):
        self.tstart   = datetime.datetime.now()
        self.response = requests.post(self.endpoint, data=self.payload, headers=self.headers[self.en])
        self.trun     = datetime.datetime.now() - self.tstart
        self.trun_ms  = self.trun.seconds*1000 + self.trun.microseconds/1000.0
        response_code = kinvey_okay if self.en == 0 else 200 # default success code is 200
        self.did_pass = True if (self.response.status_code == response_code) else False
        if not self.did_pass: 
            print " #--> FAIL w/ endpoint:{0}, {1} records".format(self.endpoint.split(".com")[-1], self.num_records)
        else:
            self.timing   = self.response.json()['timing'] # individual timings from Kinvey


    def save(self, data):
        d = {   'tstart':      self.tstart,
                'status':      self.response.status_code,
                'timing':      self.timing,
                'trun':        self.trun,
                'trun_ms':     self.trun_ms,
                'did_pass':    self.did_pass,
                'endpoint':    self.endpoint,
                'dataset':     self.dataset,
                'num_records': self.num_records}
        data.append(d)

    def plot(self, fig, ax):
        marker = 'o'    if self.en == 0 else 's'
        mfc    = 'none' if self.en == 0 else colors[self.en]
        ax.plot(self.num_records, self.trun_ms, marker, mec=colors[self.en], mfc=mfc)
        ax.set_xlabel("Number of records")
        ax.set_ylabel("Time for POST operation (ms)")
        fig.canvas.draw()


if __name__ == '__main__':

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
    time_start_test = datetime.datetime.now()
    print "Starting test at: {0}".format(time_start_test)
    num_tests = 2
    fname     = "results_num-{1}.pkl".format("random",num_tests)
    data      = []
    plt.close(1)
    fig, ax = plt.subplots(1,1, num=1)
    fig.show()

    ax.set_title("elapsed17")

    elapsed17 = [] 

    for i in range(num_tests):
        print "test {0}".format(i)
        t = Test([rest_header]*len(endpoints), endpoints, datasets, endpoint_number=1)
        t.run()
        t.save(data)
        if t.did_pass: 
            if t.timing.has_key("elapsed17"):
                elapsed17.append(t.timing['elapsed17'])
                ax.plot(t.num_records, t.timing['elapsed17'], 'ok')

    time_end_test = datetime.datetime.now()
    print "ending test at: {0}".format(time_end_test)
    print "elapsed time: {0}".format(time_end_test - time_start_test)

    with open(fname, 'wb') as fobj:
        cPickle.dump(data, fobj)

    ax.set_xlabel("Number of records")
    ax.set_ylabel("Time (ms)")

    fig.suptitle("Number of tests: {0}".format(num_tests))
    fig.canvas.draw()
    fig.savefig( os.path.splitext(fname)[0] + ".png", dpi=300 )
