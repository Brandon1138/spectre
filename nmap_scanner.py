import nmap
import json
import asyncio
import logging

# Set up a common logging configuration for this module
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

class NmapScanner:
    def __init__(self, scan_arguments='-sS -sV -O'):
        # Initialise the python-nmap scanner
        self.nm = nmap.PortScanner()
        self.scan_arguments = scan_arguments

    def scan_target(self, target, ports="1-1024"):
        try:
            self.nm.scan(target, ports, arguments=self.scan_arguments)
            result = self.nm[target]

            # Process OS detection results (if further processing is needed)
            osmatches = result.get('osmatch', [])

            # Process TCP service details for potential internal checks
            tcp_data = result.get('tcp', {})
            for port, port_info in tcp_data.items():
                service_name = port_info.get('name', '')
                service_version = port_info.get('version', '')
                product = port_info.get('product', '')
                # Additional processing can be done here

            return result

        except Exception as e:
            logging.exception("Scan error for target %s: %s", target, e)
            return None

    async def async_scan_target(self, target, ports="1-1024"):
        """
        Asynchronously execute a scan on the given target.
        Offloads the blocking scan_target call to a background thread.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.scan_target, target, ports)

    def save_scan(self, target, filename, ports="1-1024"):
        """
        Run a scan and save the results in JSON format.
        """
        result = self.scan_target(target, ports)
        if result:
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            logging.info("Scan results saved to %s", filename)
        else:
            logging.error("No results to save for target %s.", target)

if __name__ == '__main__':
    scanner = NmapScanner()
    # Run a simple synchronous test scan against localhost
    result = scanner.scan_target("127.0.0.1")
    if result:
        print(json.dumps(result, indent=2))
