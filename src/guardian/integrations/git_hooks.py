PRE_COMMIT_HOOK = '''#!/usr/bin/env python3
# QualiGuard pre-commit hook
import subprocess, sys

result = subprocess.run(["qg", "scan", "--format", "terminal"], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    sys.exit(1)
'''


def install_pre_commit(target_dir: str = ".git/hooks") -> str:
    import os
    hook_path = os.path.join(target_dir, 'pre-commit')
    with open(hook_path, "w") as f:
        f.write(PRE_COMMIT_HOOK)
    os.chmod(hook_path, 0o755)
    return hook_path
