import logging
import os
import sys
from typing import List, Optional

import click

from spellbook import VERSION
from spellbook.log_formatter import setup_logging


LOG = logging.getLogger("spellbook")
PLUGIN_DIR = os.path.join(os.path.dirname(__file__), "commands")


class SpellbookCLI(click.MultiCommand):
    """_summary_

    Args:
        click (_type_): _description_
    """

    def list_commands(self, ctx: click.Context) -> List[str]:
        """Actively looks for command scripts in the plugin directory

        Args:
            ctx (click.Context):

        Returns:
            List[str]: List of implemented spellbook commands
        """
        files = os.listdir(PLUGIN_DIR)
        files = [file[:-3] for file in files if file.endswith(".py") if not file.startswith("__")]
        return sorted(files)

    def get_command(self, ctx: click.Context, cmd_name: str) -> click.core.Command:
        """Get command from implemented scripts

        Args:
            ctx (click.Context): _description_
            cmd_name (str): _description_

        Raises:
            FileNotFoundError: _description_

        Returns:
            click.core.Command: Requested function
        """
        command_script_path = os.path.join(PLUGIN_DIR, cmd_name + ".py")
        if not os.path.isfile(command_script_path):
            raise FileNotFoundError(f"No script for command '{cmd_name}' was found")

        globals_dict: dict = {}
        with open(command_script_path, "rb") as f:
            code = compile(f.read(), command_script_path, "exec")

        eval(code, globals_dict)
        return globals_dict["cli"]


@click.command(cls=SpellbookCLI)
@click.option(
    "--level",
    required=False,
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
    help="Set the logger level",
)
@click.version_option(VERSION)
def spellbook(level: Optional[str]):
    setup_logging(logger=LOG, log_level=level.upper(), colors=True)


def main() -> None:
    if len(sys.argv) == 1:
        with click.Context(spellbook) as ctx:
            click.echo(spellbook.get_help(ctx))
        return 1
    try:
        spellbook()
    except Exception as err:
        LOG.error(str(err))
        return 1


if __name__ == "__main__":
    sys.exit(main())
