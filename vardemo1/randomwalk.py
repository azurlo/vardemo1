#!/usr/bin/env python
import argparse
import csv
import math
import pickle
from os import path, makedirs
from random import randint
from sys import exit, stdout, stderr
from time import sleep

import numpy
import pandas


TRADING_DAYS = 252  # Number of trading days on stock


class Connector(object):
    def __init__(self, company, start_date):
        self._initial_counter = 1
        self.increment = 2
        self.delay = 1
        self.max_counts = 60
        self.company = company
        self.start_date = start_date
        self.token = None
        self.link = 'WIKI/{0}'.format(self.company)
        self.verbose = True

    def get_data(self):
        import quandl
        if self.token:
            quandl.ApiConfig.api_key = self.token

        while self._initial_counter <= self.max_counts:
            if self.verbose:
                stderr.write("Delay set to {0} seconds\n".format(self.delay))
            sleep(self.delay)
            try:
                data = quandl.get(self.link, start_date=self.start_date)
                if self.verbose:
                    stderr.write("Data recieved from quandl after {0} tries\n".format(self._initial_counter))
                return data
            except Exception as e:
                if self.verbose:
                    stderr.write("{0}\n".formar(e))
                self.delay = self.delay * self.increment
        raise ("Failed to get data from quandl after {0} tries".format(self.max_counts))

    def get_local_data(self):
        pass


class DataModel(object):
    def __init__(self, company, start_date):
        self._connector = Connector(company, start_date)
        self.token = None
        if self.token:
            self._connector.token = self.token
        self.cache_dir = None
        self.cache_file = path.join(self.cache_dir, "{0}_{1}.p".format(company, start_date)) if self.cache_dir else None
        self.verbose = False

        self._raw_data = None
        self.data = None
        self.to_csv = False
        self.to_cache = False
        self.use_cache = False
        self.iter_count = 1000
        self._cache_file = None
        self.from_csv = None

    # def _save_to_csv(self, file_path):
    #     output_dir = path.dirname(file_path)
    #     if not path.exists(output_dir):
    #         makedirs(output_dir)
    #     with open(file_path, 'wb') as outfile:
    #         csv_writer = csv.writer(stdout)
    #         for row in self.data:
    #             csv_writer.writerow(row)

    def _save_to_csv(self, file_path):
        csv_writer = csv.writer(stdout)
        for row in self.data:
            csv_writer.writerow(row)

    def _save_to_cache(self, file_path):
        output_dir = path.dirname(file_path)
        if not path.exists(output_dir):
            makedirs(path.dirname(file_path))
        if self.verbose:
            stderr.write("Trying save {0} to cache\n".format(file_path))
        pickle.dump(self._raw_data, open(file_path, 'wb'))
        if self.verbose:
            stderr.write("Cache saved to {0}\n".format(file_path))

    def _from_csv(self, file_path):
        data = {}
        with open(file_path, 'rb') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                if line['ticker'] == self._connector.company:
                    data[pandas.Timestamp(line['date'])] = line
                    line['Close'] = numpy.float64(line['close'])
                    del line['ticker']
                    del line['date']
        self._raw_data = pandas.DataFrame.from_dict(data, orient='index')

    def _from_cache(self, file_path):
        try:
            data = pickle.load(open(file_path, 'rb'))
            if self.verbose:
                stderr.write("Loaded data from a local cache for object: {0}\n".format(file_path))
            self._raw_data = data
        except Exception as e:
            if self.verbose:
                stderr.write("Failed to load data from cache: {0}\n".format(e))

    def _get_data(self):
        marketd = self._raw_data
        # calculate the compound annual growth rate (CAGR) which will give us our mean return input (mu)
        days = (marketd.index[-1] - marketd.index[0]).days
        cagr = (marketd['Close'][-1] / marketd['Close'][1]) ** (365.0 / days) - 1
        # create a series of percentage returns and calculate the annual volatility of returnsgoogle_quandl
        marketd['Returns'] = marketd['Close'].pct_change()
        vol = marketd['Returns'].std() * numpy.sqrt(TRADING_DAYS)

        data = []
        starting_price = marketd['Close'][-1]  # starting company price (i.e. last available real company price)
        position = randint(10, 1000) * 10
        for i in xrange(self.iter_count):
            # create list of daily returns using random norgoogle_quandlmal distribution
            daily_returns = numpy.random.normal(cagr / TRADING_DAYS, vol / math.sqrt(TRADING_DAYS), TRADING_DAYS) + 1
            # set starting price and create price series generated by above random daily returns
            price_list = [self._connector.company, position, i, starting_price]
            for x in daily_returns:
                price_list.append(price_list[-1] * x)
            data.append(price_list)
        self.data = data

    def run(self):
        self._connector.verbose = self.verbose
        if self.use_cache:
            self._from_cache(self.use_cache)
        if self.from_csv:
            self._from_csv(self.from_csv)
        if self._raw_data is None:
            self._raw_data = self._connector.get_data()
        if self.to_cache:
            self._save_to_cache(self.to_cache)
            return 0
        self._get_data()
        if self.to_csv:
            self._save_to_csv(self.to_csv)


