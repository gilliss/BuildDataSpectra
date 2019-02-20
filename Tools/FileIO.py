"""
"""
import os
import sys

class FileIO:
    """
    """
    def __init__(self, st):
        self.data_set = st.data_set
        self.data_type = st.data_type
        self.file_index = st.file_index

        # SOME GLOBAL VARIABLES
        self.skim_data_dirname = st.skim_data_dirname
        self.channel_data_dirname = st.channel_data_dirname
        self.bds_output_dirname = st.bds_output_dirname

    def GetGatRev(self):
        """
        Return the GAT revision string.
        The 'blind' strings refer to blind_b14, or the most unblinded files available.
        """
        data_set = self.data_set
        data_type = self.data_type

        gat_rev_dict = {
            'DS0': {
                'open': 'GAT-v01-07', # updated 2017-09
                'blind': None
            },
            'DS1': {
                'open': 'GAT-v01-07', # updated 2017-09
                'blind': 'GAT-v02-01' # updated 2018-05-23 1017 ET
            },
            'DS2': {
                'open': 'GAT-v01-07', # updated 2017-09
                'blind': 'GAT-v02-01' # updated 2018-05-23 1017 ET
            },
            'DS3': {
                'open': 'GAT-v01-07', # updated 2017-09
                'blind': None
            },
            'DS4': {
                'open': 'GAT-v01-07', # updated 2017-09
                'blind': None
            },
            'DS5a': {
                'open': 'GAT-v01-07', # updated 2017-09
                'blind': None
            },
            'DS5b': {
                'open': 'GAT-v01-07', # updated 2017-09
                'blind': None
            },
            'DS5c': {
                'open': 'GAT-v02-00-72-gc94f3a1', # updated 2018-05-17
                'blind': 'GAT-v02-01' # updated 2018-05-23 1017 ET
            },
            'DS6': {
                'open': 'GAT-v02-00-66-gf078278', # updated 2018-05-16
                'blind': 'GAT-v02-01' # updated 2018-05-23 1017 ET
            }
        }

        if gat_rev_dict[data_set][data_type] is not None:
            return gat_rev_dict[data_set][data_type]
        else:
            sys.exit('Error: FileIO::GetGatRev(): None')


    def GetSkimFilePath(self):
        """
        Full file path
        """
        data_set = self.data_set
        data_type = self.data_type
        file_index = self.file_index
        skim_data_dirname = self.skim_data_dirname
        channel_data_dirname = self.channel_data_dirname
        bds_output_dirname = self.bds_output_dirname

        data_set_base = data_set[:3]
        if data_set == 'DS5c': data_set_base = data_set

        dirname = skim_data_dirname
        if data_type == 'open': dirname += '/' + data_set_base
        if data_type == 'blind': dirname += '/' + '%s_blind_b14' % data_set_base
        dirname += '/' + '%s' % self.GetGatRev()

        basename = 'skim%s*.root' % data_set_base
        if file_index is not None:
            basename = 'skim%s_%d.root' % (data_set_base, file_index)

        path = dirname + '/' + basename

        if os.path.isfile(path):
            return path
        else:
            sys.exit('Error: FileIO::GetSkimFilePath(): path DNE')
