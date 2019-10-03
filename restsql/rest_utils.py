import os
import io

import ROOT

from restsql.stdout_redirector import stdout_redirector


def is_installed_rest():
    """
    Method to check if REST is installed using environment variables
    Returns True if it detects REST and False otherwise
    """

    # this is the environment variable that points to the REST installation
    rest_environment_variable = "REST_PATH"
    # we check if the environment variable exists
    if not rest_environment_variable in os.environ:
        return False
    # we verify the environment variable points to a directory in our system
    if not os.path.isdir(os.environ[rest_environment_variable]):
        return False
    # we passed all checks
    return True


def load_rest_libs(rest_libs_to_load=None):
    """
    Method to load the REST libraries using the pyROOT library
    It can be used to load any library under the 'lib' directory in the REST path
    If no argument is specified it loads the default libraries specified here
    """

    # the default REST libraries to load
    default_rest_libs = ["libRestCore", "libRestEvents", "libRestMetadata", "libRestProcesses", "libRestTools"]
    if not rest_libs_to_load:
        rest_libs_to_load = default_rest_libs

    # check if REST is installed using environment variables
    if not is_installed_rest():
        raise Exception("REST is not installed!")

    # check the libraries path points to a directory in our system
    rest_lib_path = os.path.join(os.environ["REST_PATH"], "lib")
    assert os.path.isdir(rest_lib_path), "REST libraries path ({}) does not exist".format(
        os.path.abspath(rest_lib_path))

    for lib_name in rest_libs_to_load:
        # add .so extension if its not on lib_name
        if not lib_name.split(".")[-1] == "so":
            lib_name += ".so"

        lib = os.path.join(rest_lib_path, lib_name)
        # lib points to the location of the library but it may not correspond exactly to the file if it doesn't include a file extension
        try:
            load_status = ROOT.gSystem.Load(lib)
            # Load method should return 1 if OK or -1 if it failed
            assert load_status in [0, 1], "Failed to load REST library ({}) using ROOT.gSystem.Load".format(lib)
        except Exception as e:
            # something went very wrong
            raise Exception("Something went wrong when loading REST library ({}). Exception: {}".format(lib, e))

        print("REST library ({}) loaded successfully with status: {}.".format(lib, load_status))


def get_class_map(root_file):
    """
    Return dictionary with metadata name : object
    """
    class_map = {}

    f = ROOT.TFile(root_file, "READ")
    for key in f.GetListOfKeys():
        name = key.GetName()
        metadata = f.Get(name)
        if not metadata.InheritsFrom("TRestMetadata"):
            continue
        class_map[name] = metadata

    f.Close()

    return class_map


def get_class_data(metadata, only_starts_with_f=True, ignore_pointers=True):
    f = io.BytesIO()

    with stdout_redirector(f):
        metadata.Dump()

    dump = f.getvalue().decode('utf-8')
    data = {}
    # first we need to locate the starting position of the second column i.e. "value"
    first_column_length_limit = len(dump)
    for line in dump.split("\n")[1:]:
        split = line.split()
        if len(split) > 1:
            pos = line.find(" " + split[1]) + 1
            first_column_length_limit = min(first_column_length_limit, pos)
    # warning: there can be spaces in the "value" column, that is why need third column start
    second_column_length_limit = len(dump)
    tmp = []
    for line in dump.split("\n")[1:]:
        line = line[first_column_length_limit:]
        split = line.split()
        if len(split) > 1:
            pos = line.find(split[1]) + first_column_length_limit
            tmp.append(pos)
    second_column_length_limit = max(set(tmp), key=tmp.count)
    # we always skip the first line
    for line in dump.split("\n")[1:]:
        if line == "":
            continue
        split = line.split()
        if only_starts_with_f:
            # we only want attributes that start with "f" e.g. "fName"
            if split[0][0] != "f":
                continue
        if len(split[0]) > first_column_length_limit:
            # this means length of name is on the limit so there is no space, we add one
            split = line.replace(line[0:first_column_length_limit], line[0:first_column_length_limit] + " ", 1).split()
        if line[first_column_length_limit] == " ":
            if len(split) == 1:
                split.append("")
            else:
                split[1] = ""
        if split[1] != "":
            split[1] = line[first_column_length_limit:second_column_length_limit]
        if ignore_pointers:
            if split[1][0:2] == "->":
                continue
        data[split[0]] = split[1].rstrip()

    return data


load_rest_libs()
