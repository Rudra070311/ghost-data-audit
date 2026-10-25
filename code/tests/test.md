# Test Execution Guide

To execute the test suite completely, set the `PYTHONPATH` variable to target your configuration's `code/` folder path. Use the command matching your operating system terminal below:

## KEEP AS PER YOUR OS

### Windows (PowerShell)

```powershell
\$env:PYTHONPATH="C:\Users\rudra\OneDrive\Documents\VS_Code\ghost-data-auditor\code"
python -m pytest code/tests/
```

### Windows (Command Prompt - CMD)

```cmd
set PYTHONPATH=C:\Users\rudra\OneDrive\Documents\VS_Code\ghost-data-auditor\code
python -m pytest code/tests/
```

### Linux / macOS (Bash/Zsh Terminal)

```bash
export PYTHONPATH="/Users/rudra/OneDrive/Documents\VS_Code\ghost-data-auditor\code"
python3 -m pytest code/tests/
```

#### Latest Output

PS C:\Users\rudra\OneDrive\Documents\VS_Code\ghost-data-auditor> $env:PYTHONPATH="C:\Users\rudra\OneDrive\Documents\VS_Code\ghost-data-auditor\code"
>> python -m pytest code/tests/
============================== test session starts ==============================
platform win32 -- Python 3.14.0, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\rudra\OneDrive\Documents\VS_Code\ghost-data-auditor
plugins: anyio-4.13.0, asyncio-1.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 9 items

code\tests\test_decision.py ..                                             [ 22%]
code\tests\test_identity.py .                                              [ 33%]
code\tests\test_loader.py ...                                              [ 66%]
code\tests\test_output.py .                                                [ 77%]
code\tests\test_policy.py .                                                [ 88%]
code\tests\test_resurrection.py .                                          [100%]

=============================== 9 passed in 0.15s ===============================
