#!/usr/bin/python3

import argparse
from unit_test_compilation import *
from unit_test_groups import *
from os import system as call
from os.path import isfile, dirname, realpath
from shutil import copytree
import json

COMPILATION_CFG = "unit_testing/compilation.json"
GROUPS_CFG = "unit_testing/groups.json"
VALIDATION_CFG = "unit_testing/validation.json"
GROUPS_PATH = "unit_testing/group_%s.json"

should_stop = False
timeout = 120
command = ""

def check_setup():
    if not isfile(GROUPS_CFG) or not isfile(COMPILATION_CFG) or not isfile(VALIDATION_CFG):
        print("Testing environment isn't setup, use --setup to do a quick setup or --help for help")
        return (False)
    return (True)

def unsigned_int(value):
    int_value = int(value)
    if int_value < 0:
        raise argparse.ArgumentTypeError("invalid unsigned int value: '%s'" % value)
    return (int_value)

def run_group_tests(out):
    f = open(VALIDATION_CFG)
    validation = json.load(f)
    f.close()
    groups = load_groups(GROUPS_CFG)
    results = []
    i = 0
    failed = False
    print("Running test groups in order: %s" % (', '.join(groups)))
    for group_id in groups:
        results.append([0.0, 0])
        if failed:
            break
        if not isfile(GROUPS_PATH % group_id):
            print("\nWarning: %s does not exist\nSkipping it\n"
                  % (GROUPS_PATH % group_id))
            continue
        print("\n\nRunning test group: %s\n" % group_id)
        call('echo "\n\nRunning test group: %s\n" >> %s' % (group_id, out))
        tests = load_group_tests(GROUPS_PATH % group_id, validation)
        for test in tests:
            code = test.run(out, "./" + command, timeout)
            if should_stop and code is not 0:
                failed = True
                break
            if code is 0:
                results[i][0] += 1.0 / len(tests)
            if code is 2:
                results[i][1] += 1
        i += 1
    if not failed:
        print("\n\n")
        total = 0.0
        crashes = 0
        for i in range(0, len(groups)):
            group = groups[i]
            res = results[i]
            total += res[0]
            crashes += res[1]
            print("Result for group %s: %.f%% (%d crash)"
                  % (group, res[0] * 100, res[1]))
        total /= len(groups)
        print("\nTotal: %.f%% (%d crash)\n" % (total * 100, crashes))

def compile(compiler, out):
    global command
    compiler.compile(out)
    command = compiler.bin_name
    if not compiler.check_compile(out):
        return (False)
    return (True)

def setup():
    directory = dirname(realpath(__file__)) + "/unit_testing"
    copytree(directory, "unit_testing")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--timeout", dest="timeout", type=unsigned_int,
                        help="Sets the timeout value (default=120)")
    parser.add_argument("-o", "--output", dest="trace", type=str,
                        help="Sets the output file (default='trace')")
    parser.add_argument("-s", "--stop", dest="should_stop", action="store_true",
                        help="Makes the tester stop at the first error")
    parser.add_argument("--setup", dest="setup", action="store_true",
                        help="Sets up the testing environment")
    args = parser.parse_args()
    if args.setup:
        setup()
        return
    if not check_setup():
        return
    if args.trace is not None:
        out = args.trace
    else:
        out = "trace"
    global should_stop, timeout
    should_stop = args.should_stop
    if timeout is not None:
        timeout = args.timeout
    call("echo -n > %s" % out)
    print("Compiling program")
    compiler = load_compilation_settings(COMPILATION_CFG)
    if not compile(compiler, out):
        print("Compilation failed")
        return
    print("Compilation successful\n\n")
    run_group_tests(out)
    call('echo "\n" >> %s' % (out))
    compiler.clean(out)

main()
