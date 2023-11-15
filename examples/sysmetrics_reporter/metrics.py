import datetime
import json
from typing import Any, NamedTuple, Optional

import psutil


class CpuUsage(NamedTuple):
    """CPU usage information."""

    usage: Optional[str]


class MemoryUsage(NamedTuple):
    """Memory usage information."""

    usage: Optional[str]
    total: Optional[str]
    free: Optional[str]
    used: Optional[str]
    active: Optional[str]
    available: Optional[str]
    inactive: Optional[str]
    wired: Optional[str]


class NetworkStats(NamedTuple):
    """Network statistics."""

    bytes_sent: Optional[int]
    bytes_received: Optional[int]


class DiskUsage(NamedTuple):
    """Disk usage information."""

    device: Optional[str]
    mountpoint: Optional[str]
    total: Optional[int]
    used: Optional[int]
    free: Optional[int]
    percent: Optional[int]


class ProcessInfo(NamedTuple):
    """Process information."""

    pid: Optional[int]
    name: Optional[str]
    cpu_percent: Optional[float]
    memory_info: Optional[int]
    status: Optional[str]
    memory_percent: Optional[float]
    create_time: Optional[float]


class BatteryInfo(NamedTuple):
    """Battery information."""

    percent: Optional[float]
    power_plugged: Optional[bool]
    seconds_left: Optional[int]


MetricsReport = NamedTuple(
    "MetricsReport",
    [
        ("cpu_usage", CpuUsage),
        ("memory_usage", MemoryUsage),
        ("disk_usage", list[DiskUsage]),
        ("network_stats", NetworkStats),
        ("process_info", list[ProcessInfo]),
        ("battery_info", BatteryInfo),
        ("timestamp", Optional[str]),
    ],
)


