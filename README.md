
# UnitTesting

## Synopsis
This program allows to quickly setup unit testing for small projects. 
It enables developpers to run tests on their code whenever they change it with a single command.
Setting up tests is easy, the program reads simple .json files that contain all the data required to run the tests

## Setting up
To set up the testing environment in one of your repository simply use the `--setup` option when running the command.

First you will need to edit the `unit_testing/compilation.json` file:

- `"make"` should be set to the command used to compile your programe

- `"clean"` should be set to the command used to clean your environment

- `"name"` should represent the name of the executable once it has been compiled

The second step is to set up the `unit_testing/validation.json`:

- `"mode"` can either be `"expected"`, `"compare"` or `"validate"`

  * `"expected` is the most basic mode and will simply compare stdout with the `"expected"` field of the test setting
    it will also compare the return code if the program with the `"code"` field of the test settings

  * `"compare"` will compare the return code and stdout to the ones of the command contained in the `"correct"` field
    (in the `validation.json` file)

  * `"validate"` will allow the use of a custom validation program, it will run the command contained in the `"validator"` field
    (in the `validation.json` file) as such: `command <command used to run program> <path to file containing program stdout> <program return code> `,
    it should return 0 if evrything was correct, 1 if the program stdout was incorrect or 2 if the program return code was incorrect

Last step is to setup tests:

- You should put all your test groups names in the `unit_testing/groups.json` file, they will be ran in the order you put them in

- For each testing group create a file named `unit_testing/group_<name>.json`:
  * They should have a list named `"tests"` containing all your tests
  * Each test should have an `"id"` field with their name and a `"cmd"` field with the command used to run the test
  (the `$` sign will be replaced with the name of your program binary)
  * If you use the `"expected"` mode to validate your tests, add an `"expected"` field and a `"code"` field as described above

**Congratulations! You have set up your testing environment!**
Note that if you are having troubles setting up your testing environment, there is an example available in the "example" folder of this repo

## Running a test

To run your tests, you simply have to call the script (by default `./unit_test_core.py`)

### Options

There are multiple optional arguments available:

- `-h` displays the help screen

- `-t` allows you to set the time before your program should be terminated 

- `-o` allows you to set the ouput trace file path

- `-s` makes the tests stop at the first KO or crash
