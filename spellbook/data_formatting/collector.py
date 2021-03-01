import json


def process_args(args):
    result = []
    for path in args.instring.split("\n"):
        with open(path, "r") as json_file:
            result.append(json.load(json_file))

    with open(args.outfile, "w") as outfile:
        json.dump(result, outfile)
