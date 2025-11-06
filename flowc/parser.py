# Parser -> AST

import re
from .ast_nodes import (
    Load, Pipeline, Filter, Sum, GroupBy, Average, DropDuplicates,
    SortBy, Emit, Ensure, Join, Rename, Select
)

def parse_flow(src: str):
    lines = [ln.strip() for ln in src.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    loads = []
    pipelines = []
    cur_pipe = None

    for ln in lines:
        # ---------------- LOAD ----------------
        if ln.startswith("load"):
            m = re.match(r'load\s+"([^"]+)"\s+as\s+(\w+)', ln)
            if m:
                loads.append(Load(path=m.group(1), alias=m.group(2)))

        # ---------------- PIPELINE ----------------
        elif ln.startswith("pipeline"):
            name = ln.split()[1].rstrip(':')
            cur_pipe = Pipeline(name=name, steps=[])
            pipelines.append(cur_pipe)

        # ---------------- PIPELINE STEPS ----------------
        elif "|>" in ln:
            parts = ln.split("|>")
            if not parts or len(parts) < 2:
                continue

            cur_alias = parts[0].strip()
            step = parts[1].strip() if len(parts) > 1 else ""

            # Detect dependency
            if cur_pipe and cur_alias:
                existing_pipes = [p.name for p in pipelines if p != cur_pipe]
                if cur_alias in existing_pipes:
                    cur_pipe.depends_on = cur_alias
                if cur_pipe.base_alias is None:
                    cur_pipe.base_alias = cur_alias

            # Skip malformed steps
            if not step or len(step.split()) < 1:
                continue

            # Ensure pipeline has steps list
            if cur_pipe and not hasattr(cur_pipe, "steps"):
                cur_pipe.steps = []

            # ---------------- OPERATIONS ----------------
            if step.startswith("filter"):
                expr = step[len("filter"):].strip()
                cur_pipe.steps.append(Filter(expr=expr))

            elif step.startswith("sum"):
                m = re.match(r'sum (\w+)(?: as (\w+))?', step)
                if m:
                    column = m.group(1)
                    alias = m.group(2) if m.group(2) else m.group(1)
                    cur_pipe.steps.append(Sum(column=column, alias=alias))

            elif step.startswith("group_by"):
                m = re.match(r'group_by (\w+)', step)
                if m:
                    column = m.group(1)
                    cur_pipe.steps.append(GroupBy(column=column))

            elif step.startswith("average"):
                m = re.match(r'average (\w+)(?: as (\w+))?', step)
                if m:
                    column = m.group(1)
                    alias = m.group(2) if m.group(2) else m.group(1)
                    cur_pipe.steps.append(Average(column=column, alias=alias))

            elif step.startswith("dropduplicates"):
                parts = step.split()
                column = parts[1] if len(parts) > 1 else None
                cur_pipe.steps.append(DropDuplicates(column=column))

            elif step.startswith("sortby"):
                parts = step.split()
                if len(parts) > 1:
                    column = parts[1]
                    ascending = True
                    if len(parts) > 2 and parts[2].lower() == "desc":
                        ascending = False
                    cur_pipe.steps.append(SortBy(column=column, ascending=ascending))

            elif step.startswith("ensure"):
                condition = step[len("ensure"):].strip()
                cur_pipe.steps.append(Ensure(condition=condition))

            elif step.startswith("join"):
                m = re.match(r'join (\w+) on (\w+)', step)
                if m:
                    other = m.group(1)
                    on = m.group(2)
                    cur_pipe.steps.append(Join(other_alias=other, on=on))

            elif step.startswith("rename"):
                m = re.match(r'rename (\w+) to (\w+)', step)
                if m:
                    old_name = m.group(1)
                    new_name = m.group(2)
                    cur_pipe.steps.append(Rename(old_name=old_name, new_name=new_name))

            elif step.startswith("select"):
                cols = step[len("select"):].strip()
                if cols:
                    columns = [c.strip() for c in cols.split(",") if c.strip()]
                    cur_pipe.steps.append(Select(columns=columns))

            elif step.startswith("emit"):
                m = re.match(r'emit to "([^"]+)"', step)
                if m:
                    path = m.group(1)
                    cur_pipe.steps.append(Emit(path=path))

    return loads, pipelines