class DataPlot(object):
    def __init__(self, data):
        import matplotlib
        matplotlib.use('agg')
        from matplotlib import pyplot as plt
        self._plt = plt

        self.verbose = False
        self._figure, self._axis = self._plt.subplots()
        for row in data:
            self._axis.plot(row[4:])

    def save_plot(self, file_path):
        if self.verbose:
            stderr.write("Saving plot to {0}\n".format(file_path))
        self._figure.savefig(file_path)
        if self.verbose:
            stderr.write("Plot saved to {0}\n".format(file_path))


def _parse_args():
    parser = argparse.ArgumentParser('randomwalk', description='Monte-Carlo simulation of stock prices behaviour '
                                                               'based on data from www.quandl.com')
    parser.add_argument('-n', '--snum', type=int, default=1000, help='number of simulations (default:%(default)s)')
    parser.add_argument('-c', '--company', required=True, help='company symbol on stock (i. e. WDC)')
    parser.add_argument('-t', '--quandl-token', help='get token from www.quandl.com')
    parser.add_argument('-s', '--start-date', default='2018-01-01', help='example: %(default)s')
    parser.add_argument('-o', '--output-dir', default=path.join(path.dirname(path.abspath(__file__)), 'outputs'))
    parser.add_argument('--from-csv', help='path to wiki csv file')
    parser.add_argument('-p', '--plot', action='store_true', help='create plot and save it to .png')
    parser.add_argument('-m', '--make-cache', help='Make a cache file to specified directory')
    parser.add_argument('-u', '--use-cache', help='Use a cache file from specified directory')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()


def main():
    args = _parse_args()
    data_model = DataModel(args.company, args.start_date)
    if args.quandl_token:
        data_model.token = args.quandl_token
    if args.make_cache:
        data_model.to_cache = path.join(args.make_cache, '{0}_{1}.p'.format(args.company, args.start_date))
    if args.use_cache:
        data_model.use_cache = path.join(args.use_cache, '{0}_{1}.p'.format(args.company, args.start_date))
    if args.verbose:
        data_model.verbose = args.verbose
    if args.snum:
        data_model.iter_count = args.snum
    data_model.from_csv = args.from_csv

    data_model.to_csv = path.join(args.output_dir, '{0}_{1}.csv'.format(args.company, args.start_date))
    data_model.run()

    if args.plot:
        plot = DataPlot(data_model.data)
        if args.verbose:
            plot.verbose = args.verbose
        if args.plot:
            plot.save_plot(path.join(args.output_dir, '{0}_{1}.png'.format(args.company, args.start_date)))


if __name__ == '__main__':
    exit(main())
