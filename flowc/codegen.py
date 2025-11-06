# Code generator (Pandas backend) for the Flow programming language.

from flowc.ast_nodes import (
    Filter, Sum, GroupBy, Average, DropDuplicates,
    SortBy, Emit, Ensure, Join, Rename, Select
)

def generate_pandas_code(loads, pipelines):

    if not isinstance(loads, list):
        loads = [loads] if loads else []

    code_lines = ["import pandas as pd\n"]

    # ---------------- LOAD SECTION ----------------
    if len(loads) > 0:
        for ld in loads:
            code_lines.append(f'{ld.alias} = pd.read_csv(r"{ld.path}")')
    else:
        code_lines.append("# ⚠️ No load statement found; starting with empty DataFrame")
        code_lines.append("data = pd.DataFrame()")

    pipeline_outputs = {}

    # ---------------- PIPELINE SECTION ----------------
    if not pipelines or len(pipelines) == 0:
        code_lines.append("# ⚠️ No pipelines defined, skipping generation.")
        with open("generated_pipeline.py", "w", encoding="utf-8") as f:
            f.write("\n".join(code_lines))
        print("⚠️ No pipelines to generate. File created with load only.")
        return

    for pipe in pipelines:
        code_lines.append(f"\n# ----- Pipeline: {pipe.name} -----")

        known_aliases = [ld.alias for ld in loads] + list(pipeline_outputs.keys())
        pipeline_names = [p.name for p in pipelines]

        if pipe.depends_on and pipe.depends_on in pipeline_outputs:
            input_alias = pipeline_outputs[pipe.depends_on]

        elif pipe.depends_on and pipe.depends_on not in pipeline_outputs:

            print(f"❌ Skipping pipeline '{pipe.name}' because dependency '{pipe.depends_on}' was not generated.")
            code_lines.append(f"# ⚠️ Skipped pipeline '{pipe.name}' due to missing dependency '{pipe.depends_on}'")
            continue

        else:
            if pipe.base_alias:
                if pipe.base_alias in known_aliases:
                    input_alias = pipe.base_alias
                elif pipe.base_alias in pipeline_names:
                    print(f"❌ Skipping pipeline '{pipe.name}' because base alias '{pipe.base_alias}' is an unresolved pipeline.")
                    code_lines.append(f"# ⚠️ Skipped pipeline '{pipe.name}' due to unresolved pipeline alias '{pipe.base_alias}'")
                    continue
                else:
                    print(f"❌ Skipping pipeline '{pipe.name}' because base alias '{pipe.base_alias}' is undefined.")
                    code_lines.append(f"# ⚠️ Skipped pipeline '{pipe.name}' due to undefined base alias '{pipe.base_alias}'")
                    continue
            elif len(loads) > 0:
                input_alias = loads[0].alias
            else:
                input_alias = "pd.DataFrame()"

        if input_alias == "pd.DataFrame()":
            code_lines.append(f"{pipe.name} = {input_alias}")
        else:
            code_lines.append(f"{pipe.name} = {input_alias}.copy()")

        alias = pipe.name

        # ---------------- PIPELINE STEPS ----------------
        for step in pipe.steps:
            # FILTER
            if isinstance(step, Filter):
                code_lines.append(f'{alias} = {alias}.query("{step.expr}")')

            # SUM
            elif isinstance(step, Sum):
                if step.column:
                    code_lines.append(
                        f'{alias} = pd.DataFrame([{alias}["{step.column}"].sum()], columns=["{step.alias}"])'
                    )
                else:
                    code_lines.append("# ⚠️ Skipped SUM (no column specified)")

            # GROUP BY
            elif isinstance(step, GroupBy):
                if step.column:
                    code_lines.append(
                        f'{alias} = {alias}.groupby("{step.column}").sum().reset_index()'
                    )
                else:
                    code_lines.append("# ⚠️ Skipped GROUPBY (no column specified)")

            # AVERAGE
            elif isinstance(step, Average):
                if step.column:
                    code_lines.append(
                        f'{alias} = pd.DataFrame([{alias}["{step.column}"].mean()], columns=["{step.alias}"])'
                    )
                else:
                    code_lines.append("# ⚠️ Skipped AVERAGE (no column specified)")

            # DROP DUPLICATES
            elif isinstance(step, DropDuplicates):
                if step.column:
                    code_lines.append(
                        f'{alias} = {alias}.drop_duplicates(subset="{step.column}")'
                    )
                else:
                    code_lines.append(f"{alias} = {alias}.drop_duplicates()")

            # SORT BY
            elif isinstance(step, SortBy):
                if step.column:
                    code_lines.append(
                        f'{alias} = {alias}.sort_values("{step.column}", ascending={step.ascending})'
                    )
                else:
                    code_lines.append("# ⚠️ Skipped SORTBY (no column specified)")

            # ENSURE
            elif isinstance(step, Ensure):
                code_lines.append(
                    f'assert ({step.condition}), "Ensure failed: {step.condition}"'
                )

            # JOIN
            elif isinstance(step, Join):
                code_lines.append(
                    f'{alias} = {alias}.merge({step.other_alias}, on="{step.on}", how="inner")'
                )

            # RENAME
            elif isinstance(step, Rename):
                code_lines.append(
                    f'{alias} = {alias}.rename(columns={{"{step.old_name}": "{step.new_name}"}})'
                )

            # SELECT
            elif isinstance(step, Select):
                if step.columns and len(step.columns) > 0:
                    cols_str = ", ".join([f'"{c}"' for c in step.columns])
                    code_lines.append(f"{alias} = {alias}[[{cols_str}]]")
                else:
                    code_lines.append("# ⚠️ Skipped SELECT (no columns specified)")

            # EMIT
            elif isinstance(step, Emit):
                code_lines.append(f'{alias}.to_csv(r"{step.path}", index=False)')
                code_lines.append(f'print("📂 Output written to {step.path}")')

        pipeline_outputs[pipe.name] = alias

    with open("generated_pipeline.py", "w", encoding="utf-8") as f:
        f.write("\n".join(code_lines))

    print("✅ Code generation completed: generated_pipeline.py created successfully.")
