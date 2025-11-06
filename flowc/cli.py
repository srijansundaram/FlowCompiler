# CLI entrypoint for FlowC

import subprocess
from flowc.parser import parse_flow
from flowc.codegen import generate_pandas_code
from flowc.ai_hooks import detect_invalid_keywords, auto_correct_source
from flowc.semantic import validate_semantics


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
            

        if not hasattr(main, "_ai_checked"):
            issues = detect_invalid_keywords(src)
            if issues:
                print("\n⚠️  Possible Syntax Issues Detected:")
                for line_num, wrong, suggestion in issues:
                    if suggestion:
                        print(f"   Line {line_num}: '{wrong}' → Did you mean '{suggestion}'?")
                    else:
                        print(f"   Line {line_num}: '{wrong}' → Unknown keyword (no suggestion found)")

                choice = input("\nApply these corrections automatically? (y/n): ").strip().lower()
                if choice == "y":
                    src = auto_correct_source(src, issues)
                    print("\n✅ Applied corrections in-memory. Continuing compilation...\n")
                else:
                    print("\nSkipping auto-correction. Continuing compilation...\n")


        load, pipelines = parse_flow(src)
        
        try:
            validate_semantics(load, pipelines)
        except Exception as e:
            print(e)
            print("❌ Compilation aborted due to semantic error.\n")
            return

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
