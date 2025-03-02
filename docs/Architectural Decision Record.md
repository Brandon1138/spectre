# ADR-001: Use python‑nmap for the Network Scanner
## Status:
Accepted
## Context:
We require a scanning tool that is quick to implement and easy to integrate. python‑nmap offers a direct wrapper around nmap commands, enabling standard scan types with minimal overhead.
## Decision:
Adopt python‑nmap as the core for initial network scanning. This choice balances ease of use against the need for low‑level control (reserved for future scapy integration).
## Consequences:
• Rapid prototyping with standard scan types.  
• Limited raw packet control compared to scapy.  
• Future modules may augment functionality with more granular packet handling.
---
# ADR-002: Stealth Enhancements for the Network Scanner
## Status: 
 Accepted
## Context:
Network scanning risks detection. To reduce this risk, stealth features—such as decoy scans, packet fragmentation, idle scanning, and timing adjustments—must be integrated.
## Decision:
Implement a subclass of the base scanner that allows for optional stealth parameters. These parameters map directly to nmap command-line flags. This provides modularity while keeping our core code intact.
## Consequences: 
• Simplifies the addition of stealth features as optional enhancements.
• Enables quick toggling between standard and stealth scans.
• May require elevated privileges for some options.
---
# ADR-003: Logging & Reporting for the Network Scanner
## Status:
Accepted
## Context:
Accurate logging of scan results aids analysis and troubleshooting. Two formats are needed:
- JSON for machine readability.
- Plain text (and optionally Markdown/HTML) for quick review.
## Decision:
Implement a dedicated logging module to store scan results in a date-based directory structure. The logger will offer methods for:
- JSON logs.
- Plain text logs.
- Markdown exports (as an optional presentation format).
## Consequences:
• Facilitates both automated analysis and human review.  
• Provides a modular component that can be extended or replaced as needed.
---
# ADR-004: Rich-based UI for the Network Scanner
## Status:
Accepted
## Context: 
A real‑time UI improves usability by providing progress feedback and an interactive view of scan results. Curses is unavailable on Windows. Rich offers a modern, cross-platform alternative with progress bars and formatted tables. 
## Decision:
Integrate a UI module using the Rich library. The UI displays a progress indicator during scanning, accepts user input for target selection, and presents results in a table. Logging remains decoupled.
## Consequences:
• Enhanced user experience and clarity during scanning. 
• Modular UI that can later be swapped for a GUI if needed.
---
# ADR-005: Asynchronous Scanning and Concurrency
## Status:
Accepted
## Context:
The current scanner implementation blocks on each target due to synchronous nmap calls. As network scans can be time‐consuming, we need to enable asynchronous scanning to reduce total wait time when scanning multiple targets concurrently.
## Decision:
- Refactor blocking scanning methods (e.g., `scan_target`) into asynchronous wrappers using Python’s `asyncio`.
- Use `asyncio.get_running_loop().run_in_executor` (or `asyncio.to_thread`) to offload blocking I/O operations.
- Update the UI to support concurrent scanning via `asyncio.gather`.
## Consequences:
- Improved performance when scanning multiple targets.
- The scanner code will need careful exception handling (see ADR-006).
---
# ADR-006: Robust Error Handling and Unified Logging
## Status:
Accepted
## Context:
Our current implementation uses basic print statements and minimal exception management. For better troubleshooting and production reliability, we need to integrate Python’s built‑in logging module across all components.
## Decision:
- Replace `print` statements with logging calls (`logging.info`, `logging.error`, and `logging.exception`).
- Set up a common logging configuration (e.g., logging level, formatter, and output handlers).
- Enhance exception handling in scanning methods to capture and log detailed error information.
## Consequences:
- Consistent and centralized logging across modules.
- Easier debugging and post-mortem analysis via log files.
---
# ADR-007: Advanced Service/OS Detection Integration
## Status: 
Accepted
## Context:
The initial scanning implementation using python‑nmap provided basic port detection. As user requirements evolved, there was a need to collect richer target data—specifically:
- Detailed OS fingerprinting using Nmap’s `-O` flag.
- Service and version detection using Nmap’s `-sV` flag. 
This need extended to all scan modes, including stealth operations where such data was previously inconsistent.
## Decision: 
- **Enhance Base Scanner:** Update the default scan arguments in `nmap_scanner.py` to include `-sV -O`, ensuring all scans retrieve OS and service version details. 
- **Stealth Scanner Integration:** Modify `stealth_scanner.py` so that, regardless of stealth-specific options, `-sV -O` are always appended. This guarantees that even stealth scans yield enriched detection data. 
## Consequences:
- **Uniform Data Collection:** Both standard and stealth scans now produce comprehensive data sets, reducing ambiguity in scan results.
- **Enhanced Reporting:** Operators receive more actionable information, such as OS guesses and service version details, which improves downstream analysis.
- **Maintenance:** Future modifications to scan parameters can be centrally managed, but require periodic review to align with evolving Nmap capabilities.
---
# ADR-008: Vulnerability Analysis Integration
## Status:
Accepted 
## Context:
Operators need to quickly identify potentially outdated or vulnerable software running on scanned targets. Basic version detection alone does not suffice for actionable intelligence. With evolving software releases, comparing discovered versions against current stable baselines is essential for security assessments.
## Decision:
* **Implement Vulnerability Checker Module:** Develop a new module (`vulnerability_checker.py`) that:
	- Parses version strings using regex. 
	- Compares parsed version tuples against predetermined thresholds.
	- Flags software running versions below the current stable baseline.
- **Defined Thresholds:** As of March 2, 2025, the thresholds are set as follows:
	- **OpenSSH:** 9.9p2 (threshold as (9, 9, 2))
	- **Apache HTTP Server:** 2.4.57 (threshold as (2, 4, 57))
	- **MySQL:** 8.0.34 (threshold as (8, 0, 34))
	- **NGINX:** 1.23.3 (threshold as (1, 23, 3))
- **Integration:** Integrate vulnerability analysis into the UI and logging workflow so that alerts are displayed and recorded if outdated versions are detected. 
## Consequences:
- **Actionable Intelligence:** Provides immediate alerts on potential vulnerabilities, enabling faster remediation.
- **Extensibility:** The module is designed to be extended easily with additional software checks or dynamic threshold updates.
 * **Operational Overhead:** Maintaining current thresholds requires periodic updates aligned with software release cycles.