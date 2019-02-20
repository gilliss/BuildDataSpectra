"""
"""
import os
import glob
import numpy as np

import Tools.FileIO as FileIO
import Tools.DataInfo as DataInfo

class Stitch:
    """
    """
    def __init__(self, st):
        self.data_set = st.data_set
        self.data_type = st.data_type
        self.file_index = st.file_index

        self.io = FileIO.FileIO(st)
        self.di = DataInfo.DataInfo(st)

    def Run(self):
        """
        Stitch together Gather jobs that were split up
        """
        data_set = self.data_set
        data_type = self.data_type
        io = self.io
        di = self.di
        cut_scheme_list = di.cut_scheme_list

        print('Stitch::Run()')

        # Read in channel data dict
        channel_data_dict = di.GetChannelData()

        # Set up dict of numpy arrays for each cut and for each channel
        data_dict = {} # dict to be filled and saved
        for cpd in channel_data_dict:
            data_dict[cpd] = {}
            for cut_scheme in cut_scheme_list:
                data_dict[cpd][cut_scheme] = np.array([])

        glob_path = io.GetGlobPathNPZ()
        path_list = glob.glob(glob_path)

        for path in path_list:
            d = np.load(path)['arrayDict'].item() # use numpy.ndarray.item() to copy the contents of dtype=object to a Python scalar
            for cpd in data_dict:
                for cut_scheme in cut_scheme_list:
                    data_dict[cpd][cut_scheme] =\
                        np.insert(data_dict[cpd][cut_scheme], len(data_dict[cpd][cut_scheme]), d[cpd][cut_scheme])

        # Save
        io.SaveNPZ(data_dict)

        # Delete split files
        for path in path_list:
            os.remove(path)
