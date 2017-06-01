# -*- coding: utf-8

import subprocess

from liridev.utils import console


class _ExecGenerator:
    def __init__(self, command: str, *args, path: str = None, formatting: bool = True):
        self._exit_code = -1
        self._output = ''
        self._command = command
        self._args = list(args)
        self._path = path
        self._formatting = formatting

    def __iter__(self):
        cmd = []
        bash_command = self._command + ' ' + ' '.join(self._args)
        if self._path:
            bash_command = 'cd {} && {}'.format(self._path, bash_command)
        cmd += ['bash', '-c', bash_command]
        p = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        for line in p.stdout:
            self._output += line.decode()
            yield line.decode()
        for line in p.stderr:
            self._output += line.decode()
            if self._formatting:
                line = console.Formatting.Red + line.decode() + console.Formatting.End
            else:
                line = line.decode()
            yield line
        exit_code = p.wait()
        self._exit_code = exit_code
        if exit_code:
            raise subprocess.CalledProcessError(exit_code, cmd)

    @property
    def output(self) -> str:
        return self._output


def run(command, *args, path: str = None, silent: bool = False):
    gen = _ExecGenerator(command, *args, path=path)
    try:
        for line in gen:
            if not silent:
                print(line, end='')
    except subprocess.CalledProcessError as e:
        if silent:
            print(gen.output)
        raise e
    return gen.output


def find_program(program: str):
    import os

    def is_executable(filepath: str):
        return os.path.isfile(filepath) and os.access(filepath, os.X_OK)

    filepath, filename = os.path.split(program)
    if filepath:
        return is_executable(program)
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_executable(exe_file):
                return True
    return False
