import cdflib
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
from scipy.fft import fft, ifft

filenames = ["./20170810data/mms1/fgm/mms1_fgm_brst_l2_20170810121733_v5.99.0.cdf"]
filenames.append("./20170810data/mms2/fgm/mms2_fgm_brst_l2_20170810121733_v5.99.0.cdf")
filenames.append("./20170810data/mms3/fgm/mms3_fgm_brst_l2_20170810121733_v5.99.0.cdf")
filenames.append("./20170810data/mms4/fgm/mms4_fgm_brst_l2_20170810121733_v5.99.0.cdf")

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

# readvariables(zData, "z")
# readvariables(rData, "r")
# txt.close()

raw_times = get_cdf_var(filenames[0], ["Epoch"])[0]
times = []

start_minute = 18
start_sec = 25
stop_sec = 41

for i in range(0, len(raw_times)):
    new_time = cdflib.epochs.CDFepoch.to_datetime(raw_times[i])[0]

    #set time contraints
    if new_time.minute == start_minute and new_time.second == start_sec:
        start_index = i
        start_nano = raw_times[i]
    if new_time.minute == start_minute and new_time.second == stop_sec:
        stop_index = i
        stop_nano = raw_times[i]
    if new_time.minute == start_minute and new_time.second >= start_sec and new_time.second < stop_sec:
        times.append(raw_times[i])

#for i in range(0, len(times)):
    #print(times[i])

num_of_ticks = 17
tick_indexes = []
tick_values = np.linspace(start_sec, stop_sec, num_of_ticks).tolist()

distance_between_ticks = math.floor((len(times)/(num_of_ticks-1)))
for x in range(num_of_ticks):
    if distance_between_ticks*x >= 1:
        tick_indexes.append(times[distance_between_ticks*x-1])
    else:
        tick_indexes.append(times[distance_between_ticks*x])

# print("Data:")
#use GSE (elliptical) or GSM (magnetospheric)
raw_data = [get_cdf_var(filenames[0], ["mms1_fgm_b_gsm_brst_l2"])[0], get_cdf_var(filenames[1], ["mms2_fgm_b_gsm_brst_l2"])[0], get_cdf_var(filenames[2], ["mms3_fgm_b_gsm_brst_l2"])[0], get_cdf_var(filenames[3], ["mms4_fgm_b_gsm_brst_l2"])[0]]
data = [[],[],[],[]]

#only Bx Data
for j in range(4):
    for i in range(0,len(raw_data[j])):
        data[j].append(raw_data[j][i][0])

fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8]) #(x, y, len, wid)

#data sets as arrays
x = raw_times[start_index:stop_index]
for i in range(0, len(raw_data)):
    y = data[i][start_index:stop_index]
    ax.plot(x, y, ',-')

ax.set_xticks(tick_indexes)
ax.set_xticklabels(tick_values)

plt.title("FGM B Field Plot")
plt.xlabel('Epoch')
plt.ylabel('B Field')
plt.show()
