# SPDX-License-Identifier: MIT
"""Development-only constrained runtime probe, using Python audit hooks and rlimits."""
import os
from pathlib import Path
import resource
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(os.environ.get('MAKEFUN_OUTPUT_DIR','/output')).resolve()
OUTPUT.mkdir(parents=True,exist_ok=True)
resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024))
resource.setrlimit(resource.RLIMIT_CPU,(60,60))
sys.dont_write_bytecode = True
sys.path.insert(0,str(ROOT))


def inside_output(path):
    return Path(path).resolve().is_relative_to(OUTPUT)


def audit(event,args):
    if event.startswith(('socket.','subprocess.')) or event in ('os.system','os.posix_spawn','os.fork'):
        raise PermissionError(f'Network/process action prohibited: {event}')
    if event == 'open':
        path,mode,flags = args
        writing = flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)
        if writing and not inside_output(path):
            raise PermissionError(f'Write outside output: {path}')
    if event == 'os.mkdir' and not inside_output(args[0]):
        raise PermissionError('Directory creation outside output')


sys.addaudithook(audit)
runpy.run_path(str(ROOT/'main.py'),run_name='__main__')
print('PASS: 512 MiB address-space cap, 60s CPU cap, network/process denial, output-only writes')
