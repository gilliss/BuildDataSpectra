"""
"""
import os
import glob
import numpy as np
import h5py

import Tools.FileIO as FileIO
import Tools.DataInfo as DataInfo

class Stitch:
    """
    Stitch together Gather jobs that were split up
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

        # Read in channel data dict
        channel_data_dict = di.GetChannelData()

        # Set up dict of numpy arrays for each cut and for each channel
        data_dict = {} # dict to be filled and saved
        for cpd in channel_data_dict:
            data_dict[cpd] = {}
            for cut_scheme in cut_scheme_list:
                data_dict[cpd][cut_scheme] = np.array([])

        # Gather files to stitch
        glob_path = io.GetGlobPathHDF5()
        glob_list = sorted(glob.glob(glob_path))

        # Loop files and stitch in data_dict
        for path in glob_list:
            f = h5py.File(path, 'r')
            for grp_name in data_dict:
                for dset_name in data_dict[grp_name]:
                    data_dict[grp_name][dset_name] =\
                        np.insert(data_dict[grp_name][dset_name], len(data_dict[grp_name][dset_name]), f[grp_name][dset_name])
            f.close()

        # Save
        io.SaveHDF5(data_dict)

        # Delete split files
        for path in glob_list:
            os.remove(path)
