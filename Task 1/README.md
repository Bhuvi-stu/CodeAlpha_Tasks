# Basic Network Sniffer Using Python

A small learning project that uses Scapy to capture a **limited number of packet headers** from your own computer or a network you are explicitly authorized to test. It prints and saves metadata only. It does not decode, print, or store payload contents, passwords, credentials, or message bodies.

**Important privacy detail:** Scapy's normal live capture receives each selected packet in memory so it can parse the headers. This program reads only header fields and length, uses `store=False`, and writes no payload bytes to the terminal or CSV; packet objects are not retained after processing. If your rules require that payload bytes never enter memory at all, do not use this basic `sniff()` implementation—use an approved capture setup configured to truncate packets to headers, or test only with generated sample packets.

## Project files

Save these files in one folder, for example `C:\Users\YourName\Desktop\BasicNetworkSniffer`:

```text
BasicNetworkSniffer\
|-- sniffer.py
|-- requirements.txt
|-- README.md
|-- REPORT.md
|-- setup.bat
|-- run.bat
`-- tests\
    `-- test_sniffer.py
```

## Easiest way to run on a Windows laptop

Each laptop needs Python 3.10 or newer. For live capture it also needs Npcap. Keep the project folder together when copying it to another computer.

1. On the laptop, install Python from [python.org](https://www.python.org/downloads/) and select **Add Python to PATH** during setup.
2. For live capture, install Npcap from [npcap.com](https://npcap.com/).
3. Open the copied project folder in File Explorer and double-click `setup.bat`. This creates a private `.venv` folder inside the project and installs Scapy. Run setup once on each laptop; the `.venv` is local to that computer and should not be copied between computers.
4. Double-click `run.bat` to capture up to 10 packets for at most 15 seconds. The CSV report is saved as `captured_packets.csv` in the project folder.

Alternatively, open the folder in VS Code and double-click `setup.bat` from File Explorer once, then use the VS Code terminal:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe sniffer.py --count 10 --timeout 15
```

The setup and run batch files are for Windows. Copying the folder does not install Python or Npcap on another laptop; those prerequisites must be installed there too. Capture only your own or explicitly authorized traffic.

### Alternative: run with PowerShell commands

If you do not want to use the `.bat` files, open the project folder in VS Code, choose **Terminal > New Terminal**, and run these commands from the project folder.

Run these **two setup commands once on each laptop**:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Then use this command whenever you want to run a short live capture:

```powershell
.\.venv\Scripts\python.exe sniffer.py --count 10 --timeout 15
```

The CSV is saved as `captured_packets.csv` in the project folder. To run the offline tests instead:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Install Python 3.10 or newer and Npcap on each laptop before live capture. Capture only your own or explicitly authorized traffic.

## Requirements

- Windows 10 or 11
- Python 3.10 or newer, installed from [python.org](https://www.python.org/downloads/). During setup, select **Add python.exe to PATH**.
- Visual Studio Code and its Microsoft Python extension
- Npcap for live capture on Windows: install it from [npcap.com](https://npcap.com/). Use the default installation options and allow the capture driver to be installed.

## Install and test in VS Code

1. Create a project folder and save each file above in the matching location. In VS Code, choose **File > Open Folder...** and open that project folder.
2. Open **Terminal > New Terminal**. Check that the prompt is in the project folder.
3. Check Python is available:

   ```powershell
   py --version
   ```

   If `py` is not recognized, reinstall Python with the PATH option selected, then reopen VS Code.
4. Install Scapy:

   ```powershell
   py -m pip install -r requirements.txt
   ```

5. In VS Code, press **Ctrl+Shift+P**, choose **Python: Select Interpreter**, and select the Python installation where Scapy was installed.
6. Run the offline tests; they construct sample packets and do not start a network capture:

   ```powershell
   py -m unittest discover -s tests -v
   ```

7. For the live capture steps below, install Npcap first. If Windows blocks packet capture, close VS Code, reopen it using **Run as administrator**, and try again.

## Run a safe live capture

Only capture traffic from your own computer or a network you have explicit permission to monitor. Do not capture on public, workplace, school, or other people's networks unless you have authorization.

Run from the VS Code terminal:

```powershell
py sniffer.py --count 10 --timeout 15
```

This stops after at most 10 packets or 15 seconds, whichever comes first. The defaults are also bounded: at most 20 packets or 30 seconds. The packet summary appears in the terminal. The CSV is saved as `captured_packets.csv` in the terminal's current folder (normally the project folder).

To choose another CSV location:

```powershell
py sniffer.py --count 10 --timeout 15 --output .\demo_packets.csv
```

To specify a network interface, first inspect Scapy's interface names:

```powershell
py -c "from scapy.all import show_interfaces; show_interfaces()"
```

Then pass the exact interface name shown:

```powershell
py sniffer.py --interface "Wi-Fi" --count 10 --timeout 15
```

If no packets arrive before the timeout, an empty CSV containing the column headings is still written. To produce benign traffic on your own computer, open another terminal and visit a simple public website or run `ping 1.1.1.1`; only do this where permitted. The sniffer still observes headers only, and packet visibility depends on your interface and network.

## Terminal fields

| Field | Simple meaning |
|---|---|
| No. | Packet's sequence number in this capture |
| Timestamp | Local date and time when Scapy timestamped the packet |
| Source IP | Network address that sent the packet |
| Destination IP | Network address the packet is going to |
| Protocol | Header type identified, such as TCP, UDP, ICMP, or ARP |
| Src | Source port for TCP/UDP; `-` when not applicable |
| Dst | Destination port for TCP/UDP; `-` when not applicable |
| Length | Total packet size in bytes |
| TCP flags | TCP control flags, such as `S` (start connection) or `SA` (start/acknowledge); `-` when not TCP |

The CSV uses the full column names `source_port`, `destination_port`, `packet_length`, and `tcp_flags`.

## Example terminal output

The following is an **illustrative format example**, not a result from your computer:

```text
 No.  Timestamp                         Source IP                               Destination IP                          Protocol  Src  Dst  Length  TCP flags
------------------------------------------------------------------------------------------------------------------------------------------------------
   1  2026-10-19T19:30:00.123456+05:30  192.0.2.10                              198.51.100.20                            TCP      51515    443      60  S

Captured 1 packet(s). Metadata CSV saved to: C:\...\BasicNetworkSniffer\captured_packets.csv
```

The addresses in this example are documentation-only placeholders. Actual output depends on your computer and network.

## Error handling

- **Scapy missing:** install dependencies with `py -m pip install -r requirements.txt`.
- **Npcap or adapter error:** install/repair Npcap, ensure its capture driver is enabled, and use the right interface.
- **Permission denied:** reopen VS Code as administrator for the authorized capture.
- **No packets seen:** confirm the selected interface is active and generate permitted traffic during the short capture window.
- **CSV write error:** choose an output path in a folder where you have write permission.

## Screenshot demonstration

1. Run the offline test command and capture a screenshot of the test summary.
2. Start a brief authorized live capture using `--count 10 --timeout 15`, while generating benign traffic on your own computer.
3. Capture the terminal showing the packet metadata and the final CSV path.
4. Open the CSV in VS Code or a spreadsheet and capture the header row and metadata rows. Check that it contains no payload column or message text.
5. Avoid including unrelated personal information in screenshots. Clearly label any example data as sample data.

## GitHub Copilot workflow

Use Copilot Chat in VS Code to understand or debug the project one file at a time. Example prompts:

- “Explain `sniffer.py` line by line. Confirm it only stores packet metadata and never reads payload bytes.”
- “Explain what each test in `tests/test_sniffer.py` verifies.”
- “I ran `py -m unittest discover -s tests -v` and got this error: [paste the error]. Help me diagnose it without adding live packet capture to the tests.”

Run the tests again after making any changes. Do not use Copilot-generated code to capture traffic without authorization.

See [REPORT.md](REPORT.md) for the project report and recorded test results.
