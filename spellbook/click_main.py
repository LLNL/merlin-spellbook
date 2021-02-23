import os
import sys
import traceback

import click


plugin_folder = os.path.join(os.path.dirname(__file__), "commands")


class MyCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.startswith("__"):
                continue
            if filename.endswith(".py"):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name + ".py")
        with open(fn) as f:
            code = compile(f.read(), fn, "exec")
            eval(code, ns, ns)
        return ns["cli"]


def main():
    if len(sys.argv) == 1:
        #parser.print_help(sys.stdout) TODO print help
        return 1
    cli = MyCLI(help="Merlin Spellbook!")  # TODO add --level, --version
    #setup_logging(logger=LOG, log_level="INFO", colors=True)  # TODO level
    try:
        cli()
    except Exception as e:
        print(traceback.format_exc())
        print(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
