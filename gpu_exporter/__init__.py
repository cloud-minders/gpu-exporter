from gpu_exporter.cli import cli
import gpu_exporter.subscribers
from gpu_exporter.config.events_emitter import emitter
import traceback


def main():
    try:
        cli()
    except SystemExit:
        pass
    except BaseException as error:
        emitter.emit("logger.error", msg=repr(error))
        emitter.emit("logger.error", msg=traceback.print_exc().__str__())

    emitter.emit("logger.debug", msg="finished running cli.")


if __name__ == "__main__":
    main()
