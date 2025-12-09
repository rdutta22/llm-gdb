# GDBINI: An LLM-GDB Tool

This project integrates the ability of a Large Language Model(LLM) with the GNU Debugger(GDB). It helps us understand and debug programs through root-cause analysis and potential fixes. This tool currently uses the tool calling method from Gemnini API to simulate the Model Cntext Protocol(MCP) and execute GDB commands to create a detailed report. 

## Requirements

1. Python 3.8 +
2. Gemini API Key: You can get this key from Google AI Studio
3. Python GenAI SDK

## Setup

```sh
# Step 1: Install all the needed packages with this command
pip3 install requirements.txt

# Step 2: Add the Gemini API Key to the variables.py file
GEMINI_API_KEY="..." # <- Enter your Gemini API key here

# Step 3: There are some example C files in tests/ dir
          You can create a binary from these files to use
chmod +x bin_script.sh
./bin_script.sh <path_to_c_file> # Creates a binary in the name of the file

```

## Run

```sh
# To run the llm agent
python3 run.py

# It will ask you to enter the binary file name
Enter the binary you want to debug: <binary_name>
```

## How it works

There is an MCP server and an MCP client. The MCP server hosts the GDB Session that provides an interface to send and input via the Gemini Tool abilities--which is the MCP client--and receive the raw output from the GNU Debugger. Each tool handler method parses the arguments from LLM call and calls the GDB method that are mapped with their corresponding `gdb commands`.


