import os

from .. lib.myparser import CrispyArgumentParser
from .. lib.module import CrispyModule

logger = logging.getLogger(__name__)

class VirtualMachineModule(CrispyModule):
    """ Determine if remote machine is a virtual machine. """

    def init_argparse(self):
        self.parser = CrispyArgumentParser(prog="virtual", description=self.__doc__)
        #self.parser.add_argument()

    def run(self, args):
        pass