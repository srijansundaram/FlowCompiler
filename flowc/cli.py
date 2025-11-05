# CLI entrypoint for FlowC

import subprocess
from flowc.parser import parse_flow
from flowc.codegen import generate_pandas_code

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m flowc.cli <file.flow>")
        return
    
    src_path = sys.argv[1]
    print(f"✅ Compiling {src_path}...")

    try:
        with open(src_path) as f:
            src = f.read()

        load, pipelines = parse_flow(src)
        generate_pandas_code(load, pipelines)

        print("✅ Running generated pipeline...\n")
        subprocess.run(["python", "generated_pipeline.py"], check=True)
        print("\n✅ Pipeline execution completed successfully.")

        for p in pipelines:
            for s in p.steps:
                if hasattr(s, "path"):
                    print(f"📂 Output saved to: {s.path}")
                    
    except Exception as e:
        print(f"\n❌ Pipeline execution failed: {e}")
    


if __name__ == "__main__":
    main()
