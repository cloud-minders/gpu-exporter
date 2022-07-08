from miner_exporter.cli.main import cli
import miner_exporter.subscribers.main
from miner_exporter.config.events_emitter import emitter
import traceback
import sys, os

if __name__ == "__main__":
    try:
        cli()
    except SystemExit:
        pass
    except BaseException as error:
        emitter.emit("logger.error", msg=repr(error))
        emitter.emit("logger.error", msg=traceback.print_exc().__str__())

    emitter.emit("logger.info", msg="finished running cli.")


def override_where():
    """overrides certifi.core.where to return actual location of cacert.pem"""
    # change this to match the location of cacert.pem
    return os.path.abspath("cacert.pem")


# is the program compiled?
if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = override_where()
    certifi.core.where = override_where

    # delay importing until after where() has been replaced
    import requests.utils
    import requests.adapters

    # replace these variables in case these modules were
    # imported before we replaced certifi.core.where
    requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()
