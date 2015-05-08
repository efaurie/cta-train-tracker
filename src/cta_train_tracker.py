import time
import argparse
import datetime

from CTAInterface import CTAInterface
from TrainTrackerConfigParser import TrainTrackerConfigParser


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-config', help='The path to the config file.')
    return parser.parse_args()


def print_schedule(schedule):
    for station, station_value in schedule.iteritems():
        print '\nStation: {0}'.format(station)
        for line, line_value in station_value.iteritems():
            print '\tLine: {0}'.format(line)
            for direction, arrival_times in line_value.iteritems():
                print '\t\tDirection: {0}'.format(direction)
                for arrival_time in arrival_times:
                    wait_time = calculate_wait_time(arrival_time)
                    print '\t\t\tETA: {0} min {1} sec'.format(wait_time[0], wait_time[1])


def aggregate_results(results):
    aggregate = dict()

    for result in results:
        if result[0] not in aggregate:
            aggregate[result[0]] = dict()
        if result[1] not in aggregate[result[0]]:
            aggregate[result[0]][result[1]] = dict()
        if result[2] not in aggregate[result[0]][result[1]]:
            aggregate[result[0]][result[1]][result[2]] = list()
        aggregate[result[0]][result[1]][result[2]].append(result[3])

    return aggregate


def calculate_wait_time(next_arrival_time):
    current_time = datetime.datetime.now()
    time_format_arrival = time.strptime(next_arrival_time, '%Y%m%d %H:%M:%S')
    time_difference = datetime.datetime(*time_format_arrival[:6]) - current_time
    wait_time = divmod(time_difference.days * 86400 + time_difference.seconds, 60)
    return wait_time


def run(config, cta_interface):
    while True:
        results = cta_interface.get_next_arrivals(config.stations_to_track)
        aggregate = aggregate_results(results)
        print_schedule(aggregate)
        time.sleep(float(config.refresh_rate))


if __name__ == '__main__':
    args = init_parser()
    config = TrainTrackerConfigParser(args.config)

    cta_interface = CTAInterface(config.api_key)

    run(config, cta_interface)
