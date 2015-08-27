import sys
import argparse
import utils

parser = argparse.ArgumentParser(
    prog='sc', usage='./sc <txt_files_dir>',
    description='Whatever the hell it does'
)

parser.add_argument(
    '-d', '--dir', action='store', dest='txt_dir', default='sample_txts',
    help=('Directory where text files for vectorization, similarity, '
          'clustering, etc. are stored')
)

def main(argv=sys.argv[1:]):
    arg = parser.parse_args()
    vecs = utils.vectorize_txts(arg.txt_dir)
    winst = vecs['cracked_winston']
    utils.collapse_vector(winst,43)
    import pdb; pdb.set_trace()
    print 'blah'

if __name__ == '__main__':
    main()
