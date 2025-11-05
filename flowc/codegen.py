# Code generator (Pandas backend) for the Flow programming language.

from flowc.ast_nodes import Filter, Sum, GroupBy, Average, DropDuplicates, SortBy, Emit, Ensure, Join, Rename, Select

def generate_pandas_code(loads, pipelines):
    code_lines = []
    code_lines.append("import pandas as pd\n")

    # Load all datasets first
    for ld in loads:
        code_lines.append(f'{ld.alias} = pd.read_csv(r"{ld.path}")')

    code_lines.append("")

    for pipe in pipelines:
        current_alias = getattr(pipe, "base_alias", None) or loads[0].alias

        for step in pipe.steps:
            # ---------- FILTER ----------
            if isinstance(step, Filter):
                code_lines.append(f'{current_alias} = {current_alias}.query("{step.expr}")')

            # ---------- SUM ----------
            elif isinstance(step, Sum):
                code_lines.append(f'{current_alias} = pd.DataFrame([{current_alias}["{step.column}"].sum()], columns=["{step.alias}"])')

            # ---------- GROUP BY ----------
            elif isinstance(step, GroupBy):
                code_lines.append(f'{current_alias} = {current_alias}.groupby("{step.column}").sum().reset_index()')

            # ---------- AVERAGE ----------
            elif isinstance(step, Average):
                code_lines.append(f'{current_alias} = pd.DataFrame([{current_alias}["{step.column}"].mean()], columns=["{step.alias}"])')

            # ---------- DROP DUPLICATES ----------
            elif isinstance(step, DropDuplicates):
                code_lines.append(f'{current_alias} = {current_alias}.drop_duplicates(subset="{step.column}")')

            # ---------- SORT BY ----------
            elif isinstance(step, SortBy):
                code_lines.append(f'{current_alias} = {current_alias}.sort_values("{step.column}", ascending={step.ascending})')

            # ---------- ENSURE ----------
            elif isinstance(step, Ensure):
                code_lines.append(f'assert ({step.condition}), "Ensure failed: {step.condition}"')

            # ---------- JOIN ----------
            elif isinstance(step, Join):
                code_lines.append(
                    f'{current_alias} = {current_alias}.merge({step.other_alias}, on="{step.on}", suffixes=("", "_right"))'
                )
                code_lines.append(
                    f'{current_alias}.columns = [c.replace("_right", "") for c in {current_alias}.columns]'
                )

            # ---------- SELECT ----------
            elif isinstance(step, Select):
                columns_str = ", ".join([f'"{c}"' for c in step.columns])
                code_lines.append(f'{current_alias} = {current_alias}[[{columns_str}]]')

            # ---------- RENAME ----------
            elif isinstance(step, Rename):
                code_lines.append(f'{current_alias} = {current_alias}.rename(columns={{"{step.old_name}": "{step.new_name}"}})')

            # ---------- EMIT ----------
            elif isinstance(step, Emit):
                code_lines.append(f'{current_alias}.to_csv(r"{step.path}", index=False)')

    with open("generated_pipeline.py", "w") as f:
        f.write("\n".join(code_lines))
