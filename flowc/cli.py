# CLI entrypoint for FlowC

import subprocess
import sys
import argparse
import time
from rich.console import Console
from rich.progress import track
from rich.panel import Panel
from rich.traceback import install
from flowc.parser import parse_flow
from flowc.codegen import generate_pandas_code

console = Console()
install()  


def main():
    parser = argparse.ArgumentParser(description="Flow Compiler CLI (v1.0.2)")
    parser.add_argument("file", help="Path to the .flow source file")
    parser.add_argument("--verbose", action="store_true", help="Enable detailed logs")
    parser.add_argument("--no-run", action="store_true", help="Compile only, skip execution")

    args = parser.parse_args()

    src_path = args.file
    verbose = args.verbose
    no_run = args.no_run

    start_time = time.time()

    console.print("\n🚀 [bold cyan]Flow Compiler v1.0.2[/bold cyan]")
    console.print(f"📂 Loading source: [bold white]{src_path}[/bold white]\n")

    try:
        # === Step 1: Parse ===
        console.print("🔍 [cyan]Parsing source file...[/cyan]")
        load, pipelines = parse_flow(open(src_path).read())
        if verbose:
            console.log(f"AST successfully built with {len(pipelines)} pipelines.")

        # === Step 2: Generate Code ===
        console.print("\n⚙️ [cyan]Generating Python backend code...[/cyan]")
        for step in track(pipelines, description="Generating pipelines"):
            generate_pandas_code(load, [step])

        console.print("[green]✅ Code generation completed: generated_pipeline.py[/green]\n")

        if not no_run:
            # === Step 3: Execute Generated Code ===
            console.print("▶️ [blue]Executing generated pipeline...[/blue]")
            try:
                with console.status("[bold green]Running...[/bold green]", spinner="dots"):
                    subprocess.run(["python", "generated_pipeline.py"], check=True)
                console.print("[green]✅ Pipeline executed successfully![/green]")
            except subprocess.CalledProcessError:
                console.print("[red]❌ Pipeline execution failed.[/red]")
                sys.exit(1)
        else:
            console.print("[yellow]⚠ Skipped execution (--no-run flag used).[/yellow]")

        # === Step 4: Show Summary ===
        elapsed = time.time() - start_time
        console.print(
            Panel.fit(
                f"[bold green]✅ Compilation Completed Successfully![/bold green]\n\n"
                f"[cyan]Source:[/cyan] {src_path}\n"
                f"[cyan]Output:[/cyan] generated_pipeline.py\n"
                f"[cyan]Pipelines Processed:[/cyan] {len(pipelines)}\n"
                f"[cyan]Elapsed Time:[/cyan] {elapsed:.2f}s\n"
                f"[cyan]Version:[/cyan] v1.2.2",
                title="[bold]Summary[/bold]",
                border_style="bright_green",
            )
        )

    except Exception as e:
        console.print(f"\n[red]❌ Compilation aborted: {e}[/red]")
        if verbose:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
