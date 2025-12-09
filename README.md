# LLaDebug: An LLM-GDB Tool (prounounced: Ladybug)

This project integrates the ability of a Large Language Model(LLM) with the GNU Debugger(GDB). It helps us understand and debug programs through root-cause analysis and potential fixes. This tool currently uses the tool calling method from Gemnini API to simulate the Model Cntext Protocol(MCP) and execute GDB commands to create a detailed report. 

## Requirements

1. Python 3.8+
2. Gemini API Key: You can get this key from Google AI Studio
3. Python GenAI SDK

## Setup

```sh
# Step 1: Create a virtual environment

python3 -venv <venv_name>

# Step 2: Install all the needed packages with this command

pip3 install requirements.txt

# Step 3: Add the Gemini API Key to the variables.py file

GEMINI_API_KEY="..." # <- Enter your Gemini API key here

# Step 4: There are some example C files in tests/ dir
#         You can create a binary from these files to use

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

## What has been achieved and how it works

There is an MCP server and an MCP client. The MCP server hosts the GDB Session that provides an interface to send an input via the Gemini Tool abilities--which is the MCP client--and receive the raw output from the GNU Debugger. Each tool handler method parses the arguments from LLM call and calls the GDB method that are mapped with their corresponding `gdb commands`.


## Example Run:
```sh
python3 run.py

# ./bin_script.sh tests/run.c
# Creates a 'run' binary in the home dir

Enter the binary you want to debug: run

=== Gemini answer ===

Execution Summary: The program /home/.../cse598/llm_gdb/run was executed with the argument "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA". This
input caused a Segmentation fault (SIGSEGV) at memory address 0x00000000004011fb within the vulnerable_function defined in tests/run.c
at line 15.

Root-Cause Analysis: The backtrace clearly shows the vulnerable_function received user_input consisting of 31 'A' characters. Inside
this function, a local buffer variable is identified as containing 16 'A's. The crucial piece of evidence is frame #1 in the backtrace,
which points to 0x0041414141414141. The hexadecimal value 0x41 corresponds to the ASCII character 'A'. This indicates that the extensive
input of 'A's (31 characters) overflowed the buffer (which seems to be 16 bytes), overwriting the saved return address on the stack with
the 'A' characters. When the vulnerable_function attempted to return, it tried to jump to the corrupted address 0x0041414141414141,
which is an invalid memory location, leading to the segmentation fault.

Vulnerability Type: Stack-based Buffer Overflow.

Proposed Fix: The root cause is an unbounded copy operation into a fixed-size buffer on the stack. To fix this, the program must ensure
that data copied into the buffer never exceeds its allocated size.

 1 Use Bounded String Copying Functions: Replace unsafe functions like strcpy, strcat, or sprintf with their safer, length-checked
   alternatives.
    • For copying strings, strncpy is recommended.
    • For formatting strings, snprintf is recommended.
 2 Input Validation: Always validate the length of user-supplied input before attempting to copy it into a buffer. Truncate or reject
   input that exceeds the buffer's capacity.

Example using strncpy to fix the vulnerability (assuming BUFFER_SIZE is the actual size of the buffer in vulnerable_function):

 #define BUFFER_SIZE 16 // Or the actual defined size of the buffer

 void vulnerable_function(const char* user_input) {
     char buffer[BUFFER_SIZE];

     // Ensure user_input length does not exceed buffer capacity
     // strncpy copies at most (BUFFER_SIZE - 1) characters
     strncpy(buffer, user_input, BUFFER_SIZE - 1);
     buffer[BUFFER_SIZE - 1] = '\0'; // Manually null-terminate to prevent issues

     // ... rest of the function logic
 }
=====================
```
## Limitations and Proposed Improvements

The initial plan was to implement a (Read-Eval-Print-Loop) REPL-chat like
interface from the mcp_client side, so we can keep asking the LLM to continue
evaluation with user input prompts. The challenge to implement this chat-like
functionality came in the form of exhausted quota of API calls, and a 'set up
biling' option, which I decided not to pursue.

I did try to use Mistral 7B API, if in any case I get an extended quota of API
calls. But alas, the Mistral API was not advanced enough to run and analyze any
binaries.

It would be fruitful to extend the functionality of this LLM-GDB interface to a
more chat-like structure in the future. It would definitely help with debugging
more on the spot through responsive prompts to the LLM API.


## References

[1] The starter code for MCP client and server communication was built using
    GenAI (ChatGPT). It was also used for debugging purposes and adding some
    more tool ability methods from the server end.

[2] https://modelcontextprotocol.io/docs/

[3] https://aistudio.google.com/
