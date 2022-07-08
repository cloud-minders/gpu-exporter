from gpu_exporter.config.events_emitter import emitter, events
from gpu_exporter.config.logger import logger


@events.on(emitter=emitter, event="logger.debug")
def debug(msg):
    logger.debug(msg)


@events.on(emitter=emitter, event="logger.info")
def info(msg):
    logger.info(msg)


@events.on(emitter=emitter, event="logger.warn")
def warn(msg):
    logger.warn(msg)


@events.on(emitter=emitter, event="logger.error")
def error(msg):
    logger.error(msg)


@events.on(emitter=emitter, event="logger.critical")
def critical(msg):
    logger.critical(msg)
