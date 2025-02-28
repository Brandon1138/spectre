import nmap
import json

class NmapScanner:
    def __init__(self, scan_arguments='-sS'):
        self.nm = nmap.PortScanner()
        self.scan_arguments = scan_arguments

    def scan_target(self, target, ports="1-1024"):
        try:
            self.nm.scan(target, ports, arguments=self.scan_arguments)
            return self.nm[target]
        except Exception as e:
            print(f"Scan error: {e}")
            return None

    def save_scan(self, target, filename, ports="1-1024"):
        result = self.scan_target(target, ports)
        if result:
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Scan results saved to {filename}")
        else:
            print("No results to save.")

class StealthNmapScanner(NmapScanner):
    def __init__(self, decoy=None, fragmentation=False, idle_scan_zombie=None,
                 timing=None, source_port=None, ttl=None):
        stealth_opts = ""
        if decoy:
            # Example: '-D RND:10' or '-D 192.168.1.100,192.168.1.101'
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
        # Remove extra spaces
        stealth_opts = stealth_opts.strip() or '-sS'
        super().__init__(scan_arguments=stealth_opts)

if __name__ == '__main__':
    # Example: decoy scan using random decoys, fragmentation enabled, and timing level 1.
    scanner = StealthNmapScanner(decoy="RND:10", fragmentation=True, timing=1)
    result = scanner.scan_target("127.0.0.1")
    if result:
        print(json.dumps(result, indent=2))