class Metrics:
    """
    Class to get system metrics.

    Attributes:

    cpu_usage: CpuUsage
        CPU usage information
    memory_usage:
        Memory usage information
    disk_usage list[DiskUsage]:
        Disk usage information
    network_stats: NetworkStats
        Network statistics
    process_info: list[ProcessInfo]
        Information about running processes
    battery_info: BatteryInfo
        Battery information
    """

    report: MetricsReport = MetricsReport(
        cpu_usage=CpuUsage(usage=""),
        memory_usage=MemoryUsage(
            usage="",
            total="",
            free="",
            used="",
            active="",
            available="",
            inactive="",
            wired="",
        ),
        disk_usage=[
            DiskUsage(
                device="",
                mountpoint="",
                total=0,
                used=0,
                free=0,
                percent=0,
            )
        ],
        network_stats=NetworkStats(
            bytes_sent=0,
            bytes_received=0,
        ),
        process_info=[
            ProcessInfo(
                pid=0,
                name="",
                cpu_percent=0.0,
                memory_info=0,
                status="",
                memory_percent=0.0,
                create_time=0.0,
            )
        ],
        battery_info=BatteryInfo(percent=0.0, power_plugged=False, seconds_left=0),
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    @property
    def cpu_usage(self) -> CpuUsage:
        """
        Get CPU usage.
        Returns:
            CpuUsage: CPU usage information
        """
        cpu_percent = psutil.cpu_percent(interval=1)
        return CpuUsage(usage=f"{cpu_percent}%")  #  dict[str, str]

    @property
    def memory_usage(self) -> MemoryUsage:
        """
        Get memory usage.
        Returns:
            MemoryUsage: Memory usage information
        """
        memory = psutil.virtual_memory()
        return MemoryUsage(
            usage=f"{memory.percent}%",  # default unit is byte
            total=f"{memory.total / 2**30:.2f} GB",  # 2**30 = 1024**3 = 1GB
            free=f"{memory.free / 2**30:.2f} GB",
            used=f"{memory.used / 2**30:.2f} GB",
            active=f"{memory.active / 2**30:.2f} GB",
            available=f"{memory.available / 2**30:.2f} GB",
            inactive=f"{memory.inactive / 2**30:.2f} GB",
            wired=f"{memory.wired / 2**30:.2f} GB",
        )
        # MemoryUsage(**memory._asdict()) -> dict[str, str]

    @property
    def disk_usage(self) -> list[DiskUsage]:
        """
        Get disk usage information.
        Returns:
           list[DiskUsage]: list of Disk usage information
        """
        partitions = psutil.disk_partitions()
        disk_usage_info: list[DiskUsage] = []

        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage_info.append(
                DiskUsage(
                    device=partition.device,
                    mountpoint=partition.mountpoint,
                    total=usage.total,
                    used=usage.used,
                    free=usage.free,
                    percent=usage.percent,
                )
            )
        return disk_usage_info  # list[dict[str, str]]

    @property
    def network_stats(self) -> NetworkStats:
        """
        Get network statistics.
        Returns:
            NetworkStats: Network statistics
        """
        network_stats = psutil.net_io_counters()
        return NetworkStats(
            bytes_sent=network_stats.bytes_sent,
            bytes_received=network_stats.bytes_recv,
        )  # dict[str, int]

    @property
    def process_info(self) -> list[ProcessInfo]:
        """
        Get information about running processes as a list of dictionaries.
        Returns:
            list[PocessInfo]: list of Information about running processes
        """
        process_info = []

        for process in psutil.process_iter(
            attrs=[
                "pid",
                "name",
                "cpu_percent",
                "memory_info",
                "status",
                "memory_percent",
                "create_time",
            ]
        ):
            process_info.append(
                ProcessInfo(
                    pid=process.info["pid"],
                    name=process.info["name"],
                    cpu_percent=process.info["cpu_percent"],
                    memory_info=process.info["memory_info"].rss
                    if process.info["memory_info"]
                    else None,
                    status=process.info["status"],
                    memory_percent=process.info["memory_percent"],
                    create_time=process.info["create_time"],
                )
            )

        return process_info  # list[dict[str, Any]]

    @property
    def battery_info(self) -> BatteryInfo:
        """
        Get battery information.
        Returns:
            BatteryInfo: Battery information
        """
        try:
            battery_info = psutil.sensors_battery()
            return BatteryInfo(
                percent=battery_info.percent,
                power_plugged=battery_info.power_plugged,
                seconds_left=battery_info.secsleft,
            )
        except AttributeError:
            return BatteryInfo(percent=None, power_plugged=None, seconds_left=None)

    def asdict(self) -> dict[str, Any]:
        """
        Return metrics as a dictionary.
        """
        dict_report = self()._asdict()
        return self.__parse_dict(dict_report)

    def __parse_dict(self, d: dict[str, Any]) -> dict[str, Any]:
        for k, v in d.items():
            if isinstance(v, list):
                items = []
                for i in v:
                    if hasattr(i, "_asdict"):
                        items.append(i._asdict())
                    else:
                        items.append(i)
                d[k] = items
            elif hasattr(v, "_asdict"):
                d[k] = v._asdict()
        return d

    def asjson(self) -> str:
        """
        Return metrics as a JSON string.
        """
        return json.dumps(self.asdict(), indent=2)

    def todict(self) -> dict[str, Any]:
        """
        Return Report as a dictionary.
        """
        dict_report = self.report._asdict()
        return self.__parse_dict(dict_report)

    def tojson(self) -> str:
        """
        Return Report as a JSON string.
        """
        return json.dumps(self.todict(), indent=2)

    def __call__(self) -> MetricsReport:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.report = MetricsReport(
            cpu_usage=self.cpu_usage,
            memory_usage=self.memory_usage,
            disk_usage=self.disk_usage,
            network_stats=self.network_stats,
            process_info=self.process_info,
            battery_info=self.battery_info,
            timestamp=timestamp,
        )
        return self.report
