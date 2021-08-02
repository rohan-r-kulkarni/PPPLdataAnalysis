import cdflib
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
from scipy.fft import fft, ifft

filename = "./20170810data/mms1/edp/mms1_edp_brst_l2_scpot_20170810121733_v2.4.0.cdf"

rData = []
zData = []

file = cdflib.CDF(filename)

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

raw_times = get_cdf_var(filename, ["mms1_edp_epoch_brst_l2"])[0]

times = []

start_minute = 18
start_sec = 25
stop_sec = 41

ERROR = 90*pow(10, 9) #90 sec ERROR

def binary_search(y, m, d, hour, min, sec):
    low = 0
    high = len(raw_times)-1
    while (low <= high):
        mid = int((low+high)/2)
        midTime = cdflib.epochs.CDFepoch.to_datetime(raw_times[mid])[0]
        if midTime.year == y and midTime.month == m and midTime.day == d and midTime.minute == min and midTime.hour == hour:
            if midTime.second == sec:
                return mid
            elif midTime.minute < min:
                low = mid+1
            else:
                high = mid-1
    return -1

target = [2017,8,10,12,18,20]
targetEPOCH = cdflib.epochs.CDFepoch.compute_tt2000(target)
print(targetEPOCH)

beginSearching = binary_search(2017, 8, 10, 12, 18, 20)
endSearching = binary_search(2017, 8, 10, 12, 19, 50)

print()

print(beginSearching)
print(endSearching)

#linear search, make it binary search
# for i in range(0, len(raw_times)):
#     new_time = cdflib.epochs.CDFepoch.to_datetime(raw_times[i])[0]
#
#     #set time contraints
#     if new_time.minute == start_minute and new_time.second == start_sec:
#         start_index = i
#     if new_time.minute == start_minute and new_time.second == stop_sec:
#         stop_index = i
#     if new_time.minute == start_minute and new_time.second >= start_sec and new_time.second < stop_sec:
#         new_timeF = new_time.strftime("%H:%M:%S")
#         times.append(new_timeF)
#
print(times)
# raw_data = get_cdf_var(filename, ["mms1_edp_scpot_brst_l2"])[0]
#INSTEAD, USE "mms1_edp_dce_gse_brst_l2" #in elliptical coordinates, ExEyEz

# data = raw_data



#data sets as arrays
# x = raw_times[start_index:stop_index]
# #x = times
# y = data[start_index:stop_index]
#
# #add figure from canvas coordinates (0.1, 0,1) to (0.9,0.9)
# fig = plt.figure()
#
# plt.plot(x,y,'-')
# fig.autofmt_xdate()
#
# plt.title("EDP E Field Plot")
# plt.xlabel('Epoch')
# plt.ylabel('E Field')
# plt.show()
