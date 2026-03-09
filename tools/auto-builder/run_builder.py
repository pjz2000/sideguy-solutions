import subprocess

print("\nSIDEGUY AUTO BUILDER\n")

subprocess.run("python3 tools/auto-builder/gravity_builder.py", shell=True)

print("\nAuto build complete\n")
