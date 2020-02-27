from scipy.io import wavfile
from pylab import *
from scipy import *
import sys

maleMinMax=[60,160]
femaleMinMax=[180,270]

def HPS(rate, Voice):
    if shape(Voice[0])==(2,):
        Voice=Voice[:, 0]
    T = len(Voice)/rate
    partLen=int(rate)
    parts = [ Voice[i*partLen:(i+1)*partLen] for i in range(int(T))]
    resultParts = []
    for data in parts:
        if(len(data)==0): continue
        window = np.hamming(len(data))
        data = data*window
        fftV = abs(fft(data))/rate
        fftR = copy(fftV)
        for i in range(2,5):
            tab = copy(fftV[::i])
            fftR = fftR[:len(tab)]
            fftR *= tab
        resultParts.append(fftR)
    result = [0]*len(resultParts[int(len(resultParts)/2)])
    for res in resultParts:
        if(len(res)!=len(result)): continue
        result += res
    if(sum(result[maleMinMax[0]:maleMinMax[1]]) > sum(result[femaleMinMax[0]:femaleMinMax[1]])): return 'M'
    return 'K'


if __name__ == "__main__":
    rate, array = wavfile.read(sys.argv[1])
    print(HPS(rate, array))


