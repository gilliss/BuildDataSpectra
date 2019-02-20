"""
"""
import os
import sys
import json

class DataInfo:
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

        # Cut schemes
        self.cut_scheme_list = ['R','RM','RA','RD','RMA','RMD','RAD','RMAD', 'RM2sum','RMa','RmD']

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

    def GetChannelData(self):
        """
        Return dict of the channel data for this data set.
        The dict holds only those channels included in the "DS Livetime" technical documents.
        For each channel, the dict holds
            'CPD': {'good' 'detectorName' 'channel' 'detectorType' 'activeMass' 'liveTime' 'exposure' 'exposureUncert'}
        """
        data_set = self.data_set
        data_type = self.data_type
        channel_data_dirname = self.channel_data_dirname

        dirname = channel_data_dirname
        if data_type == 'open': basename = '%s_channel_data.json' % data_set
        if data_type == 'blind': basename = '%s_%s_channel_data.json' % (data_set, data_type)
        path = dirname + '/' + basename

        if os.path.isfile(path):
            with open(path) as channel_data_file:
                channel_data_dict = json.load(channel_data_file)
            channel_data_file.close()
            return channel_data_dict
        else:
            sys.exit('Error: DataInfo::GetChannelData(): path DNE')

    def GetCutScheme(self, cut_scheme):
        """
        Returns a string of comparisons corresponding to cutScheme
        """
        data_set = self.data_set

        cutEnergy = 't.trapENFCalC[j] > 0.0 and t.trapENFCalC[j] < 10000.0'
        cutSumEnergy = 't.sumEHClean > 0.0 and t.sumEHClean < 10000.0'
        cutDC = 't.isGood and (not (t.isLNFill1 and t.C[j]==1)) and (not (t.isLNFill2 and t.C[j]==2)) and (not t.muVeto) and (not t.wfDCBits[j])'
        cutHG = 't.gain[j] == 0'
        cutLG = 't.gain[j] == 1'
        cutEnr = 't.isEnr[j]'
        cutNat = 't.isNat[j]'
        cutMult = 't.mHL == 1'
        cutMult2 = 't.mHL == 2'
        cutMult_inv = 't.mHL > 1'
        cutAvsE = 't.avse[j] > -1'
        cutAvsE_inv = 't.avse[j] <= -1'
        cutDCR = 't.dcr99[j] < 0'
        AND = ' and '
        cut_scheme_dict = { # ['R','RM','RA','RD','RMA','RMD','RAD','RMAD', 'RM2sum','RMa','RmD']
            'R': cutEnergy + AND + cutHG + AND + cutDC,
            'RM': cutEnergy + AND + cutHG + AND + cutDC + AND + cutMult,
            'RA': cutEnergy + AND + cutHG + AND + cutDC + AND + cutAvsE,
            'RD': cutEnergy + AND + cutHG + AND + cutDC + AND + cutDCR,
            'RMA': cutEnergy + AND + cutHG + AND + cutDC + AND + cutMult + AND + cutAvsE,
            'RMD': cutEnergy + AND + cutHG + AND + cutDC + AND + cutMult + AND + cutDCR,
            'RAD': cutEnergy + AND + cutHG + AND + cutDC + AND + cutAvsE + AND + cutDCR,
            'RMAD': cutEnergy + AND + cutHG + AND + cutDC + AND + cutMult + AND + cutAvsE + AND + cutDCR,

            'RM2sum': cutSumEnergy + AND + cutHG + AND + cutDC + AND + cutMult2,
            'RMa': cutEnergy + AND + cutHG + AND + cutDC + AND + cutMult + AND + cutAvsE_inv,
            'RmD': cutEnergy + AND + cutHG + AND + cutDC + AND + cutMult_inv + AND + cutDCR,
        }
        final_cut = cut_scheme_dict[cut_scheme];
        if data_set == 'DS5a':
            final_cut = final_cut + ' and t.run >= 18623 and t.run <= 22392' # DS5a , ends with skimDS5_79.root
        if data_set == 'DS5b':
            final_cut = final_cut + ' and t.run >= 22393 and t.run <= 23958' # DS5b , begin with skimDS5_80.root
        return final_cut
