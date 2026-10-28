import csv
import tempfile
import unittest
from pathlib import Path

from scapy.all import ICMP, IP, Raw, TCP, UDP

from sniffer import CSV_FIELDS, packet_to_record, write_csv


class PacketMetadataTests(unittest.TestCase):
    def test_tcp_metadata_and_sensitive_payload_are_not_saved(self):
        packet = (
            IP(src="192.0.2.10", dst="198.51.100.20")
            / TCP(sport=51515, dport=443, flags="S")
            / Raw(load=b"payload-must-not-appear")
        )
        packet.time = 1_700_000_000

        record = packet_to_record(packet, 7)

        self.assertEqual(record.packet_number, 7)
        self.assertEqual(record.source_ip, "192.0.2.10")
        self.assertEqual(record.destination_ip, "198.51.100.20")
        self.assertEqual(record.protocol, "TCP")
        self.assertEqual(record.source_port, "51515")
        self.assertEqual(record.destination_port, "443")
        self.assertEqual(record.tcp_flags, "S")
        self.assertEqual(record.packet_length, len(packet))
        self.assertNotIn("payload-must-not-appear", repr(record))

        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "packets.csv"
            write_csv([record], output)
            saved_csv = output.read_text(encoding="utf-8")
            self.assertNotIn("payload-must-not-appear", saved_csv)
            self.assertEqual(next(csv.reader(saved_csv.splitlines())), list(CSV_FIELDS))

    def test_udp_metadata(self):
        packet = IP(src="192.0.2.1", dst="192.0.2.2") / UDP(sport=1234, dport=53)

        record = packet_to_record(packet, 1)

        self.assertEqual(record.protocol, "UDP")
        self.assertEqual(record.source_port, "1234")
        self.assertEqual(record.destination_port, "53")
        self.assertEqual(record.tcp_flags, "")

    def test_icmp_has_no_ports_or_tcp_flags(self):
        packet = IP(src="192.0.2.1", dst="192.0.2.2") / ICMP()

        record = packet_to_record(packet, 1)

        self.assertEqual(record.protocol, "ICMP")
        self.assertEqual(record.source_port, "")
        self.assertEqual(record.destination_port, "")
        self.assertEqual(record.tcp_flags, "")


if __name__ == "__main__":
    unittest.main()
