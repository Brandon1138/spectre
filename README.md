# Spectre: Network Scanner

Spectre is a Python-based network scanning utility that leverages `python-nmap` to perform port scans. It provides both standard and stealth scanning capabilities, asynchronous operations, an interactive Rich-based UI, robust logging, **and a new vulnerability checker** for detecting outdated or at-risk software versions.

---

## Table of Contents

- [Features](#features)
- [Architecture & Design](#architecture--design)
- [Installation](#installation)
- [Usage](#usage)
    - [Basic Scan](#basic-scan)
    - [Stealth Scan](#stealth-scan)
    - [Vulnerability Checks](#vulnerability-checks)
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
    Utilizes Python’s `asyncio` to execute multiple scans concurrently, reducing overall scan time.
    
- **Rich-based UI**  
    Provides a user-friendly command-line interface with progress bars and tables for real-time feedback.
    
- **Robust Logging**  
    Scan results are logged in multiple formats:
    
    - **JSON** for machine readability.
    - **Plaintext** for quick reviews.
    - **Markdown** for formatted documentation (ideal for tools like Obsidian)
	
- **Vulnerability Checker**  
    After scans complete, Spectre can inspect the discovered service versions and compare them to known stable baselines, automatically flagging any outdated software (e.g., OpenSSH, Apache, MySQL, NGINX). This streamlines identification of potential security risks.
    

---

## Architecture & Design

Spectre is organized into modular components:

- **Scanning Modules:**
    
    - `nmap_scanner.py` – Implements the basic scanning functionality (port, OS, and service detection).
    - `stealth_scanner.py` – Extends the basic scanner with stealth options.
    - **New**: `vulnerability_checker.py` – Parses discovered service versions and checks them against known stable or secure baselines.
	
- **User Interface:**
    
    - `ui.py` – A Rich-based UI that handles user input, displays progress, and shows results in tabular form.
	
- **Logging:**
    
    - `logger.py` – Contains the `ScanLogger` class to log outputs in JSON, plaintext, and Markdown.
	
- **Asynchronous Execution:**
    
    - Scanning methods are wrapped in asynchronous calls to handle multiple targets concurrently.

For deeper technical context, see the [Architectural Decision Record](./docs/Architectural%20Decision%20Record.md) and Body Documentation.

---

## Installation

1. **Clone the Repository:**
	
    `git clone https://github.com/Brandon1138/spectre.git cd spectre`
    
2. **Install Dependencies:**
    
    `pip install -r requirements.txt`
    
    Dependencies include:
    
    - `python-nmap`
    - `rich`
    - `asyncio` (built into Python 3.7+)
    - `logging` (built into Python)
    - ... and any additional packages listed in `requirements.txt`.
	
3. **Verify nmap Installation (Optional):**
    
    `nmap -h`
    
    Ensure `nmap` is installed and accessible from your system’s PATH.
    

---

## Usage

### Basic Scan

Run the UI module to start a standard scan:

`python ui.py`

When prompted, enter one or more target IP addresses (comma-separated), e.g. `192.168.1.10` or `192.168.1.10, 192.168.1.20`.

### Stealth Scan

To perform a stealth scan with advanced options, modify the scanner initialization in your code (or create a separate UI option) using the `StealthNmapScanner` from `stealth_scanner.py`. For example:


`from stealth_scanner import StealthNmapScanner  

 `scanner = StealthNmapScanner(decoy="RND:10", fragmentation=True, timing=1) 
 `result = scanner.scan_target("127.0.0.1")`
  `if result:`
	`print(result)`

### Vulnerability Checks

Spectre’s built-in **vulnerability_checker.py** compares discovered service versions against known thresholds for common software (e.g., OpenSSH, Apache, MySQL, NGINX).

Here’s a basic example of how you might integrate vulnerability checks:

`from vulnerability_checker import check_for_outdated_services from nmap_scanner import NmapScanner  

`scanner = NmapScanner()` 
`result = scanner.scan_target("127.0.0.1")` 
`if result:`   
	`tcp_data = result.get("tcp", {})`  
	`alerts = check_for_outdated_services(tcp_data)`    
	`if alerts:` 
		`print("Potential Vulnerabilities Detected:")`
		`for alert in alerts:`
			`print(f"- {alert}")`     
	`else:`        
		`print("No vulnerabilities detected.")`

This enables quick identification of outdated or at-risk services within the scanning workflow.

---

## Modules Overview

- **nmap_scanner.py**  
    Contains the `NmapScanner` class for standard port scanning. It provides both synchronous and asynchronous methods and includes functionality to save scan results in JSON format.
    
- **stealth_scanner.py**  
    Inherits from `NmapScanner` and adds stealth functionalities such as decoy scanning, fragmentation, idle scanning, and other advanced options.
    
- **vulnerability_checker.py**  
    Examines service data from scans, parses version strings, and flags instances of outdated or potentially vulnerable software based on predefined thresholds.
    
- **logger.py**  
    Implements the `ScanLogger` class, which logs scan results to a date-based directory structure in JSON, plaintext, and Markdown formats.
    
- **ui.py**  
    A user-friendly interface built with Rich. It prompts for target IP(s), displays a progress bar during scans, shows results in a formatted table, and logs outputs using the `ScanLogger` module.
    

---

## Documentation & ADRs

For comprehensive design details and rationale, refer to:

- **Architectural Decision Record (ADR)**  
    Includes decisions on python-nmap adoption, stealth integration, logging/reporting strategies, asynchronous scanning, vulnerability analysis, and more (ADR-001 to ADR-008).
    
- **Body Documentation**  
    Offers detailed feature descriptions, implementation notes, and technical discussions.
    
- **Code Walkthrough**  
    In-depth exploration of key modules and their interdependencies.
    

These documents collectively provide a thorough understanding of Spectre’s design and capabilities.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with clear, descriptive messages.
4. Submit a pull request for review.
5. For major changes, please open an issue first to discuss your ideas.