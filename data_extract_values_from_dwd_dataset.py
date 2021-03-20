import pandas as pd
from pathlib import Path

"""
IMPORT parameters
"""
# PATH_SRC_FILES = Path.cwd()  # current working dir
PATH_SRC_FILES = 'C:\..<path to your directory>'  # of unpacked data set'

"""
EXPORT parameters
"""
# EXPORT_PREFIX = 'City_outskirts'
EXPORT_PREFIX = 'City_center'  # replaces coordinates with distinguishable name

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


def getColumnVectorFromFile(file: Path, val_to_extract: str) -> pd.DataFrame:

    # column names of data set
    columns_src = ['RW', 'HW', 'MM', 'DD', 'HH', 't', 'p', 'WR', 'WG', 'N',
                   'x', 'RF', 'B', 'D', 'A', 'E', 'IL']

    TRY_future = 'TRY2045_'  # identifier future data set
    head_future = 36
    head_normal = 34

    rows_to_skip = head_future if TRY_future in file.name else head_normal

    # use python engine, because c engine cant handle 2 sep
    df = pd.read_csv(file,
                     skiprows=rows_to_skip,
                     engine='python',
                     sep=r'\s+',
                     header=None,
                     names=columns_src,
                     dtype=object)

    return df[val_to_extract]


def getExportPath(export_path: str, file_prefix: str, file_name: str,
                  val_name: str) -> Path:

    name_sep = '_'

    name_string = file_name.split(name_sep)
    export_file_name = name_sep.join([file_prefix,
                                      name_string[0],
                                      name_string[2],
                                      val_name])        # w/o coordinates
    return Path(export_path) / Path(export_file_name)


def exportAsCSV(data_frame: pd.DataFrame, name_path: Path, export_format: str):

    name = name_path.with_suffix(export_format)
    data_frame.to_csv(name,
                      header=None,
                      index=False)


def runExtraction():
    file_ext_src = '.dat'

    matching_files_dir = list(Path(PATH_SRC_FILES).glob('**/*' + file_ext_src))
    if matching_files_dir is None:
        print("No matching files in directory...")
        return

    for file in matching_files_dir:
        # creates PurePath objects from matching files in src folder

        print('Extracting data....for value: ', VAL_TO_EXTRACT)
        print('from: ', file.name)

        values = getColumnVectorFromFile(file, VAL_TO_EXTRACT)

        export_path = getExportPath(PATH_FOR_EXPORT,
                                    EXPORT_PREFIX,
                                    file,
                                    VAL_TO_EXTRACT)

        exportAsCSV(values, export_path, EXPORT_FORMAT)

        print('...exported.\n')


if __name__ == '__main__':
    runExtraction()
