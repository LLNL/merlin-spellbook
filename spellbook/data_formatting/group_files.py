import argparse
import pickle as pkl
import sys


def get_chunks(itr, n):
    for i in range(0, len(itr), n):
        yield itr[i:i + n]


def process_args(args):
    filepaths = args.filepaths
    n_files_to_collect = len(filepaths)
    n_chunks = args.n_chunks
    n_files_per_chunk = int(n_files_to_collect / n_chunks) #TODO accomodate odd # of files, non-integer ratios
    filepath_chunks = list(get_chunks(filepaths, n_files_per_chunk))
    pkl.dump(filepath_chunks, open("filepath_chunks.pkl", "wb"))


def setup_argparse():
    parser = argparse.ArgumentParser(description="Group a list of filepaths into chunks of size 'n_chunks'")
    parser.add_argument(
        "--n_chunks", action="store", type=int, help="Number of chunks"
    )
    parser.add_argument('--filepaths', nargs='+', default=[])
    parser.set_defaults(func=process_args)
    return parser


def main():
    parser = setup_argparse()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
