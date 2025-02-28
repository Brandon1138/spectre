import nmap
import json
import logging
from nmap_scanner import NmapScanner

# Set up logging for this module
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

class NmapScanner:
    def __init__(self, scan_arguments='-sS'):
        self.nm = nmap.PortScanner()
        self.scan_arguments = scan_arguments

    def scan_target(self, target, ports="1-1024"):
        try:
            self.nm.scan(target, ports, arguments=self.scan_arguments)
            return self.nm[target]
        except Exception as e:
            logging.exception("Scan error for target %s: %s", target, e)
            return None

class StealthNmapScanner(NmapScanner):
    def __init__(self, decoy=None, fragmentation=False, idle_scan_zombie=None,
                 timing=None, source_port=None, ttl=None):
        stealth_opts = ""
        if decoy:
            stealth_opts += f" -D {decoy}"
        if fragmentation:
            stealth_opts += " -f"
        if idle_scan_zombie:
            stealth_opts += f" -sI {idle_scan_zombie}"
        if timing:
            stealth_opts += f" -T{timing}"
        if source_port:
            stealth_opts += f" --source-port {source_port}"
        if ttl:
            stealth_opts += f" --ttl {ttl}"
        stealth_opts = stealth_opts.strip() or '-sS'
        super().__init__(scan_arguments=stealth_opts)

if __name__ == '__main__':
    # Example usage with stealth options
    scanner = StealthNmapScanner(decoy="RND:10", fragmentation=True, timing=1)
    result = scanner.scan_target("127.0.0.1")
    if result:
        logging.info("Scan results:\n%s", json.dumps(result, indent=2))
