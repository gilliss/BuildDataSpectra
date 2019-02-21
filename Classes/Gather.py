"""
"""
from ROOT import TFile, TChain
import numpy as np

import Tools.FileIO as FileIO
import Tools.DataInfo as DataInfo

class Gather:
    """
    Gather hits into arrays and save
    """
    def __init__(self, st):
        self.data_set = st.data_set
        self.data_type = st.data_type
        self.file_index = st.file_index

        self.io = FileIO.FileIO(st)
        self.di = DataInfo.DataInfo(st)

    def Run(self):
        """
        Gather hits into arrays and save
        """
        file_index = self.file_index
        io = self.io
        di = self.di
        cut_scheme_list = di.cut_scheme_list

        # Read files into TChain
        t = TChain('skimTree', 'skimTree')
        in_file_path = io.GetSkimFilePath()
        t.Add(in_file_path)
        n_entries = t.GetEntries()
        # print('in_file_path', in_file_path)
        # print('t', t)
        # print('t.GetEntries()', n_entries)

        # Read in channel data dict
        channel_data_dict = di.GetChannelData()

        # Set up dict of numpy arrays for each cut and for each channel
        data_dict = {} # dict to be filled and saved
        for cpd in channel_data_dict:
            data_dict[cpd] = {}
            for cut_scheme in cut_scheme_list:
                data_dict[cpd][cut_scheme] = np.array([])

        # Loop TChain
        for i in range(n_entries):
            entry = t.GetEntry(i)
            # if i % int(0.1 * n_entries) == 0:
            #     print('progress ... %.0f pct ... on entry %d' % (100*(i/n_entries), i))
            for j in range(len(t.channel)):
                cpd = 'C' + str(t.C[j]) + 'P' + str(t.P[j]) + 'D' + str(t.D[j])
                if cpd in data_dict:
                    for cut_scheme in cut_scheme_list:
                        if eval(di.GetCutScheme(cut_scheme)):
                            data_dict[cpd][cut_scheme] =\
                                np.insert(data_dict[cpd][cut_scheme], len(data_dict[cpd][cut_scheme]), t.trapENFCalC[j])

        # Save NPZ
        io.SaveNPZ(data_dict)

        # Save NPY
        # Loop each channel and cut in channel data dict and save
        # for cpd in data_dict:
        #     for cut_scheme in data_dict[cpd]:
        #         io.SaveNPY(data_dict[cpd][cut_scheme], cpd, cut_scheme)

        # print('FINISHED')
