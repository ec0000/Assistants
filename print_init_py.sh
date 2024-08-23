#!/bin/bash

# Check if a directory is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Function to process __init__.py files
process_init_file() {
    local file="$1"
    local relative_path="${file#$2/}"
    
    echo "# $relative_path"
    cat "$file"
    echo ""  # Add a blank line for readability
}

# Find all __init__.py files in the specified directory and its subdirectories
find "$1" -type d -not -path '*/\.*' | while read -r dir; do
    init_file="$dir/__init__.py"
    if [ -f "$init_file" ]; then
        process_init_file "$init_file" "$1"
    fi
done
