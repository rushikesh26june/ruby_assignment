import logging

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Abstinence@24",
    "database": "ruby_assignment"
}

filepath = '../dump.sql'

create_query = "CREATE TABLE `master_group` (`id_master` varchar(45) COLLATE utf8_bin NOT NULL, `name` varchar(45) COLLATE utf8_bin NOT NULL," \
               " `sell_uom` varchar(45) COLLATE utf8_bin DEFAULT NULL, `sell_uom_type` varchar(45) COLLATE utf8_bin DEFAULT NULL, " \
               "`sell_uom_avg_wt_per_uom` double DEFAULT NULL, " \
               "`packaging_cost` double DEFAULT NULL, " \
               "`loading_percent` double DEFAULT NULL, " \
               "`id_parent` varchar(45) COLLATE utf8_bin DEFAULT NULL, " \
               "PRIMARY KEY (`id_master`), UNIQUE KEY `id_master_UNIQUE` (`id_master`)," \
               " UNIQUE KEY `name_UNIQUE` (`name`) )" \
               "ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;"

def get_logger(filename):
    """Return a logger instance that writes in filename
    Args:
        filename: (string) path to log.txt
    Returns:
        logger: (instance of logger)
    """
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(
            '%(asctime)s:%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)

    return logger
