"""
"""
import os
import sys
import numpy as np
import h5py

import Tools.DataInfo as DataInfo

class FileIO:
    """
    """
    def __init__(self, st):
        self.data_set = st.data_set
        self.data_type = st.data_type
        self.file_index = st.file_index

        # Environment variables
        self.skim_data_dirname = st.skim_data_dirname
        self.channel_data_dirname = st.channel_data_dirname
        self.bds_output_dirname = st.bds_output_dirname

        self.di = DataInfo.DataInfo(st)

    def GetSkimFilePath(self):
        """
        Return full skim file path
        """
        data_set = self.data_set
        data_type = self.data_type
        file_index = self.file_index
        skim_data_dirname = self.skim_data_dirname
        di = self.di

        data_set_base = data_set[:3]
        if data_set == 'DS5c': data_set_base = data_set

        dirname = skim_data_dirname
        if data_type == 'open': dirname += '/' + data_set_base
        if data_type == 'blind': dirname += '/' + '%s_blind_b14' % data_set_base
        dirname += '/' + '%s' % di.GetGatRev()

        if file_index is not None:
            basename = 'skim%s_%d.root' % (data_set_base, file_index)
        else:
            basename = 'skim%s*.root' % data_set_base

        path = dirname + '/' + basename

        if os.path.isdir(dirname):
            return path
        else:
            sys.exit('Error: FileIO::GetSkimFilePath(): path DNE %s' % path)

    def SaveNPY(self, array, cpd, cut_scheme):
        """
        Save arrays in individual files
        """
        data_set = self.data_set
        data_type = self.data_type
        file_index = self.file_index
        bds_output_dirname = self.bds_output_dirname

        dirname = bds_output_dirname
        if file_index is not None:
            basename = '%s_%s_%s_%s_%s.npy' % (cpd, data_set, data_type, cut_scheme, file_index)
        else:
            basename = '%s_%s_%s_%s.npy' % (cpd, data_set, data_type, cut_scheme)
        path = dirname + '/' + basename

        np.save(path, array)

    def SaveNPZ(self, dict):
        """
        Save a dictionary holding data arrays into one .npz file
        """
        data_set = self.data_set
        data_type = self.data_type
        file_index = self.file_index
        bds_output_dirname = self.bds_output_dirname

        dirname = bds_output_dirname
        if file_index is not None:
            basename = '%s_%s_%d.npz' % (data_set, data_type, file_index)
        else:
            basename = '%s_%s.npz' % (data_set, data_type)
        path = dirname + '/' + basename

        np.savez(file = path, arrayDict = dict) # the LHS arrayDict is used as the keyword

    def SaveHDF5(self, dict):
        """
        Save a dictionary holding data arrays into one .npz file
        """
        data_set = self.data_set
        data_type = self.data_type
        file_index = self.file_index
        bds_output_dirname = self.bds_output_dirname

        dirname = bds_output_dirname
        if file_index is not None:
            basename = '%s_%s_%d.hdf5' % (data_set, data_type, file_index)
        else:
            basename = '%s_%s.hdf5' % (data_set, data_type)
        path = dirname + '/' + basename

        f = h5py.File(path, 'w')
        for grp_name in dict:
            grp = f.create_group(grp_name)
            for dset_name in dict[grp_name]:
                dset = grp.create_dataset(dset_name, data = dict[grp_name][dset_name])
        f.close()

    def GetGlobPathNPZ(self):
        """
        Get wildcard path to NPZ files from split jobs
        """
        data_set = self.data_set
        data_type = self.data_type
        bds_output_dirname = self.bds_output_dirname

        dirname = bds_output_dirname
        basename = '%s_%s_*.npz' % (data_set, data_type)
        return dirname + '/' + basename

    def GetGlobPathHDF5(self):
        """
        Get wildcard path to HDF5 files from split jobs
        """
        data_set = self.data_set
        data_type = self.data_type
        bds_output_dirname = self.bds_output_dirname

        dirname = bds_output_dirname
        basename = '%s_%s_*.hdf5' % (data_set, data_type)
        return dirname + '/' + basename
