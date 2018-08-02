"""
This demo script loads the annotations for a given audio file and plots them.
"""

from scipy.io import wavfile
import matplotlib.pyplot as plt
import json
import pprint
import matplotlib.patches as patches

ip_file = '2018-02-01_17-26-07_42.08_24.33_10_0.wav'
#ip_file = '2008-08-08_17-26-07_42.94_23.03_10_0.wav'
meta_data_file = 'demo_bat_data.json'

# read metadata
with open(meta_data_file) as da:
    meta_data = json.load(da)

# print metadata
ip_file_info = [mm for mm in meta_data['audio_files'] if mm['file_name'] == ip_file][0]
pprint.pprint(ip_file_info)

# get annotations
anns = [mm for mm in meta_data['annotations'] if mm['audio_file_id'] == ip_file_info['id']]
print(str(len(anns)) + ' annotations found')

# read audio file
_, audio = wavfile.read(ip_file)
tm_exp = float(ip_file_info['time_expansion_factor'])
sampling_rate = float(ip_file_info['sampling_rate'])

# create spectrogram and plot
plt.close('all')
plt.figure(0, figsize=(8, 4))
spec, freqs, tm, im_ax = plt.specgram(audio, Fs=sampling_rate, NFFT=512, noverlap=384)
plt.xlabel('time (secs)')
plt.ylabel('frequency (hertz)')
plt.title(ip_file)

# plot the bounding boxes
for aa in anns:
    height = (aa['bbox'][3]-aa['bbox'][2])*1000
    width = aa['bbox'][1]-aa['bbox'][0]
    rect = patches.Rectangle((aa['bbox'][0],aa['bbox'][2]*1000), width, height,
           linewidth=2,edgecolor='b',facecolor='none')
    plt.gca().add_patch(rect)

plt.show()


