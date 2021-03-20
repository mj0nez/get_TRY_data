import pandas as pd
from pathlib import Path

# IMPORT parameters
# PATH_SRC_FILES = Path.cwd()  # current working dir
PATH_SRC_FILES = 'D:/Master Thesis/Modellentwicklung/TRY_DWD/' \
                 'product_wgs84_20200626__125716_Kiel_Stadtrand/' \
                 'TRY_543103100873/'  # '<path of unpacked data set>'

# EXPORT parameters
# EXPORT_PREFIX = 'City_outskirts'
EXPORT_PREFIX = 'City_center'  # replaces coordinates

PATH_FOR_EXPORT = PATH_SRC_FILES  # to src folder
# PATH_FOR_EXPORT = '<your desired export location>'

# VAL_TO_EXTRACT = 't'    # temperature
# VAL_TO_EXTRACT = 'N'    # okta / degree of coverage
# VAL_TO_EXTRACT = 'WG'   # wind speed
# VAL_TO_EXTRACT = 'p'    # atmospheric pressure
# VAL_TO_EXTRACT = 'B'    # dir. solar irradiance (horiz. plane) [W/m^2]
VAL_TO_EXTRACT = 'D'  # diff solar irradiance (horiz. plane) [W/m^2]

EXPORT_FORMAT = '.txt'


# EXPORT_FORMAT = '.csv'


def readData(file):
    # column names of data set
    value_names = ['RW', 'HW', 'MM', 'DD', 'HH', 't', 'p', 'WR', 'WG', 'N',
                   'x', 'RF', 'B', 'D', 'A', 'E', 'IL']

    TRY_future = 'TRY2045_'  # identifier future data set
    head_future = 36
    head_normal = 34

    # header to skip
    rows_to_skip = head_future if TRY_future in file.name else head_normal

    # use python engine, because c engine cant handle 2 sep
    return pd.read_csv(file,
                       skiprows=rows_to_skip,
                       engine='python',
                       sep=r'\s+',
                       header=None,
                       names=value_names,
                       dtype=object)


def getExportPath(export_path, file_prefix, file_name, val_name):
    name_sep = '_'

    name_string = file_name.split(name_sep)
    export_file_name = name_sep.join([file_prefix,
                                      name_string[0],
                                      name_string[2],
                                      val_name])  # w/o coordinates
    return Path(export_path) / Path(export_file_name)


def exportCSV(data_frame, export_name_path, export_format):
    name = export_name_path.with_suffix(export_format)
    data_frame.to_csv(name,
                      header=None,
                      index=False)
    return


def runExtraction():
    # local vars allow 
    path_src_folder = PATH_SRC_FILES
    file_ext_src = '.dat'
    path_for_export = PATH_FOR_EXPORT
    export_prefix = EXPORT_PREFIX
    val_to_extract = VAL_TO_EXTRACT
    export_format = EXPORT_FORMAT

    for file in list(Path(path_src_folder).glob('**/*' + file_ext_src)):
        # creates PurePath objects from matching files in src folder

        print('Extracting data....for value: ', val_to_extract)
        print('from: ', file.name)

        df = readData(file)
        df = df[val_to_extract]  # reduce data to column
        export_path = getExportPath(path_for_export,
                                    export_prefix,
                                    file,
                                    val_to_extract)
        exportCSV(df, export_path, export_format)

        print('...exported.\n')
    return


if __name__ == '__main__':
    runExtraction()
