#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename="$1"

if [ -f "$filename" ]; then
    mybinary=$(echo "$filename" |  awk -F '/' '{print $NF}' | awk -F '.' '{print $1}')

    gcc -g "$filename" -o "$mybinary" 
    echo "A Binary file '$mybinary' has been created!\n"
else
    echo "Error: File '$filename' not found."
fi

