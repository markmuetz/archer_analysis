import os
import datetime as dt
from glob import glob
from collections import OrderedDict
import abc

import iris

class Analyzer(object):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def get_files(data_dir, filename):
        return sorted(glob(os.path.join(data_dir, filename)))

    def __init__(self, user, suite, expt, data_type, data_dir, results_dir, filename):
        self.user = user
        self.suite = suite
        self.expt = expt
        self.data_type = data_type
	self.data_dir = data_dir
	self.results_dir = results_dir
        self.filename = os.path.join(self.data_dir, filename)

        self.name = '{}_{}_{}'.format(suite, expt, self.__class__.__name__)
        self.results = OrderedDict()
	self.force = False

    def set_config(self, config):
	self._config = config
	if 'force' in self._config:
	    self.force = self._config['force'] == 'True'

    def already_analyzed(self):
        return os.path.exists(self.filename + '.analyzed')

    def append_log(self, message):
        with open(self.filename + '.analyzed', 'a') as f:
            f.write('{}: {}\n'.format(dt.datetime.now(), message))

    def load(self):
        self.append_log('Loading')
        self.cubes = iris.load(self.filename)
        self.append_log('Loaded')

    def run(self):
        self.append_log('Analyzing')
	self.run_analysis()
        self.append_log('Analyzed')

    def save(self):
        self.append_log('Saving')
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

        cubelist_filename = os.path.join(self.results_dir, self.name + '.nc')
        cubelist = iris.cube.CubeList(self.results.values())

        iris.save(cubelist, cubelist_filename)

	self.save_analysis()
        self.append_log('Saved')

    def save_analysis(self):
	pass

    @abc.abstractmethod
    def run_analysis(self):
        return
