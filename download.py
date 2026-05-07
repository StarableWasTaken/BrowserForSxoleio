import subprocess
import sys

packages = ["PyQt5", "PyQtWebEngine"]

for package in packages:
    print(f"Installing {package}...")
    
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        package
    ])

print("\nEverything installed successfully")
