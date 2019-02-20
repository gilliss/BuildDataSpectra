"""
"""
from ROOT import TFile, TChain

class Gather:
    """
    """
    def __init__(self, st):
        self.data_set = st.data_set
        self.data_type = st.data_type
        self.file_index = st.file_index

    def Run(self):
        """
        """
        data_set = self.data_set
        data_type = self.data_type
        file_index = self.file_index

        print('Gather::Run()')

        # READ FILES INTO TCHAIN
        t = TChain('skimTree', 'skimTree')
        in_file = GetSkimPath(data_set, data_type, file_index) # specSkimFile may be None
        t.Add(in_file)
        n_entries = t.GetEntries()
        print('in_file', in_file)
        print('t', t)
        print('t.GetEntries()', n_entries)
        in_file.Close()
