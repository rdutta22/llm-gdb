#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename="$1"

if [ -f "$filename" ]; then
    gcc -g "$filename" -o binary
    echo "A Binary '$filename' has been created!\n"
else
    echo "Error: File '$filename' not found."
fi

