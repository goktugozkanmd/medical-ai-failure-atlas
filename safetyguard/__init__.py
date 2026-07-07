"""
SafetyGuard — MedFailBench safety evaluation package.

Quickly test any OpenAI-compatible model against MedFailBench clinical safety
scenarios. Use as a CLI tool or import programmatically.

CLI:
    safetyguard eval --model gpt-4o --endpoint https://api.openai.com/v1
    safetyguard compare --runs ./outputs/

Python:
    from safetyguard.cli import eval_command, compare_command
"""

__version__ = "0.1.0"
