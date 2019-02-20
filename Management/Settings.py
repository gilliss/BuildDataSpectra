"""
"""
import os

class Settings:
    """
    """
    def __init__(self, args):
        self.stitch = args.stitch
        self.data_set = args.data_set
        self.data_type = args.data_type
        self.file_index = args.file_index

        # SOME GLOBAL VARIABLES
        try:
            self.skim_data_dirname = os.environ['MJDDATADIR'] + '/surfmjd/analysis/skim'
        except KeyError:
            print('Exception', 'Settings::__init__(): Perhaps on local machine')
        try:
            self.channel_data_dirname = os.environ['CHANNELDATADIR']
        except KeyError:
            print('Exception', 'Settings::__init__(): Perhaps on local machine')
        try:
            self.bds_output_dirname = os.environ['BDSOUTPUTDIR']
        except KeyError:
            print('Exception', 'Settings::__init__(): Perhaps on local machine')
