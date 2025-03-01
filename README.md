# Spectre: Network Scanner

Spectre is a Python-based network scanning utility that leverages `python-nmap` to perform port scans. It provides both standard and stealth scanning capabilities, asynchronous operations, and an interactive, Rich-based UI. The tool also includes robust logging mechanisms for detailed post-scan analysis.

---

## Table of Contents

- [Features](#features)
- [Architecture & Design](#architecture--design)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Scan](#basic-scan)
  - [Stealth Scan](#stealth-scan)
- [Modules Overview](#modules-overview)
- [Documentation & ADRs](#documentation--adrs)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Standard Scanning**  
  Performs TCP/UDP scans on target IP(s) over configurable port ranges using `python-nmap`.

- **Stealth Scanning**  
  Supports advanced stealth options including:
  - Decoy scans (random or user-specified decoys)
  - Packet fragmentation
  - Idle scanning using a zombie host
  - Timing adjustments (e.g., using the `-T` option)
  - Source port spoofing and TTL manipulation

- **Asynchronous Scanning**  
  Utilizes Python's `asyncio` to execute multiple scans concurrently, reducing overall scan time.

- **Rich-based UI**  
  Provides a user-friendly command-line interface with progress bars and tables for real-time feedback.

- **Robust Logging**  
  Scan results are logged in multiple formats:
  - **JSON** for machine readability.
  - **Plaintext** for quick reviews.
  - **Markdown** for formatted documentation (ideal for tools like Obsidian).

---

## Architecture & Design

Spectre is organized into modular components:
- **Scanning Modules:**  
  - `nmap_scanner.py` – Implements the basic scanning functionality.
  - `stealth_scanner.py` – Extends the basic scanner with stealth options.
  
- **User Interface:**  
  - `ui.py` – A Rich-based UI that handles user input, displays progress, and shows results in tabular form.

- **Logging:**  
  - `logger.py` – Contains the `ScanLogger` class to log outputs in JSON, plaintext, and Markdown.

- **Asynchronous Execution:**  
  - Scanning methods are wrapped in asynchronous calls to handle multiple targets concurrently.

For deeper technical context, see the [Architectural Decision Record](./docs/Architectural%20Decision%20Record.md) and [Code Walkthrough](./docs/Code%20Walkthrough.md).

---

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/Brandon1138/spectre.git
    cd spectre
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
   Dependencies include:
   - `python-nmap`
   - `rich`
   - `asyncio` (built into Python 3.7+)
   - `logging` (built into Python)
   - ... and any additional packages listed in `requirements.txt`.

3. **Verify nmap Installation (Optional):**
    ```bash
    nmap -h
    

---

## Usage

### Basic Scan

Run the UI module to start a standard scan:
```bash
python ui.py
When prompted, enter one or more target IP addresses (comma-separated), e.g., 192.168.1.10 or 192.168.1.10, 192.168.1.20.
```


### Stealth Scan

To perform a stealth scan with advanced options, modify the scanner initialization in your code (or create a separate UI option) using the `StealthNmapScanner` from `stealth_scanner.py`. For example:
```python
from stealth_scanner import StealthNmapScanner

# Instantiate with stealth options: decoy, fragmentation, timing, etc.
scanner = StealthNmapScanner(decoy="RND:10", fragmentation=True, timing=1)
result = scanner.scan_target("127.0.0.1")
if result:
    print(result)
```

---

### Modules Overview
- nmap_scanner.py: 
Contains the NmapScanner class for standard port scanning. It provides both synchronous and asynchronous scanning methods and includes functionality to save scan results in JSON format.


- stealth_scanner.py:
Inherits from NmapScanner and adds stealth functionalities such as decoy scanning, fragmentation, idle scanning, and other advanced options.


- logger.py:
Implements the ScanLogger class, which logs scan results to a date-based directory structure in JSON, plaintext, and Markdown formats.


- ui.py:
A user-friendly interface built with Rich. It prompts for target IP(s), displays a progress bar during scans, shows results in a formatted table, and logs outputs using the ScanLogger module.

---

### Documentation & ADRs
For comprehensive design details and rationale, refer to:

### Architectural Decision Record:
ADR-001 to ADR-006

### Body Documentation:
Detailed feature descriptions and implementation notes.

### Code Walkthrough:
An in-depth explanation of key modules and updates.
These documents provide context on decisions, logging strategies, and asynchronous scanning enhancements.

---

### Contributing
Contributions are welcome! To contribute:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Commit your changes with clear, descriptive messages.
- Submit a pull request for review.
- For any major changes, please open an issue first to discuss your ideas.