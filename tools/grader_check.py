# SPDX-License-Identifier: MIT
"""Reproduce the grader's safe-path invocation from / against a read-only copy.

Run with Python 3.13: python3.13 -S tools/grader_check.py
Temporary files respect TMPDIR; only this probe's copy has permissions changed.
"""
import hashlib
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
    resource.setrlimit(resource.RLIMIT_CPU, (60, 60))


def fingerprint(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def main():
    with tempfile.TemporaryDirectory(prefix='atlas-1122-grader-') as tmp:
        copy = Path(tmp)/'bot'
        copy.mkdir()
        for name in ('main.py', 'raster.py', 'illustrations.py', 'assets'):
            source, target = ROOT/name, copy/name
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                shutil.copy2(source, target)
        before = fingerprint(copy)
        try:
            for path in copy.rglob('*'):
                path.chmod(0o555 if path.is_dir() else 0o444)
            copy.chmod(0o555)
            outputs = []
            for run in range(2):
                output = Path(tmp)/f'output-{run}'
                output.mkdir()
                command = ['/usr/bin/env', '-i', 'PATH=/usr/bin:/bin', 'TZ=UTC',
                           'PYTHONHASHSEED=0', 'LANG=C.UTF-8',
                           f'MAKEFUN_BOT_DIR={copy}', f'MAKEFUN_OUTPUT_DIR={output}',
                           '/usr/bin/timeout', '60', sys.executable,
                           '-P', '-s', str(copy/'main.py')]
                result = subprocess.run(command, cwd='/', text=True, capture_output=True,
                                        timeout=65, preexec_fn=limits)
                print(f'Run {run+1}: exit {result.returncode}; {result.stdout.strip()}')
                assert result.returncode == 0, result.stderr
                assert sorted(p.name for p in output.iterdir()) == ['entry.png']
                outputs.append((output/'entry.png').read_bytes())
            assert outputs[0] == outputs[1] == (ROOT/'entry.png').read_bytes()
            assert fingerprint(copy) == before
            assert not list(copy.rglob('__pycache__'))
            print(f'PASS: Python {sys.version.split()[0]}, cwd=/, -P -s, empty environment, read-only bot, 512 MiB, two identical PNGs')
            print(f'PNG: {len(outputs[0])} bytes; sha256={hashlib.sha256(outputs[0]).hexdigest()}')
        finally:
            copy.chmod(0o755)
            for path in copy.rglob('*'):
                path.chmod(0o755 if path.is_dir() else 0o644)


if __name__ == '__main__':
    main()
