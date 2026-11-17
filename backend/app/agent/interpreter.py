import io
import sys
import traceback
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np

class CodeExecutionError(Exception):
    pass

class PythonInterpreter:
    """
    Sandboxed Python environment for executing data analysis code against in-memory DataFrames.
    Captures stdout, returned variables, and traceback for self-correction.
    """

    ALLOWED_MODULES = {
        "pd": pd,
        "pandas": pd,
        "np": np,
        "numpy": np,
    }

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def execute(self, code_str: str) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Executes code_str with `df` available.
        Returns:
            (success: bool, output_or_error: str, result_vars: dict)
        """
        # Clean markdown code blocks if the LLM provided them
        cleaned_code = code_str.strip()
        if cleaned_code.startswith("```python"):
            cleaned_code = cleaned_code[9:]
        elif cleaned_code.startswith("```"):
            cleaned_code = cleaned_code[3:]
        if cleaned_code.endswith("```"):
            cleaned_code = cleaned_code[:-3]
        cleaned_code = cleaned_code.strip()

        # Setup local execution context
        exec_globals = {
            "__builtins__": __builtins__,
            "df": self.df,
            "pd": pd,
            "pandas": pd,
            "np": np,
            "numpy": np,
        }
        exec_locals = {}

        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        try:
            exec(cleaned_code, exec_globals, exec_locals)
            sys.stdout = old_stdout
            stdout_str = redirected_output.getvalue().strip()

            # Collect results created in script
            # Prioritize 'result', 'output', 'summary', or 'fig_data'
            serializable_locals = {}
            for k, v in exec_locals.items():
                if k.startswith("_"):
                    continue
                if isinstance(v, (int, float, str, bool, list, dict)):
                    serializable_locals[k] = v
                elif isinstance(v, pd.DataFrame):
                    # Keep small summary preview
                    serializable_locals[k] = v.head(10).to_dict(orient="records")
                elif isinstance(v, pd.Series):
                    serializable_locals[k] = v.head(10).to_dict()
                elif isinstance(v, (np.integer, np.floating)):
                    serializable_locals[k] = v.item()

            final_output = stdout_str if stdout_str else "Code executed successfully with no print output."
            return True, final_output, serializable_locals

        except Exception as e:
            sys.stdout = old_stdout
            tb = traceback.format_exc()
            return False, f"{type(e).__name__}: {str(e)}\n\nTraceback:\n{tb}", {}
