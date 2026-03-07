import subprocess

print("\nSIDEGUY AUTONOMOUS BUILD\n")

subprocess.run(["python3", "tools/build-orchestrator/build_orchestrator.py"])

print("\nSystem build cycle finished\n")
