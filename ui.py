from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from nmap_scanner import NmapScanner  # or import StealthNmapScanner as needed
from logger import ScanLogger

def run_scan():
    console = Console()
    target = console.input("Enter target IP: ")

    # Initialise scanner and logger
    scanner = NmapScanner()
    logger = ScanLogger()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console
    ) as progress:
        task = progress.add_task("Scanning...", start=False)
        progress.start_task(task)
        result = scanner.scan_target(target)
        progress.update(task, advance=100)

    console.print("[bold green]Scan complete[/bold green]")
    if result:
        # Build table for TCP results
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
        console.print("[bold red]No results returned from scan.[/bold red]")

if __name__ == '__main__':
    run_scan()
