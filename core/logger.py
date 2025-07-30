from logging import INFO, basicConfig, StreamHandler, FileHandler, getLogger

__all__ = ['logger']

logger = basicConfig(
    level=INFO,
    format='%(asctime)s - [%(levelname)s] - [%(name)s]: %(message)s',
    datefmt='%m-%d-%Y %H:%M:%S',
    handlers=[FileHandler(filename='logs/selfbot.log', encoding='utf-8'), StreamHandler()]
)

logger = getLogger('SELFBOT')