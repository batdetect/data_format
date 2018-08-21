"""
This script loads the annotations for a given audio file and plots them.
"""

from scipy.io import wavfile
import matplotlib.pyplot as plt
import json
import pprint
import matplotlib.patches as patches

# choose from one of two different files to display
#ip_file = '2018-02-01_17-26-07_42.08_24.33_10_0.wav'
ip_file = '2008-08-08_17-26-07_42.94_23.03_10_0.wav'

meta_data_file = ip_file[:-3] + 'json'

# read metadata
with open(meta_data_file) as da:
    meta_data = json.load(da)

# print metadata
pprint.pprint(meta_data['audio_file'])

# get annotations
print(str(len(meta_data['annotation']['bboxes'])) + ' bounding boxes found')

# read audio file
sampling_rate, audio = wavfile.read(ip_file)
sampling_rate = float(meta_data['audio_file']['time_expansion_factor'])*sampling_rate

# create spectrogram and plot
plt.close('all')
plt.figure(0, figsize=(8, 4))
spec, freqs, tm, im_ax = plt.specgram(audio, Fs=sampling_rate, NFFT=512, noverlap=384)
plt.xlabel('time (secs)')
plt.ylabel('frequency (hz)')
plt.title(ip_file)

# plot the bounding boxes
for bb in meta_data['annotation']['bboxes']:
    height = (bb[3]-bb[2])*1000
    width = bb[1]-bb[0]
    rect = patches.Rectangle((bb[0],bb[2]*1000), width, height,
           linewidth=2,edgecolor='b',facecolor='none')
    plt.gca().add_patch(rect)

plt.show()
