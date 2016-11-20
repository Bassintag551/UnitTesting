#!/usr/bin/python
from os import system as call
from os.path import isfile
import json

class   CompilationSettings():
    def __init__(self, cmd, bin_name, clean_cmd = None):
        self.cmd = cmd
        self.bin_name = bin_name
        self.clean_cmd = clean_cmd

    def clean(self, out):
        call('echo "Cleaning..." >> %s' % out)
        call('%s &>> %s' % (self.clean_cmd, out))
        call('echo Done >> %s' % out)

    def compile(self, out):
        call('echo "Compiling..." >> %s' % out)
        call('%s &>> %s' % (self.cmd, out))
        call('echo Done >> %s' % out)

    def check_compile(self, out):
        call('echo "\nChecking if compilation was successful" >> %s' % out)
        res = isfile(self.bin_name)
        if res:
            call('echo "It was" >> %s' % out)
        return (res)


def load_compilation_settings(path):
    f = open(path)
    data = json.load(f)
    f.close()
    cmd = data["make"]
    name = data["name"]
    clean_cmd = data["clean"]
    return (CompilationSettings(cmd, name, clean_cmd))
