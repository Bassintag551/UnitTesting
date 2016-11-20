#!/usr/bin/python
from os import system as call
from subprocess import PIPE, Popen
from time import sleep
from threading import Timer
import json

class   TestUnit:
    def __init__(self, name, args, expected, returncode):
        self.name = name
        self.args = args
        self.expected = expected
        self.returncode = returncode

    def run(self, out, cmd, timeout):
        log_msg = "Running test: %s" % self.name
        print(log_msg + " ...", end='', flush=True)
        call('echo "Running test %s" >> %s' % (self.name, out))
        command = self.args.replace("$", cmd)
        call('echo "%s" >> %s' % (command, out))
        result = Popen(command, stdout=PIPE, stderr=PIPE,
                       universal_newlines=True, shell=True)
        kill_prog = lambda prog: prog.kill()
        timer = Timer(timeout, kill_prog, [result])
        try:
            timer.start()
            res, err = result.communicate()
            code = result.returncode
        finally:
            timer.cancel()
        if code == -9:
            print("\r" + log_msg + " Timeout")
            call('echo "Exec error: program timed out (Max: %d sec)" >> %s' %
                 (timeout, out))
            return (3)
        if code < 0:
            print("\nCrashed")
            call('echo "Exec error: program crashed (Code: %d)" >> %s' %
                 (code, out))
            return (2)
        if not res == self.expected:
            print("\r" + log_msg + " KO ")
            call('echo "KO, expected: %s and got: %s" >> %s' %
                 (self.expected, res, out))
            return (1)
        if not code is self.returncode:
            print("\r" + log_msg + " KO ")
            call('echo "KO, got incorrect return code: %d (expected %d)" >> %s'
                 % (code, self.returncode, out))
            return (1)
        call('echo "OK" >> %s' % out)
        print("\r" + log_msg + " OK ")
        return (0)

def load_groups(path):
    f = open(path)
    data = json.load(f)
    f.close()
    groups = data["groups"]
    return (groups)

def load_group_tests(path):
    f = open(path)
    data = json.load(f)
    f.close()
    tests = data["tests"]
    result = [TestUnit(test["id"], test["cmd"], test["expected"], test["code"])
              for test in tests]
    return (result)
