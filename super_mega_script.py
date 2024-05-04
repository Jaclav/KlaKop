from pydub import AudioSegment
from scipy.fft import fft
import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile
from scipy.spatial.distance import pdist, squareform


sample_rate, data = wavfile.read(r'kop6.wav')

data = data[:,0]

# Remove negative data
data = np.abs(data.astype(np.int32))

clipping_indices = np.where(np.abs(data) == np.iinfo(np.int16).max)[0]

indices_500_away = []

temp_array = []

for i in range(len(clipping_indices)):
    if i == 0:
        continue
    if abs(clipping_indices[i] - clipping_indices[i-1]) <= 500:
        temp_array.append(clipping_indices[i])
    else:
        indices_500_away.append(temp_array)
        temp_array = []

indices_500_away.append(temp_array)

# Calculate the average of each sub-array
averages = [np.mean(sub_array) for sub_array in indices_500_away]

# Flatten the list of averages into a single numpy array
averages_flat = np.array(averages)

# Convert to int for indexing
averages_flat = averages_flat.astype(int)

av = averages_flat / sample_rate

differences = np.diff(av)

differences = [differences[i] for i in range(len(differences)) if np.abs(differences[i]) < 0.06 and np.abs(differences[i]) > 0.05]
#print(differences)

expected_value = np.mean(differences)
standard_deviation = np.std(differences)

print(expected_value, standard_deviation, len(differences))

plt.hist(differences, bins=20)
plt.title('Histogram 6')
plt.xlabel('czas [s]')
plt.ylabel('ilość pomiarów')
plt.show()

# Plot
#plt.plot(data)
#plt.plot(averages_flat, np.full_like(averages_flat, np.iinfo(np.int16).max), 'ro')
#plt.show()