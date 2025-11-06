# CLI entrypoint for FlowC

import subprocess
from flowc.parser import parse_flow
from flowc.codegen import generate_pandas_code
from flowc.semantic import check_pipeline_dependencies

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m flowc.cli <file.flow>")
        return
    
    src_path = sys.argv[1]
    print(f"✅ Compiling {src_path}...")

    with open(src_path) as f:
        src = f.read()

    loads, pipelines = parse_flow(src)

    try:
        check_pipeline_dependencies(pipelines)
    except Exception as e:
        print(f"❌ {e}")
        print("❌ Compilation aborted due to dependency error.")
        return  # 🚨 Stop here, don't run codegen

    print()
    print("🔗 Dependency validation successful.")
    generate_pandas_code(loads, pipelines)

    try:
        with open("generated_pipeline.py", "r", encoding="utf-8") as gen:
            content = gen.read()
            if "⚠️ Skipped pipeline" in content or "undefined dependency" in content:
                print("⚠️ Skipped execution due to incomplete or circular dependencies.")
                return
    except FileNotFoundError:
        print("❌ No generated file found. Compilation aborted.")
        return

    print("✅ Running generated pipeline...\n")
    try:
        subprocess.run(["python", "generated_pipeline.py"], check=True)
        print("\n✅ Pipeline execution completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Pipeline execution failed: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error during execution: {e}")

if __name__ == "__main__":
    main()
