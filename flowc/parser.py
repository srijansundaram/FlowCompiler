import re
from .ast_nodes import (
    Load, Pipeline, Filter, Sum, GroupBy, Average, DropDuplicates,
    SortBy, Emit, Ensure, Join, Rename, Select
)

def parse_flow(src: str):
    lines = [l.rstrip() for l in src.splitlines() if l.strip()]
    loads = []
    pipelines = []
    cur_pipe = None
    cur_alias = None

    for ln in lines:
        # ---------- LOAD ----------
        if ln.startswith("load"):
            m = re.match(r'load\s+"([^"]+)"\s+as\s+(\w+)', ln)
            if m:
                loads.append(Load(path=m.group(1), alias=m.group(2)))

        # ---------- PIPELINE ----------
        elif ln.startswith("pipeline"):
            name = ln.split()[1].rstrip(':')
            cur_pipe = Pipeline(name=name)
            pipelines.append(cur_pipe)
            cur_pipe.base_alias = None
            cur_alias = None

        # ---------- PIPELINE STEPS ----------
        elif "|>" in ln:
            # handle leading alias (like employees |> ...)
            parts = ln.split("|>")
            if len(parts) == 2 and parts[0].strip():
                cur_alias = parts[0].strip()
                step = parts[1].strip()
                if cur_pipe and cur_pipe.base_alias is None:
                    cur_pipe.base_alias = cur_alias
            else:
                step = ln.replace("|>", "").strip()

            # ---------- FILTER ----------
            if step.startswith("filter"):
                expr = step[len("filter"):].strip()
                cur_pipe.steps.append(Filter(expr=expr))

            # ---------- SUM ----------
            elif step.startswith("sum"):
                m = re.match(r'sum (\w+)(?: as (\w+))?', step)
                if m:
                    column = m.group(1)
                    alias = m.group(2) if m.group(2) else m.group(1)
                    cur_pipe.steps.append(Sum(column=column, alias=alias))

            # ---------- GROUP BY ----------
            elif step.startswith("group_by"):
                m = re.match(r'group_by (\w+)', step)
                if m:
                    column = m.group(1)
                    cur_pipe.steps.append(GroupBy(column=column))

            # ---------- JOIN ----------
            elif step.startswith("join"):
                parts = step.split()
                if len(parts) >= 4 and parts[2] == "on":
                    other_alias = parts[1]
                    on_column = parts[3]
                    cur_pipe.steps.append(Join(other_alias=other_alias, on=on_column))

            # ---------- DROP DUPLICATES ----------
            elif step.startswith("dropduplicates"):
                parts = step.split()
                column = parts[1] if len(parts) > 1 else None
                cur_pipe.steps.append(DropDuplicates(column=column))

            # ---------- SORT BY ----------
            elif step.startswith("sortby"):
                parts = step.split()
                column = parts[1]
                ascending = True
                if len(parts) > 2 and parts[2].lower() == "desc":
                    ascending = False
                cur_pipe.steps.append(SortBy(column=column, ascending=ascending))

            # ---------- AVERAGE ----------
            elif step.startswith("avg") or step.startswith("average"):
                m = re.match(r'(?:avg|average) (\w+)(?: as (\w+))?', step)
                if m:
                    column = m.group(1)
                    alias = m.group(2) if m.group(2) else m.group(1)
                    cur_pipe.steps.append(Average(column=column, alias=alias))

            # ---------- ENSURE ----------
            elif step.startswith("ensure"):
                condition = step[len("ensure"):].strip()
                cur_pipe.steps.append(Ensure(condition=condition))

            # ---------- RENAME ----------
            elif step.startswith("rename"):
                m = re.match(r'rename (\w+) to (\w+)', step)
                if m:
                    old_name = m.group(1)
                    new_name = m.group(2)
                    cur_pipe.steps.append(Rename(old_name=old_name, new_name=new_name))

            # ---------- SELECT ----------
            elif step.startswith("select"):
                cols = step[len("select"):].strip()
                columns = [c.strip() for c in cols.split(",")]
                cur_pipe.steps.append(Select(columns=columns))

            # ---------- EMIT ----------
            elif step.startswith("emit"):
                m = re.match(r'emit to "([^"]+)"', step)
                if m:
                    path = m.group(1)
                    cur_pipe.steps.append(Emit(path=path))

    return loads, pipelines
