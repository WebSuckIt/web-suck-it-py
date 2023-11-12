import time
import logging
from .config import Config, logging
from .metrics import Metrics
from .socket import Suckit, standalone_send

SYS_METRICS = Metrics()
WS_URI = Suckit().get_uri()


class Reporter:
    """
    Class to report system metrics.
    Attributes:
    metrics: dict | str
        System metrics
    """

    metrics: dict | str

    def __call__(self):
        """
        Report system metrics.
        """
        self.__gather()
        self.__push()

    def __gather(self):
        """
        Gather system metrics.
        """
        self.metrics = SYS_METRICS.asjson()

    def __push(self):
        """
        Push system metrics to the socket client.
        """
        standalone_send(self.metrics, ws_uri=WS_URI)


if __name__ == "__main__":
    REPORTER = Reporter()
    INTERVAL = Config.report_interval

    # Keep the main thread running
    while True:
        logging.info(f"Reporting system metrics @{SYS_METRICS.__report.timestamp} ...")
        REPORTER()  # Report system metrics
        logging.debug(f"Metrics: {REPORTER.metrics}")
        logging.debug(f"Waiting {INTERVAL} seconds ...")
        time.sleep(INTERVAL)
