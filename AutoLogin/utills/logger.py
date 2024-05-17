from pathlib import Path
import logging
import sys
import os

#  Gets parent directory of working directory
log_file_path = f"{Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()}/logging/logs.txt"

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s: %(asctime)s :%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=log_file_path, encoding='utf-8', 
                    level=logging.DEBUG)

def logs(message:str):
    """
    Logs script messages to logs.txt
    message: What script event occured
    logtype: info, warning, debug
    """
    logging.debug(message)