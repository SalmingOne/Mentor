from pathlib import Path


class Config:
    _isinstance = None
    _dict = {}

    def __new__(cls, *args, **kwargs):
        if cls._isinstance is None:
            cls._isinstance = super().__new__(cls)

        config_path = Path(__file__).parents[4] / 'resources' / 'urls.properties'

        if config_path.exists():
            with open(config_path) as f:
                for line in f.readlines():
                    key, value = line.split('=')
                    cls._dict[key.strip()] = value.strip()

        return cls._isinstance

    @staticmethod
    def fetch(key):
        return Config()._dict.get(key)



