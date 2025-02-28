import os
import json
from datetime import datetime

class ScanLogger:
    def __init__(self, base_dir="logs"):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def _get_log_dir(self):
        today = datetime.now().strftime("%Y-%m-%d")
        log_dir = os.path.join(self.base_dir, today)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return log_dir

    def log_json(self, data, filename_prefix="scan"):
        log_dir = self._get_log_dir()
        timestamp = datetime.now().strftime("%H%M%S")
        filename = os.path.join(log_dir, f"{filename_prefix}_{timestamp}.json")
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"JSON log saved to {filename}")

    def log_plaintext(self, data, filename_prefix="scan"):
        log_dir = self._get_log_dir()
        timestamp = datetime.now().strftime("%H%M%S")
        filename = os.path.join(log_dir, f"{filename_prefix}_{timestamp}.txt")
        with open(filename, 'w') as f:
            f.write(str(data))
        print(f"Plaintext log saved to {filename}")

    def log_markdown(self, data, filename_prefix="scan"):
        log_dir = self._get_log_dir()
        timestamp = datetime.now().strftime("%H%M%S")
        filename = os.path.join(log_dir, f"{filename_prefix}_{timestamp}.md")
        with open(filename, 'w') as f:
            f.write("# Scan Results\n")
            f.write("```\n")
            f.write(json.dumps(data, indent=2))
            f.write("\n```\n")
        print(f"Markdown log saved to {filename}")

if __name__ == '__main__':
    sample_data = {"example": "data", "status": "ok"}
    logger = ScanLogger()
    logger.log_json(sample_data)
    logger.log_plaintext(sample_data)
    logger.log_markdown(sample_data)
