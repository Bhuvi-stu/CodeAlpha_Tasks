"""Capture basic packet metadata without inspecting packet payloads."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

try:
    from scapy.all import ARP, ICMP, IP, IPv6, TCP, UDP, sniff
    from scapy.error import Scapy_Exception as _ScapyException
except ImportError as exc:
    ARP = ICMP = IP = IPv6 = TCP = UDP = sniff = None
    SCAPY_IMPORT_ERROR: ImportError | None = exc

    class _ScapyException(Exception):
        pass
else:
    SCAPY_IMPORT_ERROR = None


CSV_FIELDS = (
    "packet_number",
    "timestamp",
    "source_ip",
    "destination_ip",
    "protocol",
    "source_port",
    "destination_port",
    "packet_length",
    "tcp_flags",
)


@dataclass(frozen=True)
class PacketRecord:
    packet_number: int
    timestamp: str
    source_ip: str
    destination_ip: str
    protocol: str
    source_port: str
    destination_port: str
    packet_length: int
    tcp_flags: str


def packet_to_record(packet: Any, packet_number: int) -> PacketRecord:
    """Extract only packet headers and length; never read payload contents."""
    if SCAPY_IMPORT_ERROR is not None:
        raise RuntimeError("Scapy is required to decode packets.") from SCAPY_IMPORT_ERROR

    timestamp = datetime.fromtimestamp(float(packet.time)).astimezone().isoformat(
        timespec="microseconds"
    )

    source_ip = ""
    destination_ip = ""
    if packet.haslayer(IP):
        source_ip = packet[IP].src
        destination_ip = packet[IP].dst
    elif packet.haslayer(IPv6):
        source_ip = packet[IPv6].src
        destination_ip = packet[IPv6].dst
    elif packet.haslayer(ARP):
        source_ip = packet[ARP].psrc
        destination_ip = packet[ARP].pdst

    protocol = "OTHER"
    source_port = ""
    destination_port = ""
    tcp_flags = ""
    if packet.haslayer(TCP):
        protocol = "TCP"
        source_port = str(packet[TCP].sport)
        destination_port = str(packet[TCP].dport)
        tcp_flags = str(packet[TCP].flags)
    elif packet.haslayer(UDP):
        protocol = "UDP"
        source_port = str(packet[UDP].sport)
        destination_port = str(packet[UDP].dport)
    elif packet.haslayer(ICMP):
        protocol = "ICMP"
    elif packet.haslayer(ARP):
        protocol = "ARP"
    elif packet.haslayer(IPv6):
        protocol = "IPv6"
    elif packet.haslayer(IP):
        protocol = "IP"

    return PacketRecord(
        packet_number=packet_number,
        timestamp=timestamp,
        source_ip=source_ip,
        destination_ip=destination_ip,
        protocol=protocol,
        source_port=source_port,
        destination_port=destination_port,
        packet_length=len(packet),
        tcp_flags=tcp_flags,
    )


def write_csv(records: list[PacketRecord], output_path: Path) -> None:
    """Save packet metadata rows to a CSV file."""
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(record) for record in records)


def _print_record(record: PacketRecord) -> None:
    print(
        f"{record.packet_number:>4}  {record.timestamp}  "
        f"{record.source_ip or '-':<39}  {record.destination_ip or '-':<39}  "
        f"{record.protocol:<6}  {record.source_port or '-':>5}  "
        f"{record.destination_port or '-':>5}  {record.packet_length:>6}  "
        f"{record.tcp_flags or '-'}"
    )


def capture_packets(
    interface: str | None,
    count: int,
    timeout: int,
    output_path: Path,
    sniff_function: Callable[..., Any] | None = None,
) -> int:
    """Capture a bounded number of packets and write their metadata."""
    if SCAPY_IMPORT_ERROR is not None:
        raise RuntimeError(
            "Scapy is not installed. Install it with: py -m pip install -r requirements.txt"
        ) from SCAPY_IMPORT_ERROR

    selected_sniff = sniff_function or sniff
    records: list[PacketRecord] = []

    def handle_packet(packet: Any) -> None:
        record = packet_to_record(packet, len(records) + 1)
        records.append(record)
        _print_record(record)

    print(
        " No.  Timestamp                         Source IP                               "
        "Destination IP                          Protocol  Src  Dst  Length  TCP flags"
    )
    print("-" * 150)
    try:
        selected_sniff(
            iface=interface,
            count=count,
            timeout=timeout,
            prn=handle_packet,
            store=False,
        )
    except PermissionError:
        raise
    except OSError:
        raise
    try:
        write_csv(records, output_path)
    except OSError as exc:
        raise RuntimeError(f"Could not write CSV file '{output_path}': {exc}") from exc
    return len(records)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture a limited number of packet headers and save metadata only."
    )
    parser.add_argument(
        "--interface",
        help="Network interface name (default: Scapy/Windows selects its default).",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=20,
        help="Maximum packets to capture (default: 20; must be positive).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Maximum capture duration in seconds (default: 30; must be positive).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("captured_packets.csv"),
        help="CSV output path (default: captured_packets.csv in the current folder).",
    )
    args = parser.parse_args(argv)
    if args.count <= 0:
        parser.error("--count must be a positive integer.")
    if args.timeout <= 0:
        parser.error("--timeout must be a positive integer.")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        packet_count = capture_packets(
            interface=args.interface,
            count=args.count,
            timeout=args.timeout,
            output_path=args.output,
        )
    except PermissionError:
        print(
            "Permission denied while capturing packets. Close VS Code, reopen it "
            "with Run as administrator, then try again.",
            file=sys.stderr,
        )
        return 1
    except OSError as exc:
        print(f"Network capture failed: {exc}", file=sys.stderr)
        if sys.platform == "win32":
            print(
                "On Windows, install or repair Npcap from https://npcap.com/ "
                "and make sure its packet-capture driver is enabled.",
                file=sys.stderr,
            )
        return 1
    except _ScapyException as exc:
        print(f"Scapy could not start packet capture: {exc}", file=sys.stderr)
        if sys.platform == "win32":
            print(
                "On Windows, install or repair Npcap from https://npcap.com/ "
                "and make sure its packet-capture driver is enabled.",
                file=sys.stderr,
            )
        return 1
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"\nCaptured {packet_count} packet(s). Metadata CSV saved to: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
