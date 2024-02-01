#!/bin/bash

# Function to check if a specific sink exists
sink_exists() {
    pactl list sinks short | grep -q "$1"
}

# Check if PulseAudio is running, if not, start it
if ! pulseaudio --check; then
    echo "Starting PulseAudio..."
    pulseaudio --start

    # Wait a bit and check again if PulseAudio started
    sleep 2
    if ! pulseaudio --check; then
        echo "Failed to start PulseAudio."
        exit 1
    fi
fi

# Check if the sinks already exist
if ! sink_exists "Music_Sink"; then
    pactl load-module module-null-sink sink_name=Music_Sink sink_properties=device.description=Music_Sink
fi

if ! sink_exists "baresip_sink"; then
    pactl load-module module-null-sink sink_name=baresip_sink sink_properties=device.description="Baresip_Sink"
fi

# Check if the virtual mic source exists
if ! pactl list sources short | grep -q "Virtual_Mic_for_Music"; then
    pactl load-module module-remap-source master=Music_Sink.monitor source_name=Virtual_Mic_for_Music source_properties=device.description=Virtual_Mic_for_Music
fi

echo "Setup complete."
