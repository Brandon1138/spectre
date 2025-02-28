import nmap
import json

class NmapScanner:
    def __init__(self, scan_arguments='-sS'):
        # Initialise the python-nmap scanner
        self.nm = nmap.PortScanner()
        self.scan_arguments = scan_arguments

    def scan_target(self, target, ports="1-1024"):
        """
        Execute an nmap scan on the given target over specified ports.
        Returns a dict with scan results.
        """
        try:
            self.nm.scan(target, ports, arguments=self.scan_arguments)
            return self.nm[target]
        except Exception as e:
            print(f"Scan error: {e}")
            return None

    def save_scan(self, target, filename, ports="1-1024"):
        """
        Run a scan and save the results in JSON format.
        """
        result = self.scan_target(target, ports)
        if result:
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Scan results saved to {filename}")
        else:
            print("No results to save.")

if __name__ == '__main__':
    scanner = NmapScanner()
    result = scanner.scan_target("127.0.0.1")
    if result:
        print(json.dumps(result, indent=2))
