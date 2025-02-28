## File Overview

This module implements the `ScanLogger` class, which provides utilities for logging scan results in various formats (JSON, plaintext, and Markdown). The logs are stored in a date-organized directory structure, ensuring that scan outputs are neatly organized for later review and analysis.

_(Reference: logger)_

---

## Import Statements

`import os 
`import json`
`import logging from datetime`
`import datetime`

- **os**: Used for file system operations such as checking if directories exist and creating new directories.
- **json**: Used to serialize scan data into JSON format.
- **logging**: Facilitates logging of events, errors, and general information during execution.
- **datetime**: Provides current date and time information, which is used to timestamp log files and organize them by date.

---

## Logging Configuration

`logging.basicConfig(     
	`level=logging.INFO,`   
	`format="%(asctime)s [%(levelname)s] %(message)s",`   
	`handlers=[logging.StreamHandler()]` 
`)`

- **`logging.basicConfig`**: Configures the logging system for the module.
    - **`level=logging.INFO`**: Ensures that INFO-level and higher messages are output.
    - **`format`**: Specifies the log message format, including the timestamp, log level, and message content.
    - **`handlers`**: Uses a stream handler to print log messages to the console.

This configuration standardizes the log output across the module.

---

## Class Definition: `ScanLogger`

The `ScanLogger` class is responsible for creating and writing log files in three different formats.

### Constructor: `__init__`

`def __init__(self, base_dir="logs"):    
	`self.base_dir = base_dir`   
	`if not os.path.exists(self.base_dir):`     
		`os.makedirs(self.base_dir)`      
		`logging.info("Created base log directory: %s", self.base_dir)`

- **Parameter**:
    - `base_dir`: Specifies the base directory where logs will be stored. It defaults to `"logs"`.
	
- **Functionality**:
    - Checks if the `base_dir` exists. If not, it creates the directory.
    - Logs an INFO message indicating that the base directory was created.

This initialization step ensures that there is a designated folder for storing log files.

---

### Helper Method: `_get_log_dir`

`def _get_log_dir(self):   
	`today = datetime.now().strftime("%Y-%m-%d")`   
	`log_dir = os.path.join(self.base_dir, today)`     
	`if not os.path.exists(log_dir):`     
		`os.makedirs(log_dir)`       
		`logging.info("Created log directory for today: %s", log_dir)`    
	`return log_dir`

- **Purpose**: Determines and creates (if necessary) a directory for the current date.
	
- **Steps**:
    - Uses `datetime.now()` to get the current date and formats it as `YYYY-MM-DD`.
    - Joins the base directory with the current date to form a date-specific directory path.
    - Checks if this directory exists; if not, it creates it and logs the creation.
    - Returns the path to the date-specific directory.

This approach helps in organizing logs by date, making them easier to manage and search.

---

### Method: `log_json`

`def log_json(self, data, filename_prefix="scan"):   
	`log_dir = self._get_log_dir()`  
	`timestamp = datetime.now().strftime("%H%M%S")`   
	`filename = os.path.join(log_dir, f"{filename_prefix}_{timestamp}.json")`  
	`with open(filename, 'w') as f:`       
		`json.dump(data, f, indent=2)`   
	`logging.info("JSON log saved to %s", filename)`

- **Parameters**:
    - `data`: The scan data (typically a dictionary) to be logged.
    - `filename_prefix`: A prefix for the filename, defaulting to `"scan"`.
	
- **Process**:
    - Retrieves the log directory for the current day via `_get_log_dir()`.
    - Generates a timestamp (`HHMMSS`) to ensure unique filenames.
    - Constructs a filename combining the prefix, timestamp, and `.json` extension.
    - Opens the file in write mode and serializes `data` into JSON with an indentation of 2 for readability.
    - Logs an INFO message confirming where the JSON log was saved.

This method provides a standardized way to persist scan results in a machine-readable JSON format.

---

### Method: `log_plaintext`

`def log_plaintext(self, data, filename_prefix="scan"):   
	`log_dir = self._get_log_dir()`    
	`timestamp = datetime.now().strftime("%H%M%S")`  
	`filename = os.path.join(log_dir, f"{filename_prefix}_{timestamp}.txt")`   
	`with open(filename, 'w') as f:`     
		`f.write(str(data))`   
	`logging.info("Plaintext log saved to %s", filename)`

- **Functionality**:
    - Similar to `log_json`, this method creates a log file in a date-based directory.
    - Instead of formatting data as JSON, it converts `data` to a string and writes it to a `.txt` file.
    - Logs the file location after saving.

This format is useful for quickly reviewing scan results in a human-readable, unstructured text format.

---

### Method: `log_markdown`

`def log_markdown(self, data, filename_prefix="scan"):
`log_dir = self._get_log_dir()`
`timestamp = datetime.now().strftime("%H%M%S")`
`filename = os.path.join(log_dir, f"{filename_prefix}_{timestamp}.md")`
`with open(filename, 'w') as f:` 
	`f.write("# Scan Results\n")` 
	`f.write("``\n")`
	`f.write(json.dumps(data, indent=2))`
	`f.write("\n``\n")`    
`logging.info("Markdown log saved to %s", filename)`

- **Purpose**: Logs scan results in Markdown format, which is particularly useful for documentation tools like Obsidian.
	
- **Process**:
    - Similar to the other logging methods, it computes the log directory and filename (with a `.md` extension).
    - Writes a Markdown header (`# Scan Results`), opens a code block, and then writes the formatted JSON representation of the scan data.
    - Closes the code block and logs the save location.

This method makes scan data presentable in a format that supports syntax highlighting and improved readability.

---

## Main Block for Testing

`if __name__ == '__main__':
	`sample_data = {"example": "data", "status": "ok"}` 
	`logger = ScanLogger()` 
	`logger.log_json(sample_data)`
	`logger.log_plaintext(sample_data)     logger.log_markdown(sample_data)`

- **Purpose**:
    - Provides a simple test routine to validate that all logging methods work as intended.
	
- **Process**:
    - Defines a sample data dictionary.
    - Instantiates the `ScanLogger` class.
    - Calls each logging method to create JSON, plaintext, and Markdown log files using the sample data.

This block is useful during development to ensure that log files are created correctly and stored in the appropriate directory structure.

---

## Summary

- **Initialization & Directory Management**: The constructor ensures a base directory exists, and `_get_log_dir` organizes logs by the current date.
- **Multiple Logging Formats**:
    - **`log_json`**: Saves machine-readable JSON files.
    - **`log_plaintext`**: Saves unformatted text logs.
    - **`log_markdown`**: Saves Markdown files with a formatted code block.
- **Testing Block**: A simple main routine demonstrates and verifies the functionality of the logging methods.

This comprehensive walkthrough should help developers understand how **logger.py** manages and organizes log outputs for scan results, providing flexibility in both machine and human-readable formats.

_(Reference: logger)_