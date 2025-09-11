# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 17:37:29 2025

@author: amine
"""

import logging
from pathlib import Path
import sys

LOGFILE = Path(__file__).resolve().parent.parents[1] / Path(*["output"])
LOGFILE.mkdir(parents=True, exist_ok=True)
LOGFILE /= Path(*["output.log"])

# Configure logging to both file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGFILE, mode="w", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),  # console
    ]
)

def disp(text):
    logging.info(text)
