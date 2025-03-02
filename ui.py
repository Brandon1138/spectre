import asyncio
import logging
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from nmap_scanner import NmapScanner  # or import StealthNmapScanner as needed
from logger import ScanLogger

# Set up logging for the UI module
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def run_scan():
    console = Console()
    target_input = console.input("Enter target IP(s) (comma-separated if multiple): ")
    targets = [t.strip() for t in target_input.split(",") if t.strip()]

    # Initialise scanner and logger
    scanner = NmapScanner()
    logger = ScanLogger()

    async def run_scans():
        tasks = [scanner.async_scan_target(target) for target in targets]
        results = await asyncio.gather(*tasks)
        return dict(zip(targets, results))

    try:
        results = asyncio.run(run_scans())
    except Exception as e:
        logging.exception("Error during asynchronous scanning: %s", e)
        console.print("[bold red]An error occurred during scanning.[/bold red]")
        return

    for target, result in results.items():
        console.print(f"[bold green]Scan complete for {target}[/bold green]")
        if result:
            # Show OS detection results first.
            osmatches = result.get('osmatch', [])
            if osmatches:
                console.print(
                    f"[bold]OS Detection:[/bold] {osmatches[0].get('name', 'Unknown')} "
                    f"(Accuracy: {osmatches[0].get('accuracy', 'N/A')}%)"
                )
            else:
                console.print("[bold red]OS detection unavailable or inconclusive.[/bold red]")

            # Build table with additional 'Version' column.
            table = Table(title=f"Scan Results for {target}")
            table.add_column("Port", style="cyan", no_wrap=True)
            table.add_column("State", style="magenta")
            table.add_column("Service", style="green")
            table.add_column("Version", style="yellow")

            tcp_results = result.get("tcp", {})
            if tcp_results:
                for port, info in tcp_results.items():
                    version_str = info.get("version", "")
                    product_str = info.get("product", "")
                    version_info = f"{product_str} {version_str}" if product_str or version_str else "N/A"
                    table.add_row(
                        str(port),
                        info.get("state", "N/A"),
                        info.get("name", "N/A"),
                        version_info
                    )
            else:
                table.add_row("N/A", "No TCP info", "", "")
            console.print(table)

            # Log the extended JSON including OS and service info.
            logger.log_json(result, filename_prefix=f"scan_{target.replace('.', '_')}")
        else:
            console.print(f"[bold red]No results returned from scan of {target}.[/bold red]")


if __name__ == '__main__':
    run_scan()
