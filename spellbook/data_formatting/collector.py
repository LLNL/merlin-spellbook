##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################

import json


def process_args(args):
    result = []
    for path in args.instring.split("\n"):
        with open(path, "r") as json_file:
            result.append(json.load(json_file))

    with open(args.outfile, "w") as outfile:
        json.dump(result, outfile)
