#!/bin/bash

# Directory containing the subdirectories
parent_dir="common"

# Postfix to add to the output files
postfix="_processed"

# Highpass filter cutoff frequency (e.g., 100 Hz)
highpass_freq=100

# Lowpass filter cutoff frequency (less than 4000 Hz for 8000 Hz sample rate)
lowpass_freq=3999

# Volume reduction factor for loud sections (e.g., -6dB)
volume_reduction="-6dB"
target_duration=60

# Iterate over each subdirectory in the 'common' directory
for subdir in "$parent_dir"/*/; do
    echo "Processing directory: $subdir"

    # Path of the original and output files
    input_file="${subdir}wait.wav"
    output_file="${subdir}wait${postfix}.wav"

    # Check if the input file exists
    if [ -f "$input_file" ]; then
        # Apply the Sox command with highpass, lowpass filters, and volume reduction
        sox "$input_file" -t wav "$output_file" highpass $highpass_freq lowpass $lowpass_freq vol $volume_reduction
        ffmpeg -i "$input_file" -t "$target_duration" "$output_file"

        echo "Processed: $output_file"
    else
        echo "No 'wait.wav' in $subdir"
    fi
done

echo "Processing complete."
