import configparser


def read_config():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    db_config = dict(config['db_config'].items())
    photoprism_config = dict(config['photoprism'].items())
    host = photoprism_config.pop('host')

    return dict(
        host=host,
        photoprism_config=photoprism_config,
        db_config=db_config
    )
