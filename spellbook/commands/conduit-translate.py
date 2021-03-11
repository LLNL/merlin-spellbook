from types import SimpleNamespace

import click


@click.command()
@click.option(
    "-input",
    required=False,
    default="results_features.hdf5",
    type=click.Path(),
    help=".hdf5 file with data in it",
)
@click.option(
    "-output",
    required=False,
    default="results_features.npz",
    type=click.Path(),
    help=".npz file with the arrays",
)
@click.option(
    "-schema",
    required=False,
    default="auto",
    type=str,
    help="schema for a single sample that says what data to translate. Defaults to whole first node. Can be a comma-delimited list of subpaths, eg inputs,outputs/scalars,metadata",
)
def cli(input, output, schema):
    """
    Flatten sample file into another format (conduit-compatible or numpy)", filtering with an external schema.
    """
    from spellbook.data_formatting.conduit.python import translator

    args = SimpleNamespace(**{"input": input, "output": output, "schema": schema})
    translator.process_args(args)
