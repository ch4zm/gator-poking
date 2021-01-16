import logging


# Set basic universal log options
# (level should be WARNING INFO DEBUG)
loglevel = logging.DEBUG
logging.basicConfig(format='', level=logging.WARNING)

root_logger = logging.getLogger()
root_logger.handlers = []

# Create gp logger and add handlers
### logger = logging.Logger('gp')
logger = logging.getLogger('gp')
logger.setLevel(loglevel)

fh = logging.FileHandler('output.log')
fh.setLevel(loglevel)
logger.addHandler(fh)

sh = logging.StreamHandler()
sh.setLevel(loglevel)
logger.addHandler(sh)
