from restsql import rest_utils

root_file = "/home/lobis/gitlab/IAXOD0-REST/analysis_data/cosmic_neutrons/run_cosmic_neutrons_16-September-2019-17h29m47s/analysis_cosmic_neutrons_N100000000_0.root"

if __name__ == '__main__':
    class_map = rest_utils.get_class_map(root_file)

    print(class_map)

    for name, metadata in class_map.items():
        data = rest_utils.get_class_data(metadata)
        print(name, data)