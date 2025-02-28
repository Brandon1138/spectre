## File Overview

This module implements a user interface using the Rich library. It handles input for target IP addresses, concurrently executes network scans using asynchronous calls, displays scan progress, and shows the results in a formatted table. It also logs scan results via the dedicated logging module.

_(Reference: ui)_

---

## Import Statements

`import asyncio 
`import logging from rich.console`
`import Console from rich.progress` 
`import Progress, SpinnerColumn, TextColumn from rich.table` 
`import Table from nmap_scanner`
`import NmapScanner  # or import StealthNmapScanner as needed from logger`
`import ScanLogger`

- **asyncio**: Used to schedule and run asynchronous scanning tasks concurrently.
- **logging**: Facilitates logging events and errors.
- **Rich Library Components**:
    - **Console**: Manages user input and output.
    - **Progress, SpinnerColumn, TextColumn**: Provide visual feedback during scanning.
    - **Table**: Formats and displays scan results in a structured table.
- **nmap_scanner.NmapScanner**: Imports the scanner class for performing network scans.
- **logger.ScanLogger**: Imports the logging utility to record scan outputs in various formats.

---

## Function: `run_scan`

`def run_scan():`     
	`console = Console()` 
	`target_input = console.input("Enter target IP(s) (comma-separated if multiple): ")`  
	`targets = [t.strip() for t in target_input.split(",") if t.strip()]`     
	
	 `# Initialise scanner and logger`    
	`scanner = NmapScanner()` 
	`logger = ScanLogger()`
	
- **User Input**:
    - A `Console` object is created from Rich to handle input/output.
    - The user is prompted to enter target IP addresses, potentially multiple targets separated by commas.
    - The entered string is split into a list of targets after stripping any extra whitespace.
	
- **Initialization**:
    - A new instance of `NmapScanner` is created to perform scans.
    - An instance of `ScanLogger` is also instantiated to log results.

---

### Asynchronous Scanning Task

    `async def run_scans():       
	    tasks = [scanner.async_scan_target(target) for target in targets]       
		results = await asyncio.gather(*tasks)        
		return dict(zip(targets, results))`

- **Purpose**: Encapsulate the asynchronous scanning of multiple targets.
	
- **Task Creation**:
    - For each target, an asynchronous scanning task is generated using `scanner.async_scan_target(target)`.
	
- **Execution**:
    - `asyncio.gather` concurrently runs these tasks and waits for all to complete.
	
- **Results**:
    - The results are zipped with the corresponding target IPs into a dictionary, allowing easy association of each scan result with its target.

---

### Running the Asynchronous Scans

    `try: 
		results = asyncio.run(run_scans())    
	 except Exception as e:        
		logging.exception("Error during asynchronous scanning: %s", e)
		console.print("[bold red]An error occurred during scanning.[/bold red]")        
		 return`

- **Execution with Exception Handling**:
    - `asyncio.run(run_scans())` starts the asynchronous event loop and collects scan results.
    - If any exception occurs during the scan, it is logged using `logging.exception` and a red error message is printed to the console.
	
- **User Feedback**:
    - In case of errors, the function exits gracefully without proceeding further.

---

### Displaying and Logging Scan Results

    # Display results for each target
    for target, result in results.items():
        console.print(f"[bold green]Scan complete for {target}[/bold green]")
        if result:
            table = Table(title=f"Scan Results for {target}")
            table.add_column("Port", style="cyan", no_wrap=True)
            table.add_column("State", style="magenta")
            table.add_column("Service", style="green")

            tcp_results = result.get("tcp", {})
            if tcp_results:
                for port, info in tcp_results.items():
                    table.add_row(str(port), info.get("state", "N/A"), info.get("name", "N/A"))
            else:
                table.add_row("N/A", "No TCP info", "")
            console.print(table)
            # Log results in JSON format
            logger.log_json(result, filename_prefix=f"scan_{target.replace('.', '_')}")
        else:
            console.print(f"[bold red]No results returned from scan of {target}.[/bold red]")


- **For Each Target**:
    - A success message is printed once the scan for a target is complete.
	
- **Building the Results Table**:
    - A `Table` is created with the title set to the current target.
    - Columns are defined for "Port", "State", and "Service" using distinct color styles.
	
- **Populating the Table**:
    - The scan result is expected to include a "tcp" key containing port scan details.
    - For each TCP port, the table is populated with the port number, its state (e.g., open/closed), and the service name.
    - If no TCP information is found, a placeholder row is added.
	
- **Logging**:
    - Each scan result is logged in JSON format using `ScanLogger.log_json`, with the filename prefix adjusted based on the target IP (dots replaced by underscores).
	
- **Handling Missing Results**:
    - If no result is returned for a target, an error message is printed in bold red.

---

## Main Block

`if __name__ == '__main__':   
	`run_scan()`

- **Purpose**:
    - Allows the module to be executed directly.
	
- **Action**:
    - Calls the `run_scan()` function, initiating the entire UI flow: prompting for targets, running scans concurrently, displaying results, and logging them.

---

## Summary

- **User Input & Initialization**: The module starts by collecting target IP addresses from the user and initializing the necessary scanning and logging objects.
- **Asynchronous Execution**: It uses `asyncio` to scan multiple targets concurrently, improving performance.
- **Result Presentation**: Scan results are formatted into a Rich table and printed to the console, providing clear visual feedback.
- **Persistent Logging**: Each result is also logged in JSON format for future reference.
- **Robust Error Handling**: Exceptions during scanning are caught, logged, and communicated to the user.

This comprehensive walkthrough should clarify how the UI module integrates asynchronous scanning, user interaction, result presentation, and logging, making it a central component of the Spectre network scanner.

_(Reference: ui)_