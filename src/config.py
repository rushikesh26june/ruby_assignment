log_config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    },
    'disable_existing_loggers': False
}

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Abstinence@24",
    "database": "ruby_assignment"
}