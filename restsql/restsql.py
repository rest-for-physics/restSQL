import os

import ROOT


def is_installed_REST():
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
    if not is_installed_REST():
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

        print("REST library ({}) loaded successfuly with status: {}.".format(lib, load_status))


def get_list_of_keys_from_file(root_file):
    """
    Return all keys (class names) from a ROOT file as a list
    """

    f = ROOT.TFile(root_file, "READ")

    result = []
    for key in f.GetListOfKeys():
        result.append(key.GetClassName())

    f.Close()

    return result


def main():
    load_rest_libs()


if __name__ == '__main__':
    main()
