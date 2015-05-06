import time
import argparse
import datetime

from CTAInterface import CTAInterface
from StationDataAccessor import StationDataAccessor
from TrainTrackerConfigParser import TrainTrackerConfigParser


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-config', help='The path to the config file.')
    return parser.parse_args()


def print_schedule(schedule):
    current_time = datetime.datetime.now()
    for station, station_value in schedule.iteritems():
        print '\nStation: {0}'.format(station)
        for line, line_value in station_value.iteritems():
            print '\tLine: {0}'.format(line)
            for direction, arrival_times in line_value.iteritems():
                print '\t\tDirection: {0}'.format(direction)
                for arrival_time in arrival_times:
                    parsed_time = time.strptime(arrival_time, '%Y%m%d %H:%M:%S')
                    time_difference = datetime.datetime(*parsed_time[:6]) - current_time
                    wait = divmod(time_difference.days * 86400 + time_difference.seconds, 60)
                    print '\t\t\tETA: {0} min {1} sec'.format(wait[0], wait[1])


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


def run(config, data_accessor, cta_interface):
    while True:
        results = cta_interface.ping_many(config.stations_to_track)
        aggregate = aggregate_results(results)
        print_schedule(aggregate)
        time.sleep(float(config.refresh_rate))


if __name__ == '__main__':
    args = init_parser()
    config = TrainTrackerConfigParser(args.config)

    cta_interface = CTAInterface(config.api_key)
    data_accessor = StationDataAccessor()

    run(config, data_accessor, cta_interface)
