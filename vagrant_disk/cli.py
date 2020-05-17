import sys
import pathlib
import argparse
import shutil
from . import __version__
from .box import VagrantBoxReader


class Command:
    VERSION = __version__
    PROG = 'boxdisk'

    @classmethod
    def main(cls):
        try:
            sys.exit(cls().run_from_argv(sys.argv))
        except KeyboardInterrupt:
            sys.exit(1)

    def create_parser(self, prog=None):
        parser = argparse.ArgumentParser(prog=prog or getattr(self, 'PROG', None))
        parser.set_defaults(op='list')

        parser.add_argument(
            'box_file', action='store',
            metavar='BOX_FILE',
            help="Vagrant box file",
        )
        parser.add_argument(
            '--list', '-l', action='store_const',
            dest='op', const='list',
            help="list disks in vagrant box file",
            )
        parser.add_argument(
            '--extract', '-x', action='store_const',
            dest='op', const='extract',
            help="extract disk images from vagrant box file",
            )
        parser.add_argument(
            '--traceback', action='store_true',
            help="traceback on exception",
            )
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s version {}'.format(getattr(self, 'VERSION', None) or 'WIP'),
            )
        return parser

    def print_usage(self):
        parser = self.create_parser()
        parser.print_usage()

    def run_from_argv(self, argv):
        parser = self.create_parser()
        options = parser.parse_args(argv[1:])
        kwargs = options.__dict__
        args = kwargs.pop('args', [])
        return self.execute(*args, **kwargs)

    def execute(self, *args, **options):
        self.stdout = options.pop('stdout', sys.stdout)
        self.stderr = options.pop('stderr', sys.stderr)
        self.traceback = options.pop('traceback', False)
        try:
            return self.handle(*args, **options)
        except Exception as err:
            if self.traceback:
                raise
            else:
                self.stderr.write("{}: {}\n".format(type(err).__name__, err))
            sys.exit(1)

    def handle(self, *args, box_file=None, op=None, **options):
        box = VagrantBoxReader(box_file)
        handler = self.op_handler.get(op)
        handler(self, box)

    def op_list(self, box):
        for num, boxdisk in enumerate(box.iter_disk(), start=1):
            self.stdout.write('{num}: {0[disk_id]:12}  {0[href]}\n'.format(boxdisk, num=num))

    def op_extract(self, box):
        for boxdisk in box.iter_disk():
            with boxdisk.extractfile() as fsrc:
                suffix = pathlib.PosixPath(boxdisk['href']).suffix
                dst = pathlib.PosixPath('{}{}'.format(boxdisk['disk_id'], suffix))
                with dst.open('wb') as fdst:
                    self.stderr.write("-> {}\n".format(dst))
                    shutil.copyfileobj(fsrc, fdst)

    op_handler = {
        'list': op_list,
        'extract': op_extract,
    }
