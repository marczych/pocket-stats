#!/usr/bin/env python

from __future__ import print_function
from datetime import datetime
import argparse
import operator
import os
import sys

from pocket import Pocket
import matplotlib.pyplot
import matplotlib.dates

class PocketStats(object):
    def main(self):
        self.parse_arguments()

        if self.args.access_token:
            self.print_stats()
        else:
            self.get_access_token()

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--consumer-key", required=True)
        parser.add_argument("--access-token")
        self.args = parser.parse_args()

    def get_access_token(self):
        request_token = Pocket.get_request_token(consumer_key=self.args.consumer_key)
        auth_url = Pocket.get_auth_url(code=request_token)

        print(auth_url)
        input("Press enter after visiting the URL: ")

        user_credentials = Pocket.get_credentials(
                consumer_key=self.args.consumer_key, code=request_token)
        access_token = user_credentials['access_token']
        print("Access token: {}".format(access_token))

    def print_stats(self):
        stats = {
            'total': 0,
            'total_words': 0,
            'favorite': 0,
            'has_image': 0,
            'has_video': 0,
            'is_article': 0,
            'add_dates': [],
            'tags': {},
        }

        for item in self.get_all_items():
            from pprint import pprint
            stats['total'] += 1
            stats['total_words'] += int(item['word_count'])

            if item['favorite'] == '1':
                stats['favorite'] += 1

            if item['has_image'] == '1':
                stats['has_image'] += 1

            if item['has_video'] == '1':
                stats['has_video'] += 1

            if item['is_article'] == '1':
                stats['is_article'] += 1

            if 'tags' in item:
                for tag in item['tags']:
                    stats['tags'][tag] = stats['tags'].get(tag, 0) + 1

            stats['add_dates'].append(
                    datetime.fromtimestamp(int(item['time_added'])))

        print("Total: {}".format(stats['total']))
        print("Total words: {}".format(stats['total_words']))
        print("Average words: {}".format(stats['total_words']/stats['total']))
        print("Favorite: {}".format(stats['favorite']))
        print("Has image: {}".format(stats['has_image']))
        print("Has video: {}".format(stats['has_video']))
        print("Article: {}".format(stats['is_article']))
        print("Tags:")

        for (tag, count) in sorted(
                stats['tags'].items(), key=operator.itemgetter(1), reverse=True):
            print("\t{}: {}".format(tag, count))

        matplot_dates = matplotlib.dates.date2num(stats['add_dates'])
        _, ax = matplotlib.pyplot.subplots(1, 1)
        ax.hist(matplot_dates, bins=12)
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%y-%m-%d'))
        matplotlib.pyplot.xticks(rotation=90)
        matplotlib.pyplot.show()

        matplotlib.pyplot.bar(range(len(stats['tags'])), stats['tags'].values(), align='center')
        matplotlib.pyplot.xticks(range(len(stats['tags'])), stats['tags'].keys())
        matplotlib.pyplot.xticks(rotation=90)

        matplotlib.pyplot.show()


    def get_all_items(self):
        self.pocket = Pocket(self.args.consumer_key, self.args.access_token)

        response, headers = self.pocket.get(detailType='complete')

        # Surprisingly, this isn't paginated and returns at least 1,000 items.
        for key, item in response['list'].items():
            yield item


if __name__ == '__main__':
    PocketStats().main()
