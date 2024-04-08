import time
import logging
import subprocess
import sys


class NonZeroReturnException(Exception): pass


def run_check(cmd: str):
    logging.info('Running cmd `%s`' % cmd)
    t0 = time.time() 
    
    completed_proc = subprocess.run(cmd.split(), stdout=sys.stdout, stderr=sys.stderr)

    logging.info('Took %.2fmin' % ((time.time() - t0)/60))

    if completed_proc.returncode != 0:
        raise NonZeroReturnException(
            "Command `%s` exited with non-zero return code `%d`. "
            "Check logs for more details" %
            (cmd, completed_proc.returncode)
        )
