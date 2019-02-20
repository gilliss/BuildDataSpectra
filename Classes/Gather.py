"""
"""
from ROOT import TFile, TChain

import Tools.FileIO as FileIO

class Gather:
    """
    """
    def __init__(self, st):
        self.data_set = st.data_set
        self.data_type = st.data_type
        self.file_index = st.file_index

        self.io = FileIO.FileIO(st)

    def Run(self):
        """
        """
        io = self.io

        print('Gather::Run()')

        # READ FILES INTO TCHAIN
        t = TChain('skimTree', 'skimTree')
        in_file = io.GetSkimFilePath()
        t.Add(in_file)
        n_entries = t.GetEntries()
        print('in_file', in_file)
        print('t', t)
        print('t.GetEntries()', n_entries)
