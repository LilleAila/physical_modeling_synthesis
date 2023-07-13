import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import butter, lfilter

# Generate initial noise
def generate_initial_noise(length):
    return np.random.uniform(-1.15, 1.15, size=length)

# Apply an ADSR envelope to the samples
def apply_adsr_envelope(samples, attack_time, decay_time, sustain_level, release_time, sample_rate):
    num_samples = len(samples)
    attack_samples = int(attack_time * sample_rate)
    decay_samples = int(decay_time * sample_rate)
    release_samples = int(release_time * sample_rate)
    release_start_sample = num_samples - release_samples

    envelope = np.zeros(num_samples)
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain_level, decay_samples)
    envelope[release_start_sample:] = np.linspace(sustain_level, 0, release_samples)

    return samples * envelope

# Apply a low-pass filter to the samples
def apply_low_pass_filter(samples, cutoff_frequency, sample_rate):
    nyquist_frequency = 0.5 * sample_rate
    normalized_cutoff = cutoff_frequency / nyquist_frequency
    b, a = butter(4, normalized_cutoff, btype='lowpass')
    filtered_samples = lfilter(b, a, samples)

    return filtered_samples

# Karplus-Strong algorithm
# https://en.wikipedia.org/wiki/Karplus–Strong_string_synthesis
def karplus_strong(frequency, duration, decay_factor, attack_time, decay_time, sustain_level, release_time,
                   cutoff_frequency, stretch_factor, use_adsr=True, use_low_pass_filter=True):
    sample_rate = 44100  # Assuming a sample rate of 44100 Hz
    samples = int(duration * sample_rate)
    buffer_length = int(sample_rate / (frequency * stretch_factor))
    buffer = generate_initial_noise(buffer_length)
    output = np.zeros(samples)

    for i in range(samples):
        current_sample = buffer[0]
        output[i] = current_sample
        buffer[0:-1] = buffer[1:]
        buffer[-1] = decay_factor * 0.5 * (buffer[0] + buffer[1])

    if use_adsr:
        output = apply_adsr_envelope(output, attack_time, decay_time, sustain_level, release_time, sample_rate)

    if use_low_pass_filter:
        output = apply_low_pass_filter(output, cutoff_frequency, sample_rate)

    return output

# Function to calculate frequency from MIDI note number
def calculate_frequency(note_number, tuning_frequency):
    return tuning_frequency * 2 ** ((note_number - 69) / 12)

## Parameters
tuning_frequency = 440.0  # A4 tuning frequency in Hz
duration = 3.0  # Duration of generated sound in seconds
decay_factor = 0.995  # Decay factor for the Karplus-Strong algorithm
stretch_factor = 1.0  # Stretch factor to adjust the duration of the generated sound

### ADSR Envelope
apply_adsr = True
attack_time = 0.0  # Attack time for the ADSR envelope in seconds
decay_time = 1.5  # Decay time for the ADSR envelope in seconds
sustain_level = 0.5  # Sustain level for the ADSR envelope
release_time = 0.3  # Release time for the ADSR envelope in seconds

### Low-Pass Filter
apply_low_pass = False
cutoff_frequency = 2650.0  # Cutoff frequency for the low-pass filter in Hz

i = 4

# Infinite loop to generate, play, and save samples
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
        samples = karplus_strong(frequency, duration, decay_factor, attack_time, decay_time,
                                 sustain_level, release_time, cutoff_frequency, stretch_factor,
                                 use_adsr=apply_adsr, use_low_pass_filter=apply_low_pass)
        sd.play(samples, blocking=False)
        # sf.write("output/n" + str(i) + ".wav", samples, samplerate=44100)
        i += 1

    except ValueError:
        print("Invalid input. Please enter a valid MIDI note number.")
