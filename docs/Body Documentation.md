# Network Scanner: What It Does

The Spectre Network Scanner is a tool designed to check which devices are connected to a network and determine which services they are running. It helps users understand their network security by scanning for open ports, which are like virtual doors that allow communication between devices.

This tool can be used for basic scanning to see what is active on a network, as well as for more advanced scanning that tries to avoid detection by security systems. It is useful for IT professionals, cybersecurity enthusiasts, and anyone who wants to assess network security.

---

## How the Scanner Works

### 1. Standard Network Scanning

- The scanner quickly checks a network for devices and identifies open ports.
    
- It uses a reliable scanning method that is widely recognized and trusted.
    
- The results are presented in an easy-to-read format.
    

### 2. Stealth Scanning

Some networks have security measures that try to block or detect scans. The stealth scanning feature helps avoid detection by using techniques such as:

- **Decoy Scans** – Pretending the scan is coming from multiple sources.
    
- **Fragmentation** – Breaking the scan into smaller pieces to go unnoticed.
    
- **Idle Scans** – Hiding behind another device while scanning.
    
- **Timing Adjustments** – Controlling how fast the scan happens to reduce suspicion.
    

These methods make it harder for security systems to detect that a scan is taking place.

---

## Keeping a Record of Scans (Logging)

The scanner saves results so users can review them later. It records scan details in three formats:

- **Plain Text** – A simple list of results for easy reading.
    
- **JSON** – A structured format that can be used by other programs.
    
- **Markdown** – A formatted document that can be opened in note-taking apps.
    

Each scan result is saved in a folder named with the current date, making it easy to organize past scans.

---

## Interactive Interface (UI)

Instead of typing complicated commands, users can interact with the scanner using a simple interface. The UI provides:

- A text box to enter the devices to scan.
    
- A progress bar to show the scan’s progress.
    
- A table displaying results in an organized way.
    
- Automatic logging of results for later review.
    

---

## Faster Scanning with Multiple Tasks (Asynchronous Scanning)

If multiple devices need to be scanned at once, the scanner can run multiple tasks simultaneously. This reduces waiting time and provides results more quickly. Instead of scanning one device at a time, the scanner handles many devices at once, making it much more efficient.

---

## Error Handling & Stability

If something goes wrong during a scan, the scanner logs the issue instead of stopping abruptly. It keeps track of:

- Errors that occur during scanning.
    
- Devices that didn’t respond.
    
- Any unusual network activity detected during the scan.
    

This makes troubleshooting easier and ensures the tool remains reliable over time.

---

## Summary

- The Spectre Network Scanner checks which devices and services are active on a network.
    
- It can perform both standard and stealth scans.
    
- Scan results are saved for review.
    
- The interactive interface makes it easy to use.
    
- Multiple scans can run at the same time to speed up results.
    
- The tool is designed to be stable and reliable, even if something goes wrong.
    

This tool is ideal for anyone who wants to explore or secure their network with minimal technical knowledge.

---

## Annex: Technical Overview

### Network Scanner: python-nmap Implementation

- Uses `python-nmap` to execute TCP/UDP scans efficiently.
    
- Processes scan results and stores them in JSON format.
    
- Designed for modular expansion with future features like stealth scanning.
    

### Network Scanner: Stealth Enhancements with python-nmap

A specialized scanner subclass adds stealth options:

- **Decoy Scans** – Use random IPs or user-defined lists.
    
- **Fragmentation** – Break packets into small segments.
    
- **Idle Scans** – Route scans via a zombie host.
    
- **Timing Adjustments** – Change scan speeds.
    
- **Source Port Spoofing** – Impersonate well-known ports.
    
- **TTL Variation** – Mimic different OS behaviors.
    

These options are combined into a command string passed to nmap for execution.

### Logging & Reporting

- ScanLogger records results in three formats: JSON, plain text, and Markdown.
    
- Logs are stored in a date-based directory structure for easy organization.
    

### UI Integration

- The UI module, `ui.py`, uses the `Rich` library for an interactive experience.
    
- Features include:
    
    - User prompt for target IP(s).
        
    - Progress bar during scanning.
        
    - Tabular display of scan results.
        
    - Integration with ScanLogger for persistent logs.
        

### Asynchronous Scanning

- The scanner supports asynchronous operations.
    
- `async_scan_target` wraps the blocking `scan_target` method using `asyncio`.
    
- Multiple scans can be run in parallel for efficiency.
    

### Enhanced Error Handling & Logging

- Uses Python’s logging module to replace print statements.
    
- Logs key events, errors, and exceptions for easier debugging.
    
- Ensures scan failures and anomalies are recorded systematically.