#!/usr/bin/python
from os import system as call
from subprocess import PIPE, Popen
import json

class   TestUnit:
    def __init__(self, name, args, expected, returncode):
        self.name = name
        self.args = args
        self.expected = expected
        self.returncode = returncode

    def run(self, out, cmd):
        log_msg = "Running test: %s" % self.name
        print(log_msg + " ...", end='')
        call('echo "Running test %s" >> %s' % (self.name, out))
        command = self.args.replace("$", cmd)
        call('echo "%s" >> %s' % (command, out))
        result = Popen(command, stdout=PIPE, stderr=PIPE,
                       universal_newlines=True, shell=True)
        res, err = result.communicate()
        code = result.returncode
        if code is not 0 and code is not 84:
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
