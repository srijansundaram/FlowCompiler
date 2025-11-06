# semantic.py — validates logical consistency between Flow code and data

import pandas as pd
import difflib
from flowc.ast_nodes import Load, Pipeline, Filter, Sum, GroupBy, Average, DropDuplicates, SortBy, Emit, Ensure, Join, Rename, Select

def validate_semantics(load, pipelines):

    dataset_map = {}

    loads = load if isinstance(load, list) else [load]

    for ld in loads:
        try:
            df = pd.read_csv(ld.path)
            dataset_map[ld.alias] = df
        except FileNotFoundError:
            raise Exception(f"❌ File not found: {ld.path}")
        except Exception as e:
            raise Exception(f"❌ Unable to load dataset '{ld.path}': {e}")

    for pipe in pipelines:
        for step in pipe.steps:
            alias = list(dataset_map.keys())[0]
            df = dataset_map.get(alias)

            if isinstance(step, (Filter, Sum, GroupBy, Average, DropDuplicates, SortBy, Ensure, Rename, Select)):
                if hasattr(step, 'column') and step.column:
                    if step.column not in df.columns:
                        
                        suggestion = difflib.get_close_matches(step.column, df.columns, n=1, cutoff=0.6)
                        if suggestion:
                            raise Exception(
                                f"❌ Semantic Error: Column '{step.column}' not found in dataset '{alias}'. Did you mean '{suggestion[0]}'?"
                            )
                        else:
                            raise Exception(
                                f"❌ Semantic Error: Column '{step.column}' not found in dataset '{alias}'."
                            )

                if hasattr(step, 'columns') and step.columns:
                    for col in step.columns:
                        if col not in df.columns:
                            suggestion = difflib.get_close_matches(col, df.columns, n=1, cutoff=0.6)
                            if suggestion:
                                raise Exception(
                                    f"❌ Semantic Error: Column '{col}' not found in dataset '{alias}'. Did you mean '{suggestion[0]}'?"
                                )
                            else:
                                raise Exception(
                                    f"❌ Semantic Error: Column '{col}' not found in dataset '{alias}'."
                                )

            elif isinstance(step, Join):
                other_alias = step.other_alias
                if other_alias not in dataset_map:
                    raise Exception(f"❌ Semantic Error: Join target '{other_alias}' not loaded.")
                if step.on not in df.columns:
                    suggestion = difflib.get_close_matches(step.on, df.columns, n=1, cutoff=0.6)
                    if suggestion:
                        raise Exception(
                            f"❌ Semantic Error: Join column '{step.on}' not found in '{alias}'. Did you mean '{suggestion[0]}'?"
                        )
                    else:
                        raise Exception(
                            f"❌ Semantic Error: Join column '{step.on}' not found in '{alias}' dataset."
                        )

    print("✅ Semantic validation passed successfully.\n")
