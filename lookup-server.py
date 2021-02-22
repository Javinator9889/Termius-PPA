#                             termius-ppa
#                  Copyright (C) 2021 - Javinator9889
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#                   (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#               GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
import os
import sys
import urllib3
import logging

from pathlib import Path
from warnings import warn
from sched import scheduler
from time import time, sleep
from daemonize import Daemonize
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
from logging.handlers import RotatingFileHandler

delay_secs = 900
termius_url = "https://www.termius.com/download/linux/Termius.deb"
termius_beta_url = \
    "https://www.termius.com/beta/download/linux/Termius+Beta.deb?latest"
try:
    ppa_path = sys.argv[1]
except IndexError:
    warn("You must provide the PPA directory.\n"
         "Usage: python lookup-server.py PATH", category=RuntimeWarning)
    exit(1)
    
reprepro_cmd = f"reprepro -b {ppa_path} includedeb %dist% %file%"
http = urllib3.PoolManager()

home = str(Path.home())
pid = f"{home}/termius-ppa/termius-ppa.pid"
try:
    os.mkdir(f"{home}/termius-ppa")
except FileExistsError:
    pass

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fmt = logging.Formatter(
    "%(process)d - %(asctime)s | [%(levelname)s]: %(message)s"
)

file_handler = RotatingFileHandler(f"{home}/termius-ppa/termius-ppa.log", 'w',
                                   maxBytes=2 << 20,
                                   backupCount=2)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(fmt)

logger.addHandler(file_handler)
keep_fds = [file_handler.stream.fileno()]


def main():
    sched = scheduler(time, sleep)
    run_update_process()
    try:
        while True:
            sched.enter(delay_secs, 0, run_update_process)
            sched.run()
    except InterruptedError:
        exit(0)


def download_latest_deb(fp: NamedTemporaryFile, url: str):
    result = http.request("GET", url, redirect=True)
    if result.status == 200:
        logger.info("Downloaded correctly Termius .deb file")
        fp.write(result.data)
    else:
        logger.error("Termius .deb file could not be downloaded - status "
                     "code: {0}".format(result.status))


def update_reprepro(fp: NamedTemporaryFile, dist: str):
    cmd = reprepro_cmd.replace("%dist%", dist)\
                      .replace("%file%", fp.name)\
                      .split()
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        error = err.decode("utf-8")
        logger.error("reprepro ended with an error - ret. code: "
                     f"{proc.returncode}")
        logger.error(">>>>>>>>>>>>>>>>>>>>>>>>")
        for line in error.splitlines():
            if line.strip() and not line.strip().isspace():
                logger.error(f"> {line}")
    else:
        output = out.decode("utf-8") + "\n" + err.decode("utf-8")
        logger.info("reprepro finished OK")
        logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>")
        for line in output.splitlines():
            if line.strip() and not line.strip().isspace():
                logger.info(f"> {line}")


def run_update_process():
    stable = NamedTemporaryFile(suffix=".deb")
    beta = NamedTemporaryFile(suffix=".deb")
    try:
        download_latest_deb(stable, termius_url)
        update_reprepro(stable, "all")
        download_latest_deb(beta, termius_beta_url)
        update_reprepro(beta, "public-beta")
    finally:
        stable.close()
        beta.close()


daemon = Daemonize(app="termius-ppa",
                   pid=pid,
                   action=main,
                   keep_fds=keep_fds,
                   logger=logger)
daemon.start()
