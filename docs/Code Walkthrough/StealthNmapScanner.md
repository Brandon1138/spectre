## File Overview

The module extends basic nmap scanning functionality with stealth options. It redefines a simplified version of the base scanner (mirroring the one in _nmap_scanner.py_) and then builds a specialized subclass called `StealthNmapScanner` that accepts stealth-related parameters (such as decoys, fragmentation, idle scanning, timing adjustments, source port spoofing, and TTL settings).

_(Reference: stealth_scanner)_

---

## Import Statements

`import nmap
`import json`
`import logging from nmap_scanner`
`import NmapScanner`

- **nmap**: Imports the `python-nmap` library to handle scanning operations.
- **json**: Although not used directly for scanning in this module, it's available for potential JSON manipulations or logging needs.
- **logging**: Provides logging functionality to capture events and errors.
- **from nmap_scanner import NmapScanner**: Imports the original `NmapScanner` from the main scanning module. (Note: Despite this import, the module also defines its own `NmapScanner` class. This may be for demonstration or override purposes.)

---

## Logging Configuration

`logging.basicConfig(     
	`level=logging.INFO,`
	`format="%(asctime)s [%(levelname)s] %(message)s",`
	`handlers=[logging.StreamHandler()]` 
`)`

- This establishes a consistent logging format for the module.
- **level=logging.INFO**: Ensures that INFO-level and higher messages are logged.
- **handlers**: Directs logs to the console using a stream handler.

---

## Redefinition of `NmapScanner`

`class NmapScanner:`
	`def __init__(self, scan_arguments='-sS'):`
		`self.nm = nmap.PortScanner()`
		`self.scan_arguments = scan_arguments`
		
	def scan_target(self, target, ports="1-1024"):
		try:
			self.nm.scan(target, ports, arguments=self.scan_arguments)
			return self.nm[target]
		except Exception as e:
			logging.exception("Scan error for target %s: %s", target, e)
			return None`

- **Purpose**: Even though an original `NmapScanner` is imported, this local redefinition provides a minimal baseline scanner.

- **Constructor (`__init__`)**:
    - Instantiates a `PortScanner` object.
    - Sets a default scan argument (`-sS`, a TCP SYN scan), which can be overridden.

- **Method (`scan_target`)**:
    - Executes a scan on a target for ports in the range 1-1024 by default.
    - Returns the scan results (a dictionary) if successful.
    - In case of errors, logs the exception and returns `None`.

This setup ensures that the stealth scanner can fall back on known scanning behavior while allowing customization through its subclass.

---

## Class Definition: `StealthNmapScanner`

`class StealthNmapScanner(NmapScanner):
	`def __init__(self, decoy=None, fragmentation=False, idle_scan_zombie=None,`
		`timing=None, source_port=None, ttl=None):`
	`stealth_opts = ""` 
	`if decoy:`    
		`stealth_opts += f" -D {decoy}"`
	`if fragmentation:`       
		`stealth_opts += " -f"`  
	`if idle_scan_zombie:` 
		`stealth_opts += f" -sI {idle_scan_zombie}"`    
	`if timing:`    
		`stealth_opts += f" -T{timing}"`  
	`if source_port:`    
		`stealth_opts += f" --source-port {source_port}"` 
	`if ttl:`    
		`stealth_opts += f" --ttl {ttl}"` 
	`stealth_opts = stealth_opts.strip() or '-sS'`   
	`super().__init__(scan_arguments=stealth_opts)`

- **Inheritance**: `StealthNmapScanner` inherits from the local `NmapScanner`. This means it retains the basic scanning methods but adjusts the command-line options.

- **Parameters**:
    - **`decoy`**: If provided, the scanner uses decoy IPs (via the `-D` flag).
    - **`fragmentation`**: When set to `True`, enables packet fragmentation with `-f`.
    - **`idle_scan_zombie`**: If provided, triggers an idle scan using a specified zombie host (`-sI`).
    - **`timing`**: Adjusts the timing template for the scan using `-T`.
    - **`source_port`**: Sets the source port using the `--source-port` flag.
    - **`ttl`**: Adjusts the TTL value via the `--ttl` flag.

- **Stealth Options Construction**:
    - The method concatenates the provided options into a single command-line string (`stealth_opts`).
    - **`stealth_opts.strip() or '-sS'`**: Ensures that if no stealth option is provided, it defaults to the basic TCP SYN scan (`-sS`).

- **Superclass Initialization**:
    - Calls `super().__init__(scan_arguments=stealth_opts)`, which initializes the scanner with the composed stealth options.

This class design allows developers to easily toggle various stealth parameters without changing the underlying scanning logic.

---

## Main Block for Testing

`if __name__ == '__main__':
	`# Example usage with stealth options` 
	`scanner = StealthNmapScanner(decoy="RND:10", fragmentation=True, timing=1)`
	`result = scanner.scan_target("127.0.0.1")` 
	`if result:`    
		`logging.info("Scan results:\n%s", json.dumps(result, indent=2))`

- **Purpose**: Provides a simple test to verify that the stealth scanning works as intended.

- **Steps**:
    - Instantiates `StealthNmapScanner` with example parameters:
        - **`decoy="RND:10"`**: Specifies 10 random decoy IPs.
        - **`fragmentation=True`**: Enables packet fragmentation.
        - **`timing=1`**: Uses a timing template (the lowest speed in this case).
    - Calls `scan_target` on localhost (`127.0.0.1`).
    - If a valid result is returned, it logs the results in a formatted JSON string.

This block serves as a practical demonstration of how to utilize stealth options, ensuring that modifications to scan arguments are correctly integrated into the scan command.

---

## Summary

- **Imports and Logging**: The module imports necessary libraries and configures logging for detailed output.
- **Local NmapScanner**: Although imported from elsewhere, a local version is defined to maintain consistency and provide baseline functionality.
- **StealthNmapScanner**:
    - Inherits from the base scanner.
    - Accepts additional parameters for stealth scanning.
    - Dynamically constructs the command-line options to pass to nmap.
- **Testing Block**: Demonstrates a practical example of a stealth scan against localhost.

This detailed walkthrough clarifies how stealth scanning enhancements are layered on top of basic scanning capabilities, making the module both flexible and easy to extend.

_(Reference: stealth_scanner)_