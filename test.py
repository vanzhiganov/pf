
import os
import time
import glob
import thread
import subprocess
import logging
from pidfile import PidFile
from settings import settings

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("start")

    PidFile(settings)

    while True:
        thread.start_new_thread(checkpf, (True, True))
        time.sleep(1)


def checkpf(*var):
    if settings['debug']:
        logging.debug("get list .rule files")

    for rule in glob.glob("*.rule"):
        # check exists pid file
        if not os.path.isfile("%s.pid" % rule.split(".")[0]):
            logging.info("run %s" % rule.split(".")[0])

            response = subprocess.Popen(["python", "pf.py", rule.split(".")[0]], stdout=subprocess.PIPE).stdout.read()
            if settings['debug']:
                logging.debug(response)


def pidwrite(pidfile):
    pfile = open(pidfile, "w+")

    pfile.write("%s" % str(os.getpid()))
    pfile.close()


def pid_files_remove():
    for pid_file in glob.glob("*.pid"):
        response = subprocess.Popen(["rm", pid_file], stdout=subprocess.PIPE).stdout.read()
        logging.debug(response)


if __name__ == '__main__':
    main()
