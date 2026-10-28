# Project Report: Basic Network Sniffer Using Python

## Aim

To build a beginner-friendly Python program that captures a small, time-limited number of network packets from an authorized interface and reports basic packet metadata without collecting payload contents.

## Objectives

- Use Python and Scapy to capture packets from the user's own computer or an explicitly authorized test network.
- Display packet number, timestamp, source and destination IP addresses, protocol, source and destination ports, packet length, and TCP flags.
- Save only those metadata fields to a CSV file.
- Keep capture bounded by both a maximum packet count and a timeout.
- Handle missing Scapy, common Windows Npcap/adapter errors, permission errors, and CSV file errors with useful messages.
- Verify parsing and CSV output offline using constructed sample packets.

## Tools

- Python 3.10 or newer
- Scapy (installed using `requirements.txt`)
- Npcap on Windows for live packet capture
- Visual Studio Code and its Python extension
- Python `unittest` for automated offline tests

## Methodology

1. Install Python, VS Code, Scapy, and (for live Windows capture) Npcap.
2. Convert each observed packet into a fixed metadata record using its protocol headers, timestamp, and total length.
3. Do not examine or serialize the packet payload. Write only the defined metadata columns to CSV.
4. Restrict live capture using a positive packet-count limit and a positive timeout.
5. Test packet conversion and CSV output using generated TCP, UDP, and ICMP sample packets; do not require live network traffic for tests.

## Implementation

`sniffer.py` contains argument validation, packet metadata conversion, terminal formatting, bounded Scapy capture, CSV writing, and error messages. The default capture limit is 20 packets or 30 seconds. `requirements.txt` declares Scapy. `tests/test_sniffer.py` checks protocol metadata and that a test payload containing a password-like marker is absent from both the record and CSV. `README.md` provides Windows/VS Code setup and safe demonstration instructions.

## Actual test results

**Not run in the project-generation environment.** No test result is claimed here. To produce actual results on the target computer, open the project in VS Code and run:

```powershell
py -m pip install -r requirements.txt
py -m unittest discover -s tests -v
```

Replace this section with the exact command output after running it. Tests are offline; they do not need Npcap or administrator permissions.

## Limitations

- Live capture requires a compatible interface, Scapy, Npcap on Windows, and sufficient permissions.
- Network interfaces and drivers may expose different packet sets; the program can legitimately capture zero packets.
- Scapy's normal `sniff()` receives selected packet bytes transiently in memory before the callback extracts metadata. The program does not parse, print, or write payload bytes and does not retain packet objects; however, it cannot guarantee payload bytes never enter memory. Do not use it where policy requires strict header-only acquisition unless the capture backend is separately configured to truncate packets.
- Ports are shown only for TCP and UDP. Other protocols have blank port fields.
- TCP flags are blank for non-TCP packets.
- This is a teaching tool, not a full protocol analyzer, intrusion detection system, or forensic tool.
- Packet metadata (including addresses and timestamps) can still be sensitive. Protect the CSV and screenshots and delete them when no longer needed.
- Capture only traffic on systems and networks for which you have explicit authorization.

## Conclusion

The project provides a bounded packet-metadata capture workflow and offline tests suitable for a beginner demonstration. Its design intentionally excludes payload collection. The user should run the documented tests and a short authorized capture on their own Windows computer to obtain local test results and screenshots.
