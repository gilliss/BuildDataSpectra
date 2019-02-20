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

        # Environment variables
        self.skim_data_dirname = os.environ['MJDDATADIR'] + '/surfmjd/analysis/skim'
        self.channel_data_dirname = os.environ['CHANNELDATADIR']
        self.bds_output_dirname = os.environ['BDSOUTPUTDIR']
