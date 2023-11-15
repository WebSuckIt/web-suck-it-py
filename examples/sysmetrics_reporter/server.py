import time

from config import Config, logging
from metrics import Metrics
from sockit import Suckit, standalone_send

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
        logging.info(
            f"[*] Successfully reported system metrics at {SYS_METRICS.report.timestamp}"
        )

    def __gather(self):
        """
        Gather system metrics.
        """
        logging.debug("[*] Gathering system metrics")
        self.metrics = SYS_METRICS.asjson()
        logging.debug(f"[*] Metics: \n{self.metrics}")

    def __push(self):
        """
        Push system metrics to the socket client.
        """
        logging.debug(f"[*] Pushing system metrics to {WS_URI} ...")
        standalone_send(self.metrics, ws_uri=WS_URI)
        logging.debug(f"[*] Successfully pushed system metrics to {WS_URI} ...")


def main():
    """
    Main function.
    """
    reporter = Reporter()
    interval = Config.report_interval
    logging.info(f"[*] Reporting to websocket uri: \n {WS_URI}")
    logging.info(f"[*] Reporting system metrics every {interval} seconds")
    # Keep the main thread running
    while True:
        reporter()
        logging.info(f"[*] Waiting for {interval} seconds")
        time.sleep(interval)


if __name__ == "__main__":
    main()
