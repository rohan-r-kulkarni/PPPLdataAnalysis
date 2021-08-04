import cdflib
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
from scipy.fft import fftshift, fftfreq, fft

files = []
files.append(["../20170810data/mms1/fgm/mms1_fgm_brst_l2_20170810121733_v5.99.0.cdf", "mms1_fgm_b_gsm_brst_l2"])
files.append(["../20170810data/mms2/fgm/mms2_fgm_brst_l2_20170810121733_v5.99.0.cdf", "mms2_fgm_b_gsm_brst_l2"])
files.append(["../20170810data/mms3/fgm/mms3_fgm_brst_l2_20170810121733_v5.99.0.cdf", "mms3_fgm_b_gsm_brst_l2"])
files.append(["../20170810data/mms4/fgm/mms4_fgm_brst_l2_20170810121733_v5.99.0.cdf", "mms4_fgm_b_gsm_brst_l2"])

def readvariables(vartype):
    """Sort data into lists, only meant for rVariables and zVariables.
    For vartype input r or z."""
    returnlist = [] #returns this list
    for i in file.cdf_info().get(vartype + "Variables"):
        try:
            print(i + " " + str(file.varinq(i).get("Last_Rec"))) #Print name of variable and number of records
            returnlist.append([])
            for j in range(file.varinq(i).get("Last_Rec")):
                returnlist[file.cdf_info().get(vartype + "Variables").index(i)].append(file.varget(i,startrec=j,endrec=j+1).tolist())
                #Append data to the right list and right index
        except ValueError:
            print("No records found") #In case there are no records
            continue
    return returnlist

def filenames_get(name_list_file):
  '''
  Pulls list of filenames I'm using from the file where they are stored.
  Allows some flexibility
  Inputs:
      name_list_file- string which constains the full path to the file which
          contains a list of the full filename paths needed
  Outputs:
      name_list- list of strings which contain the full path to
          each file
  '''
  name_list=[]
  with open(name_list_file,"r") as name_file_obj: #read-only access
       for line in name_file_obj:
           line_clean =line.rstrip('\n') #removes newline chars from lines
           name_list.append(line_clean)
  return name_list

def get_cdf_var(filename,varnames):
  """
  pulls particular variables from a CDF
  note: if variable has more than one set of data (E.g. b-field with x,y,z
  components) it will be necessary to format the data by reshaping the array
  from a 1D to a 2D array
  (may find workaround/better way later)
  Inputs:
      filename- string of the complete path to the specified CDF file
      varnames- list of strings which contain the CDF variables that are
          to be extracted
  Outputs:
      data- list of numpy arrays containing the desired variables' data
  """
  cdf_file=cdflib.CDF(filename,varnames)
  data=[]
  for varname in varnames:
      var_data=np.array(cdf_file.varget(varname))
      data.append(var_data)
  return data

def getData(file, timeInterval):
    CDFfile = cdflib.CDF(file[0])
    filename = file[0]
    varname = file[1]

    #generate time series
    raw_times = get_cdf_var(filename, ["Epoch"])[0]
    times = []

    start_minute = timeInterval[0]
    start_sec = timeInterval[1]
    stop_minute = timeInterval[2]
    stop_sec = timeInterval[3]

    for i in range(0, len(raw_times)):
        new_time = cdflib.epochs.CDFepoch.to_datetime(raw_times[i])[0]

        #set time contraints
        if new_time.minute == start_minute and new_time.second == start_sec:
            start_index = i
        if new_time.minute == start_minute and new_time.second == stop_sec:
            stop_index = i
        if new_time.minute == start_minute and new_time.second >= start_sec and new_time.second < stop_sec:
            new_timeF = new_time.strftime("%H:%M:%S")
            times.append(new_timeF)

    raw_data = get_cdf_var(filename, [varname])[0]
    data = []

    #only Bx Data
    for i in range(0,len(raw_data)):
        data.append(raw_data[i][0])

    #data sets as arrays, #len = 2048
    x = raw_times[start_index:stop_index]
    # x = times
    y = data[start_index:stop_index]

    return x, y

def getFFTdata(x, y):
    N = len(x)
    T = 1.0 / N

    #average value
    sum = 0
    for i in range(0, N):
        sum += y[i]

    average = sum/N

    yf = fftshift(fft(y-average))
    xf = fftshift(fftfreq(N, T))

    return xf, yf, N

def FGManalysis(period, plotPath, FFTpath):

    MMS1x, MMS1y = getData(files[0], period)
    MMS2x, MMS2y = getData(files[1], period)
    MMS3x, MMS3y = getData(files[2], period)
    MMS4x, MMS4y = getData(files[3], period)

    #Bx-Field
    fig1 = plt.figure(1)

    s1 = plt.plot(MMS1x , MMS1y, '-k')
    s2 = plt.plot(MMS2x , MMS2y, '-r')
    s3 = plt.plot(MMS3x , MMS3y, '-g')
    s4 = plt.plot(MMS4x , MMS4y, '-b')

    fig1.autofmt_xdate()

    plt.legend(labels = ('MMS1', 'MMS2', 'MMS3', 'MMS4'), loc = 'lower right')
    plt.title("FGM Bx Field Plot")
    plt.xlabel('Epoch')
    plt.ylabel('Bx Field (nT)')

    MMS1xf, MMS1yf, MMS1N = getFFTdata(MMS1x, MMS1y)
    MMS2xf, MMS2yf, MMS2N = getFFTdata(MMS2x, MMS2y)
    MMS3xf, MMS3yf, MMS3N = getFFTdata(MMS3x, MMS3y)
    MMS4xf, MMS4yf, MMS4N = getFFTdata(MMS4x, MMS4y)

    plt.savefig(plotPath)

    #FFT
    fig2 = plt.figure(2)
    plt.plot(MMS1xf, 1.0/MMS1N * np.abs(MMS1yf), '-k')
    plt.plot(MMS2xf, 1.0/MMS2N * np.abs(MMS2yf),'-r')
    plt.plot(MMS3xf, 1.0/MMS3N * np.abs(MMS3yf), '-g')
    plt.plot(MMS4xf, 1.0/MMS4N * np.abs(MMS4yf), '-b')

    plt.legend(labels = ('MMS1', 'MMS2', 'MMS3', 'MMS4'), loc = 'lower right') # legend placed at lower right
    plt.title("FGM Bx Field FFT")
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')

    #set FFT window
    plt.xlim([0, 20])
    plt.ylim([0, 5])

    plt.grid()
    plt.savefig(FFTpath)

    plt.show()

period = [] #start min, start sec, stop min, stop sec

# FGManalysis([18, 29, 18, 37], "./FGMresults/period.png", "./FGMresults/periodFFT.png")
FGManalysis([18, 29, 18, 33], "./FGMresults/1-2period.png", "./FGMresults/1-2periodFFT.png")
FGManalysis([18, 33, 18, 37], "./FGMresults/2-2period.png", "./FGMresults/2-2periodFFT.png")
# FGManalysis([18, 29, 18, 31], "./FGMresults/1-4period.png", "./FGMresults/1-4periodFFT.png")
# FGManalysis([18, 31, 18, 33], "./FGMresults/2-4period.png", "./FGMresults/2-4periodFFT.png")
# FGManalysis([18, 33, 18, 35], "./FGMresults/3-4period.png", "./FGMresults/3-4periodFFT.png")
# FGManalysis([18, 35, 18, 37], "./FGMresults/4-4period.png", "./FGMresults/4-4periodFFT.png")
