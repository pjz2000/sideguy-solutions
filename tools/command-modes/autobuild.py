import subprocess

print("\nSIDEGUY AUTO BUILD MODE\n")

subprocess.run("python3 tools/auto-builder/run_builder.py", shell=True)

print("\nAuto build finished\n")
