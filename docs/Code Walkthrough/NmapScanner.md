## File Overview

This module provides a class (`NmapScanner`) that leverages the `python-nmap` library to execute network scans. It includes both synchronous and asynchronous methods for scanning, as well as a helper method to save scan results to a JSON file. The module also sets up logging to capture runtime events and errors.

_(Reference: nmap_scanner)_

---

## Import Statements

`import nmap
`import json`
`import asyncio`
`import logging`

- **nmap**: Imports the `python-nmap` module, which provides a Python interface to the nmap tool.
- **json**: Used for serializing scan results into JSON format for saving or further processing.
- **asyncio**: Supports asynchronous operations, which is essential for running multiple scans concurrently.
- **logging**: Provides logging capabilities so that scan events and errors are recorded with timestamps and severity levels.

---

## Logging Configuration

`logging.basicConfig(     
	`level=logging.INFO,`     
	`format="%(asctime)s [%(levelname)s] %(message)s",`
	`handlers=[logging.StreamHandler()]` 
`)`

- **`logging.basicConfig`**: Sets up a common logging configuration for the module.
    - **`level=logging.INFO`**: Ensures that all messages at INFO level and above are logged.
    - **`format`**: Specifies the log message format, including the timestamp, log level, and message.
    - **`handlers`**: Uses a stream handler to print log messages to the console.

This configuration means that any logging calls within the module will output messages in a standardized, human-readable format.

---

## Class Definition: `NmapScanner`

The `NmapScanner` class encapsulates all scanning operations.

### Constructor: `__init__`

`def __init__(self, scan_arguments='-sS'):
	`# Initialise the python-nmap scanner`
	`self.nm = nmap.PortScanner()`
	`self.scan_arguments = scan_arguments`

- **Parameters**:
    - `scan_arguments`: A string with default value `'-sS'`, which represents a TCP SYN scan. This can be overridden if different scanning options are needed.

- **Functionality**:
    - **`self.nm = nmap.PortScanner()`**: Instantiates an nmap PortScanner object to interface with the nmap tool.
    - **`self.scan_arguments = scan_arguments`**: Saves the scan arguments for later use during the scan.

This initialization prepares the scanner with a default behavior that can be modified through parameters.

---

### Method: `scan_target`

`def scan_target(self, target, ports="1-1024"):     
`""" 
`Execute an nmap scan on the given target over specified ports.`
`Returns a dict with scan results.`    
`"""`     
	 `try:` 
		`self.nm.scan(target, ports, arguments=self.scan_arguments)`
		`return self.nm[target]`
	`except Exception as e:`
		`logging.exception("Scan error for target %s: %s", target, e)
		`return None`

- **Parameters**:
    - `target`: The IP address (or hostname) of the system to be scanned.
    - `ports`: A string specifying the port range to scan (default is `"1-1024"`).

- **Workflow**:
    - **`self.nm.scan(target, ports, arguments=self.scan_arguments)`**: Executes the scan using the preconfigured scanner. The `arguments` parameter allows passing custom nmap command-line flags.
    - **`return self.nm[target]`**: If the scan completes successfully, the method returns the scan results as a dictionary (extracted from the PortScanner object for the specific target).

- **Error Handling**:
    - The method uses a try-except block to catch any exceptions during the scan.
    - **`logging.exception(...)`**: Logs the error with a traceback, making it easier to debug scan failures.
    - Returns `None` if an error occurs.

This function encapsulates the core scanning logic and ensures that errors are handled gracefully.

---

### Asynchronous Method: `async_scan_target`

`async def async_scan_target(self, target, ports="1-1024"):
	`""" 
	`Asynchronously execute a scan on the given target.`
	`Offloads the blocking scan_target call to a background thread.` 
	`"""`
	`loop = asyncio.get_running_loop()     return await loop.run_in_executor(None, self.scan_target, target, ports)`

- **Purpose**: Provides an asynchronous interface to the synchronous `scan_target` method.

- **How It Works**:
    - **`loop = asyncio.get_running_loop()`**: Retrieves the current event loop.
    - **`loop.run_in_executor(...)`**: Offloads the blocking `scan_target` call to a background thread. This prevents the main event loop from being blocked by the network scan.
    - **`await`**: Waits for the scan to complete asynchronously.

- **Usage**: This method is ideal when scanning multiple targets concurrently, as it leverages Python’s `asyncio` framework.

By wrapping the blocking operation in an executor, the code efficiently handles I/O-bound operations.

---

### Method: `save_scan`

`def save_scan(self, target, filename, ports="1-1024"):
"""
Run a scan and save the results in JSON format.
"""
result = self.scan_target(target, ports)
if result:
	with open(filename, 'w') as f:
		json.dump(result, f, indent=2)
	logging.info("Scan results saved to %s", filename)
else:
	logging.error("No results to save for target %s.", target)`

- **Parameters**:
    - `target`: The target IP address/hostname to scan.
    - `filename`: The path of the file where scan results should be saved.
    - `ports`: The port range to scan (default is `"1-1024"`).
- **Workflow**:
    - **`result = self.scan_target(target, ports)`**: Executes a synchronous scan and stores the results.
    - **`if result:`**: Checks if the scan produced valid output.
        - **`with open(filename, 'w') as f:`**: Opens the specified file in write mode.
        - **`json.dump(result, f, indent=2)`**: Serializes the results dictionary into JSON with an indentation of 2 spaces for readability.
        - **`logging.info(...)`**: Logs a message indicating that the scan results were saved successfully.
    - **Error Case**:
        - If the scan result is `None`, an error message is logged stating that no results were available to save.

This helper method combines scanning and file I/O to simplify the process of persisting scan data.

---

## Main Block

python

Copy

`if __name__ == '__main__':
	`scanner = NmapScanner()`
	`# Run a simple synchronous test scan against localhost`
	`result = scanner.scan_target("127.0.0.1")`
	`if result:`
		`print(json.dumps(result, indent=2))`

- **Purpose**: Allows the module to be run as a standalone script for testing.
- **Steps**:
    - **`scanner = NmapScanner()`**: Creates an instance of the `NmapScanner` with the default scan arguments.
    - **`result = scanner.scan_target("127.0.0.1")`**: Executes a scan on the localhost.
    - **`if result:`**: Checks whether the scan was successful.
    - **`print(json.dumps(result, indent=2))`**: Pretty prints the scan result in JSON format to the console for quick verification.

This block is useful during development to verify that the scanning logic works correctly before integrating with other modules or a larger application.

---

## Summary

- **Initialization**: The module configures logging and instantiates a PortScanner object.
- **Synchronous Scanning**: `scan_target` performs a scan with error handling and returns a dictionary of results.
- **Asynchronous Scanning**: `async_scan_target` wraps the synchronous scan in an executor for non-blocking execution.
- **Result Saving**: `save_scan` combines scanning and file writing to store results in a human-readable JSON format.
- **Standalone Testing**: The main block enables quick testing of the scanning functionality.

This comprehensive walkthrough should help developers understand how each component of **nmap_scanner.py** operates and how the module integrates network scanning, asynchronous execution, and logging.

_(Reference: nmap_scanner)_