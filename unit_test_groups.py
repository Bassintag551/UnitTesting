#!/usr/bin/python3

from os import system as call
from subprocess import PIPE, Popen
from time import sleep
from threading import Timer
import json

PATH_TMP_OUT = "unit_testing/res.tmp"

class   TestUnit:
    def run_prog(self, out, cmd, timeout):
        log_msg = "Running test: %s" % self.name
        print(log_msg + " ...", end='', flush=True)
        call('echo "Running test %s" >> %s' % (self.name, out))
        command = self.args.replace("$", cmd)
        call('echo "%s" >> %s' % (command, out))
        result = Popen(command, stdout=PIPE, stderr=PIPE,
                       universal_newlines=True, shell=True)
        kill_prog = lambda prog: prog.kill()
        if timeout is not 0:
            timer = Timer(timeout, kill_prog, [result])
        try:
            if timeout is not 0:
                timer.start()
            res, err = result.communicate()
            code = result.returncode
        finally:
            if timeout is not 0:
                timer.cancel()
        if code == -9:
            print("\r" + log_msg + " Timeout")
            call('echo "Exec error: program timed out (Max: %d sec)" >> %s' %
                 (timeout, out))
            return (None, None, 3)
        if code < 0:
            print("\nCrashed")
            call('echo "Exec error: program crashed (Code: %d)" >> %s' %
                 (code, out))
            return (None, None, 2)
        return (res, code, 0)


    def validate_expected(self, out, cmd, timeout):
        res, code, status = self.run_prog(out, cmd, timeout)
        log_msg = "Running test: %s" % self.name
        if status is not 0:
            return (status)
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

    def run_validator(self, out, cmd, timeout):
        res, code, status = self.run_prog(out, cmd, timeout)
        log_msg = "Running test: %s" % self.name
        if status != 0:
            return (status)
        print("\r" + log_msg + " Validating...", end='')
        f = open(PATH_TMP_OUT, "w")
        f.write(res)
        f.close()
        check = Popen(self.corrector + " '%s' '%s' '%i'" % (self.args, PATH_TMP_OUT, code),
                      shell=True, stdout=PIPE, stderr=PIPE)
        res, err = check.communicate()
        check_code = check.returncode
        if len(res) > 0:
            call('echo "BEGIN STDOUT TRACE:" >> %s' % (out))
            call('echo "%s" >> %s' % (res, out))
            call('echo "END STDOUT TRACE" >> %s' % (out))
        if len(err) > 0:
            call('echo "BEGIN STDERR TRACE:" >> %s' % (out))
            call('echo "%s" >> %s' % (err, out))
            call('echo "END STDERR TRACE" >> %s' % (out))
        if check_code is 1:
            print("\r" + log_msg + " KO            ")
            call('echo "KO, validator returned error: wrong output" >> %s' %
                 (out))
            return (1)
        if check_code is 2:
            print("\r" + log_msg + " KO            ")
            call('echo "KO, validator returned error: wrong return code" >> %s'
                 % (out))
            return (1)
        call('echo "OK" >> %s' % out)
        print("\r" + log_msg + " OK                ")
        return (0)

    def run_compare_to(self, out, cmd, timeout):
        res, code, status = self.run_prog(out, cmd, timeout)
        log_msg = "Running test: %s" % self.name
        if status != 0:
            return (status)
        command = self.args.replace("$", self.corrector)
        call('echo "%s" >> %s' % (command, out))
        result = Popen(command, stdout=PIPE, stderr=PIPE,
                       universal_newlines=True, shell=True)
        correct_res, correct_err = result.communicate()
        correct_code = result.returncode
        if not res == correct_res:
            print("\r" + log_msg + " KO ")
            call('echo "KO, expected: %s and got: %s" >> %s' %
                 (correct_res, res, out))
            return (1)
        if not code  == correct_code:
            print("\r" + log_msg + " KO ")
            call('echo "KO, got incorrect return code: %d (expected %d)" >> %s'
                 % (code, correct_code, out))
            return (1)
        call('echo "OK" >> %s' % out)
        print("\r" + log_msg + " OK ")
        return (0)


    def __init__(self, name, args, expected, returncode):
        self.name = name
        self.args = args
        self.expected = expected
        self.returncode = returncode
        self.run = self.run_expected

    def __init__(self, name, args, corrector):
        self.name = name
        self.args = args
        self.corrector = corrector[0]
        if corrector[1]:
            self.run = self.run_validator
        else:
            self.run = self.run_compare_to

def load_groups(path):
    f = open(path)
    data = json.load(f)
    f.close()
    groups = data["groups"]
    return (groups)

def load_group_tests(path, validation):
    f = open(path)
    data = json.load(f)
    f.close()
    tests = data["tests"]
    if validation["mode"] == "expected":
        result = [TestUnit(test["id"], test["cmd"], test["expected"], test["code"])
                  for test in tests]
    elif validation["mode"] == "validate":
        result = [TestUnit(test["id"], test["cmd"], [validation["validator"], True])
                  for test in tests]
    elif validation["mode"] == "compare":
        result = [TestUnit(test["id"], test["cmd"], [validation["correct"], False])
                  for test in tests]
    else:
        result = []
    return (result)
