import librosa
import soundfile as sf
import numpy as np
#import os


# THIS CODE MIXES 2 SONGS TOGETHER
# IT BPM MATCHES THEM, DOES A CROSSFADE, ADDS REVERB AND EXPORTS THE FINAL AUDIO


# WRITE THE SONG FILE NAMES HERE

track1_path = "track1.wav"

track2_path = "track2.wav"


# USER INPUTS

track2_start = float(input("Start Track 2 from second: "))

transition = float(input("Crossfade starts at second: "))

crossfade = float(input("Crossfade duration: "))

# ERROR CHECKING

if crossfade <= 0:

    print("Error: Crossfade duration must be greater than 0")

    exit()

if transition <= 0:

    print("Error: Transition time must be greater than 0")

    exit()

if track2_start < 0:

    print("Error: Track 2 start time cannot be negative")

    exit()

# LOAD SONGS

track1, sr = librosa.load(track1_path, sr=None, mono=True)

track2, sr2 = librosa.load(track2_path, sr=None, mono=True)

if sr != sr2:
    print("Warning: Different sample rates detected")
else:
    print("Sample Rate =", sr)


if transition > len(track1) / sr:

    print("Error: Transition point is longer than Track 1")

    exit()

if track2_start > len(track2) / sr:

    print("Error: Track 2 start point is longer than Track 2")

    exit()

# BPM DETECTION


# AI was used in this section

# librosa estimates the BPM of both tracks
# this is used so both songs match tempo before merging

tempo1, _ = librosa.beat.beat_track(y=track1, sr=sr)

tempo2, _ = librosa.beat.beat_track(y=track2, sr=sr)

#tempo1 = float(tempo1[0])
tempo1 = float(np.atleast_1d(tempo1)[0])

tempo2 = float(np.atleast_1d(tempo2)[0])
#tempo2 = float(tempo2[0])

print("Track 1 BPM =", round(tempo1, 1))

print("Track 2 BPM =", round(tempo2, 1))


# BPM MATCHING


# AI was used in this section

# stretches track 2 so its BPM matches track 1

stretch_rate = tempo2 / tempo1

track2 = librosa.effects.time_stretch(track2, rate=stretch_rate)

print("Track 2 BPM matched")


# RMS VOLUME MATCHING
# RMS gives an estimate of loudness
# this makes both songs closer in volume before mixing

rms1 = np.sqrt(np.mean(track1 ** 2))

rms2 = np.sqrt(np.mean(track2 ** 2))

track2 = track2 * (rms1 / rms2)


# CONVERT SECONDS to SAMPLES

# lecture notes explain audio as arrays
# sample rate tells us how many array positions exist per second

track2_start_s = int(track2_start * sr)

transition_s = int(transition * sr)

crossfade_s = int(crossfade * sr)


# TRIM TRACK 2

# removes the start of track 2
# lets the user pick where the song should begin

track2 = track2[track2_start_s:]


# FADE DOWN TRACK 1

# lecture notes mention fade effects
# this lowers track 1 volume before transition

dip_time = 5

dip_samples = int(dip_time * sr)

dip = np.linspace(1, 0.4, dip_samples)

dip_start = transition_s - dip_samples

track1[dip_start : transition_s] *= dip


# FADE UP TRACK 2

# gradually increases volume of track 2
# helps make the transition smoother

rise_time = 5

rise_samples = int(rise_time * sr)

rise = np.linspace(0.4, 1, rise_samples)

track2[:rise_samples] *= rise


# SLICE SONG PARTS

# splitting the songs into sections before merging

part1 = track1[:transition_s + crossfade_s]

part2 = track2[transition_s:]


# CROSSFADE

# lecture notes mention fade in + fade out
# this combines both ideas together

fade_out = np.linspace(1, 0, crossfade_s)

fade_in = np.linspace(0, 1, crossfade_s)

part1[-crossfade_s:] *= fade_out

part2[:crossfade_s] *= fade_in

crossfade_part = (part1[-crossfade_s:] + part2[:crossfade_s])


# MERGE SONG PARTS

# numpy concatenate joins arrays together

final_song = np.concatenate([part1[:-crossfade_s], crossfade_part, part2[crossfade_s:]])


# REVERB
# reverb is basically many tiny echoes together, this is how i implemented it, 
# by adding many quiet delayed copies of the song to itself 
# this is a very basic reverb but it worked well for this project and was simpleest to implement
reverb_delay = 0.08

reverb_strength = 0.45

reverb_repeat = 6

delay_samples = int(reverb_delay * sr)

outsong = np.copy(final_song)

for repeat in range(1, reverb_repeat + 1):

    start = delay_samples * repeat

    volume = reverb_strength / repeat

    for i in range(start, len(final_song)):

        outsong[i] = (outsong[i] + final_song[i - start] * volume)


# PREVENT CLIPPING


# AI was used in this section

# audio values above 1 or below -1 distort badly
# this rescales the whole song if needed

max_amp = np.max(np.abs(outsong))

if max_amp > 1:

    outsong = outsong / max_amp


# OUTPUT FILE

output_name = input("Enter Output File Name: ")

sf.write(output_name, outsong, sr)

print("Saved", output_name)
