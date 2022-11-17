import logging

# logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
logger.setLevel(logging.INFO)
log_format = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
log_handler.setFormatter(log_format)
logger.addHandler(log_handler)
