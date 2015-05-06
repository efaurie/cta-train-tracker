import ConfigParser


class TrainTrackerConfigParser():

    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.read_config(config_path)

    @staticmethod
    def read_config(config_path):
        config = ConfigParser.ConfigParser()
        config.read(config_path)
        return config

    @property
    def api_key(self):
        return self.config.get('Tracker Settings', 'APIKey')

    @property
    def refresh_rate(self):
        return self.config.get('Tracker Settings', 'RefreshRate')

    @property
    def stations_to_track(self):
        return self.config.get('Tracker Settings', 'StationsToTrack').split(',')
