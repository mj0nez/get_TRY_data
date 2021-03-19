import os
import pandas as pd

# IMPORT parameters
# PATH_SRC_FILES = os.getcwd()  # current working dir
PATH_SRC_FILES = 'D:/Master Thesis/Modellentwicklung/TRY_DWD/product_wgs84_20200626__125716_Kiel_Stadtrand/TRY_543103100873/'

# EXPORT parameters
# EXPORT_PREFIX = 'City_outskirts'
EXPORT_PREFIX = 'City_center'       # replaces coordinates

# PATH_FOR_EXPORT = FOLDER_PATH_SRC_FILES   # to src folder
PATH_FOR_EXPORT = 'D:/MATLAB_LoadFlow_Simulator/data_pv/'  # to Matlab folder

# VAL_TO_EXTRACT = 't'    # temperature
# VAL_TO_EXTRACT = 'N'    # okta / Bedeckungsgrad
# VAL_TO_EXTRACT = 'WG'   # wind speed
# VAL_TO_EXTRACT = 'p'    # atmospharic pressure
# VAL_TO_EXTRACT = 'B'    # dir. solar irradiance (horiz. plane) [W/m^2]
VAL_TO_EXTRACT = 'D'  # diff solar irradiance (horiz. plane) [W/m^2]


def readData(file_name, rows_to_skip):
    # column names of data set
    value_names = ['RW', 'HW', 'MM', 'DD', 'HH', 't',
                   'p', 'WR', 'WG', 'N', 'x', 'RF',
                   'B', 'D', 'A', 'E', 'IL']
    # use python engine, because c engine cant handle 2 sep
    return pd.read_csv(file_name,
                       skiprows=rows_to_skip,
                       engine='python',
                       sep='\\s\\*',
                       header=None,
                       names=value_names,
                       dtype=object)


def exportCSV(data_frame_to_export,
              export_path,
              export_file_name):
    # writes to new csv without index and header
    full_file_name = export_path + export_file_name + '.txt'
    # data_frame_to_export.to_csv(full_file_name,
    #                             header=None,
    #                             index=False)
    print('...exported.\n')


def runExtraction(path_src_folder,
                  path_for_export, file_prefix,
                  val_to_extract):
    # extraction only for source files
    for file in os.listdir(path_src_folder):
        file_ext_src = '.dat'

        if file.endswith(file_ext_src):
            print('Extracting data....for value: ', val_to_extract)
            print('from: ', file)

            TRY_future = 'TRY2045_'  # identifier future data set

            if TRY_future in file:
                skip_rows = 36  # header to skip
            else:
                skip_rows = 34  # for 2015 data

            df = readData(path_src_folder + str(file), skip_rows)
            df = df[val_to_extract]  # reduce data to column

            name_export_file = str(file).split('_')  # rename output file
            name_export_file = '_'.join([name_export_file[0],
                                         name_export_file[2]])  # no coordinates

            exportCSV(df, path_for_export, '_'.join([file_prefix,
                                                     name_export_file,
                                                     val_to_extract]))


if __name__ == '__main__':
    runExtraction(PATH_SRC_FILES,
                  PATH_FOR_EXPORT,
                  EXPORT_PREFIX,
                  VAL_TO_EXTRACT)
