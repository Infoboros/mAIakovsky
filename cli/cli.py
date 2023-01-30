import os
from click import MultiCommand

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')


class CLI(MultiCommand):

    def list_commands(self, ctx):
        return sorted(
            [
                filename[:-3]
                for filename in os.listdir(plugin_folder)
                if filename.endswith('.py') and filename != '__init__.py'
            ]
        )

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name + '.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']
