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

# ADR-005: Asynchronous Scanning and Concurrency
## Status:
Proposed
## Context:
The current scanner implementation blocks on each target due to synchronous nmap calls. As network scans can be time‐consuming, we need to enable asynchronous scanning to reduce total wait time when scanning multiple targets concurrently.
## Decision:
- Refactor blocking scanning methods (e.g., `scan_target`) into asynchronous wrappers using Python’s `asyncio`.
- Use `asyncio.get_running_loop().run_in_executor` (or `asyncio.to_thread`) to offload blocking I/O operations.
- Update the UI to support concurrent scanning via `asyncio.gather`.
## Consequences:
- Improved performance when scanning multiple targets.
- The scanner code will need careful exception handling (see ADR-006).

# ADR-006: Robust Error Handling and Unified Logging

## Status:
Proposed

## Context:
Our current implementation uses basic print statements and minimal exception management. For better troubleshooting and production reliability, we need to integrate Python’s built‑in logging module across all components.

## Decision:
- Replace `print` statements with logging calls (`logging.info`, `logging.error`, and `logging.exception`).
- Set up a common logging configuration (e.g., logging level, formatter, and output handlers).
- Enhance exception handling in scanning methods to capture and log detailed error information.

## Consequences:
- Consistent and centralized logging across modules.
- Easier debugging and post-mortem analysis via log files.