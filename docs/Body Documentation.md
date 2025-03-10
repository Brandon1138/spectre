# Network Scanner:

The Spectre network scanner utilises python‑nmap to perform comprehensive port scans and gather rich target data. This updated implementation not only provides basic scanning functionality but also integrates advanced OS fingerprinting, detailed service/version detection, and vulnerability analysis to flag outdated software. The document below outlines each component, its evolution, and how the new features are integrated.

---

## 1. Basic Scanning with python‑nmap

The core scanning module (`nmap_scanner.py`) leverages python‑nmap to conduct TCP scans over a specified port range. The original implementation focused on port state and basic service detection. With the recent updates, the default scan arguments now include:
- **`-sV`**: For detailed service/version detection.
- **`-O`**: For OS fingerprinting.

This enhancement ensures every scan returns an enriched data set with OS guesses and service version details.

---

## 2. Stealth Scanning Enhancements

Stealth scanning, implemented in `stealth_scanner.py`, allows the scanner to operate with low detection risk. Previously, stealth scans were limited to decoys, fragmentation, idle scanning, and timing adjustments. In this update, stealth scanning has been integrated with the advanced detection features:
- Regardless of the stealth options (e.g., decoy, fragmentation), the scanner appends the `-sV -O` flags.
- This guarantees that stealth scans produce the same rich output as standard scans, unifying data collection across modes.

---

## 3. Vulnerability Analysis Integration

A new module, `vulnerability_checker.py`, has been introduced to enhance operational intelligence:
- **Version Parsing:**  
  The module utilises regex to extract numeric components from version strings, converting them into tuples for comparison.
- **Threshold Comparison:**  
  Parsed versions are compared against predefined thresholds representing the latest stable releases as of March 2, 2025:
  - **OpenSSH:** Latest stable is 9.9p2 (threshold tuple: `(9, 9, 2)`).
  - **Apache HTTP Server:** Latest stable is 2.4.57 (threshold tuple: `(2, 4, 57)`).
  - **MySQL:** Latest stable is 8.0.34 (threshold tuple: `(8, 0, 34)`).
  - **NGINX:** Latest stable is 1.23.3 (threshold tuple: `(1, 23, 3)`).
- **Alerting:**  
  Services running versions below these thresholds are flagged as outdated. Alerts are then integrated into the UI and logged for review, giving operators actionable intelligence to prioritise remediation.

---

## 4. Asynchronous Scanning & Logging

To handle multiple targets efficiently, the scanner wraps the blocking Nmap call into an asynchronous method using Python’s `asyncio`. This improvement drastically reduces overall scan time when multiple targets are provided.  
Scan results—including the extended OS and service details—are passed to the logging module (`logger.py`), which stores output in:
- **JSON:** For machine-readable post-scan analysis.
- **Plaintext:** For quick manual review.
- **Markdown:** For well-formatted documentation (ideal for knowledge bases like Obsidian).

The unified logging strategy ensures that all relevant data, including vulnerability alerts, is captured with consistent formatting and file organisation.

---

## 5. User Interface Enhancements

The Rich-based UI (`ui.py`) has been updated to:
- Prompt for target IP(s) and provide progress feedback during asynchronous scanning.
- Display results in a detailed table that now includes columns for OS detection and service version details.
- Highlight vulnerability alerts generated by the vulnerability checker.
- Log enriched scan results automatically, ensuring that all extended data is available for later review.

---

## 6. Future Considerations

- **Maintenance:**  
  Regular updates will be required to adjust vulnerability thresholds as new stable versions are released.
- **Extensibility:**  
  The design is modular, enabling further enhancements such as dynamic threshold updates from external vulnerability feeds or integration with additional scanning protocols.
- **Documentation Updates:**  
  Further documentation, including a full code walkthrough and ADR revisions, has been maintained in the respective files to ensure clarity on design decisions.