import numpy as np
import sounddevice as sd

# Generate initial noise
def generate_initial_noise(length):
    return np.random.uniform(-1, 1, size=length)

# Karplus-Strong algorithm implementation
def karplus_strong(frequency, duration, decay_factor):
    samples = int(duration * 44100)  # Assuming a sample rate of 44100 Hz
    buffer_length = int(44100 / frequency)
    buffer = generate_initial_noise(buffer_length)
    output = np.zeros(samples)

    for i in range(samples):
        current_sample = buffer[0]
        output[i] = current_sample
        buffer[0:-1] = buffer[1:]
        buffer[-1] = decay_factor * 0.5 * (buffer[0] + buffer[1])

    return output

# Calculate frequency from MIDI note number
def calculate_frequency(note_number, tuning_frequency):
    return tuning_frequency * 2 ** ((note_number - 69) / 12)

# Parameters
tuning_frequency = 440.0  # A4 tuning frequency in Hz
duration = 3.0  # Duration of generated sound in seconds
decay_factor = 0.995  # Decay factor

while True:
    try:
        user_input = input("Enter a MIDI note number (or 'q' to quit): ")
        if user_input == 'q':
            break

        note_number = int(user_input)
        if note_number < 0 or note_number > 127:
            print("Invalid MIDI note number. Please enter a number between 0 and 127.")
            continue

        frequency = calculate_frequency(note_number, tuning_frequency)
        samples = karplus_strong(frequency, duration, decay_factor)
        sd.play(samples, blocking=False)

    except ValueError:
        print("Invalid input. Please enter a valid MIDI note number.")
