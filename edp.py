import cdflib
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime

filename = "./20170810data/mms1/edp/mms1_edp_brst_l2_scpot_20170810121733_v2.4.0.cdf"
#fgm: "./20170810data/mms1/fgm/mms1_fgm_brst_l2_20170810121733_v5.99.0.cdf"
#edp: "./20170810data/mms1/edp/mms1_edp_brst_l2_scpot_20170810121733_v2.4.0.cdf"

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

for i in range(0, len(raw_times)):
    new_time = cdflib.epochs.CDFepoch.to_datetime(raw_times[i])[0]

    #set time contraints
    if new_time.minute == 18 and new_time.second == 20:
        start_index = i
    if new_time.minute == 18 and new_time.second == 50:
        stop_index = i
    if new_time.minute == 18 and new_time.second >= 20 and new_time.second < 50:
        new_timeF = new_time.strftime("%H:%M:%S")
        times.append(new_timeF)

raw_data = get_cdf_var(filename, ["mms1_edp_scpot_brst_l2"])[0]
data = raw_data



#data sets as arrays
x = times
y = data[start_index:stop_index]

#add figure from canvas coordinates (0.1, 0,1) to (0.9,0.9)
fig = plt.figure()

plt.plot(x,y,'-')
fig.autofmt_xdate()

plt.title("E Field Plot")
plt.xlabel('Epoch')
plt.ylabel('E Field')
plt.show()
