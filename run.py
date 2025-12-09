#!/usr/bin/env python3

import subprocess
import sys
import signal
import os
from variables import *


def main():
    binary_path = input("Enter the binary you want to debug: ").strip()
    # prompt = input("Do you want to ask something specific?: ").strip()

    env = os.environ.copy()
    env["GEMINI_API_KEY"] = GEMINI_API_KEY
    
    if not binary_path:
        print("[ERROR]: No binary provided!")
        sys.exit(1)
    
    if not os.path.isfile(binary_path):
        print(f"[ERROR]: The binary path {binary_path} does not exist")
        sys.exit(1)


    subprocess.run(
            [sys.executable, 'mcp_gemini_client.py', binary_path],
        env=env,
    )

if __name__ == "__main__":
    main()
