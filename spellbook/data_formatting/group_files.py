import pickle as pkl


def get_chunks(itr, n):
    for i in range(0, len(itr), n):
        yield itr[i : i + n]


def process_args(args):
    filepaths = args.filepaths
    n_files_to_collect = len(filepaths)
    n_chunks = args.n_chunks
    n_files_per_chunk = int(
        n_files_to_collect / n_chunks
    )  # TODO accomodate odd # of files, non-integer ratios
    filepath_chunks = list(get_chunks(filepaths, n_files_per_chunk))
    pkl.dump(filepath_chunks, open(args.outfile, "wb"))
