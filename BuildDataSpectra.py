"""
"""
import argparse

import Management.Settings as Settings
import Classes.Gather as Gather
import Classes.Stitch as Stitch

def main(args):
    """
    According to args, gather hits or stitch together jobs that were split up.
    Save arrays of hits, organized in a dict by cut scheme, in .npz files.
    """
    st = Settings.Settings(args)

    if not st.stitch:
        print('gather')
        gather = Gather.Gather(st)
        gather.Run()
    else:
        print('stitch')
        stitch = Stitch.Stitch(st)
        stitch.Run()

if __name__ == "__main__":
    """
    Parse arguments and execute main().
    main() will execute code to gather the data, or stitch together data that
    has already been gathered.
    """
    parser = argparse.ArgumentParser(description = 'Gather data or stitch gathered data.')
    parser.add_argument('--stitch', dest = 'stitch', action = 'store_true', default = False,\
        help = 'Stitch gathered hits. If not invoked, default behavior is gather hits.')
    parser.add_argument('data_set', metavar = 'data_set', type = str,\
        help = 'str of data set: \'DS0\',\'DS1\',\'DS2\',\'DS3\',\'DS4\',\'DS5a\',\'DS5b\',\'DS5c\',\'DS6\'')
    parser.add_argument('data_type', metavar = 'data_type', type = str,\
        help = 'str for \'open\' or \'blind\' data')
    parser.add_argument('--file_index', dest = 'file_index', type = int,\
        help = 'index of the skimfile, skim_<index>.root')
    print('Parsed args:\n    ', parser.parse_args())

    main(parser.parse_args())
