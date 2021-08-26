import pysftp
import pandas as pd
import numpy as np
from pathlib import Path
import datetime
import time
from time import sleep
import os
import shutil 
import sys
from tqdm import tqdm
now = datetime.datetime.now()
timestamp = str(now.strftime("%Y%m%d_%H%M%S"))
import sys
import click



#Creating Employee Master Backup
if click.confirm('Do you want to continue?', default=True):
    print("Creating Employee Master Backup...") 
    for i in tqdm(range(10)):
        sleep(0.1)
    src = Path("../Resources/Source_data/master.csv")
    dst = Path("../Resources/Source_data/Archive/MASTER_BACKUP.csv")
    shutil.copy(src, dst)
    print("Employee Master Backup Complete")
    os.system("pause")