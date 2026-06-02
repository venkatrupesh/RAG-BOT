# Local Code Execution Service
import sys
from io import StringIO
from typing import Dict, Any
import html

class CodeExecutor:
    """Execute Python code locally"""
    
    def __init__(self):
        pass
    
    def execute_code(self, code: str, language: str, stdin: str = "") -> Dict[str, Any]:
        """Execute code locally (Python only)"""
        
        # Decode HTML entities if present
        code = html.unescape(code)
        
        # Only Python is supported
        if language.lower() != "python":
            return {
                "success": False,
                "output": "",
                "error": f"{language.title()} is not supported. Please select Python.",
                "time": 0,
                "memory": 0
            }
        
        old_stdout = sys.stdout
        old_stdin = sys.stdin
        
        try:
            sys.stdout = StringIO()
            # Ensure stdin has newline for input() to work
            stdin_str = str(stdin) if not stdin or str(stdin).endswith('\n') else str(stdin) + '\n'
            sys.stdin = StringIO(stdin_str)
            
            exec(code, {"__builtins__": __builtins__})
            output = sys.stdout.getvalue()
            
            return {
                "success": True,
                "output": output.strip(),
                "error": "",
                "time": 0,
                "memory": 0
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "time": 0,
                "memory": 0
            }
        finally:
            sys.stdout = old_stdout
            sys.stdin = old_stdin
    
    def run_test_cases(self, code: str, language: str, test_cases: list) -> Dict[str, Any]:
        """Run code against multiple test cases"""
        results = {
            "total": len(test_cases),
            "passed": 0,
            "failed": 0,
            "test_results": []
        }
        
        for i, test_case in enumerate(test_cases):
            result = self.execute_code(
                code=code,
                language=language,
                stdin=str(test_case.get("input", ""))
            )
            
            expected = str(test_case.get("expected_output", "")).strip()
            actual = str(result.get("output", "")).strip()
            
            passed = result["success"] and actual == expected
            
            if passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
            
            results["test_results"].append({
                "test_case": i + 1,
                "input": str(test_case.get("input", "")),
                "expected": expected,
                "actual": actual,
                "passed": passed,
                "error": result.get("error", ""),
                "time": 0,
                "memory": 0
            })
        
        return results
