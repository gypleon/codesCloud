# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

csvfile=open('D:\OneDrive - The Chinese University of Hong Kong\Study Related\Data mining\Project\dataset_diabetes(copy)\diabetes_cleaned_SPSS.csv')
data=[];
for line in csvfile:
    data.append(list(line.strip().split(',')))
    
import copy
data2=copy.deepcopy(data)

#preprocessing    
#if number No or >30, to be one single value Not30
for i in range(len(data)):
    if (data[i][-1]=='NO' or data[i][-1]=='>30' ):
        data2[i][-1]='Not30'
#if (data[i][0]=='?' or data[i][0]=='Other' ):
    
#delete ? in race
data3 = []        
for i in range(len(data2)):
    if (data2[i][0]!='?' ):
        data3.append(data2[i])
   
#age rearrange, [0-40) [40-70) [70-100)       
for i in range(1,len(data3)):
    if (data3[i][2]=='[0-10)' or data3[i][2]=='[10-20)' or data3[i][2]=='[20-30)'or data3[i][2]=='[30-40)'):
        data3[i][2]='[0-40)'       
    if (data3[i][2]=='[40-50)' or data3[i][2]=='[50-60)' or data3[i][2]=='[60-70)'):
        data3[i][2]='[40-70)'  
    if (data3[i][2]=='[70-80)' or data3[i][2]=='[80-90)' or data3[i][2]=='[90-100)'):
        data3[i][2]='[70-100)'  

#Others as 10 all the time

#admission type
#if 4,5,6,7,8 as 10 others 
for i in range(1,len(data3)):
    if (data3[i][3]!='1' and data3[i][3]!='2' and data3[i][3]!='3'):
        data3[i][3]='10' 
   
#discharge_disposition        
#1 as go home otherwise as other method  10
for i in range(1,len(data3)):
    if (data3[i][4]!='1' and data3[i][4]!='3'  and data3[i][4]!='6'):
        data3[i][4]='10'   

#admission_sourceID
#except 1,7,17 then 10, others
for i in range(1,len(data3)):
    if(data3[i][5]!='7' and data3[i][5]!='1' and data3[i][5]!='17' ):
        data3[i][5]='10'
        
        
#time in hospital 
#[1-4]  60%   [5-8] 90%  [9-14]100%
for i in  range(1,len(data3)):
    if(data3[i][6]=='1' or data3[i][6]=='2' or data3[i][6]=='3' or data3[i][6]=='4'):
        data3[i][6]='[1-4]'
    if(data3[i][6]=='5' or data3[i][6]=='6' or data3[i][6]=='7' or data3[i][6]=='8'):
        data3[i][6]='[5-8]'
    if(data3[i][6]=='9' or data3[i][6]=='10' or data3[i][6]=='11' or data3[i][6]=='12' or data3[i][6]=='13' or data3[i][6]=='14'):
        data3[i][6]='[9-14]'        

#Number of outpatients       
#except 0,1,2  95% already    otherwise 10 more than once
for i in  range(1,len(data3)):
    if(data3[i][7]!='0'and data3[i][7]!='1' and data3[i][7]!='2'):
        data3[i][7]='10'
     
#number of emgergence, 0,1,2 as none, 10 as more than once
for i in range(1,len(data3)):
    if(data3[i][8]!='0' and data3[i][8]!='1' and data3[i][8]!='2'):
      data3[i][8]='10' 

 
#number_inpatient
for i in  range(1,len(data3)):
    if(data3[i][9]!='0' and data3[i][9]!='1' and data3[i][9]!='2' and data3[i][9]!='3'):
        data3[i][9]='10'      

        
  
import csv

def createListCSV(fileName="", dataList=[]):
    with open(fileName, "w",newline='') as csvFile:
        csvWriter = csv.writer(csvFile,delimiter=',',dialect='excel') 
        for data in dataList:
            csvWriter.writerow(data)
            csvFile.close


createListCSV("disbetes_cleaned_python41129.csv", data3)

    
#define race
# Caucasian as 1 AfricanAmerica as 2, others as 3     ?as 4



#if data[1][26]=='NO':
#    data2[1][26]='Not30'

    
#define gender 
#male as 0, female as 1, age [0-30]as 1 [30-60] as 2,  age[60-100) as 3


#admission_type_id


#define Discharge disposition   
#if discharged to home  then 1   otherwise 2



#admisssssion source   Admitted from emergency room 1    Admitted because of physician/clinic referral2
#others 3


#define time_in_hospital
#1-5 day for 1, 6-10 for 2, 11-14 for 3



#define num_lab_procedures
#range 1-132
#1-50 for 1; 51-100, for 2; 101-



#define num_procedures
#range 0-6
#0-3 for 1; 4-6 for 2



#define num_medications
#range:1-81
#0-40 for 1; [41-   for 2

              
              
#define number_outpatient
#range 0-42
#0-20 for 1 ;21-42 for 2



#define number_emergency
#range 0-76
#0-38 for 1; 39-76 for 2



#define number_inpatient
#range 0-21
#0-11 for 1; 12-21 for 2



#define diag_1
#range 3-999




#define diag_2
#range 5-999




#define diag_3
#range 3-999




#define number_diagnoses
#range 1-16




#define max_glu_serum
#range 
#>300  for 3; >200, for 2, Norm for 1 ,non for 0




#define A1Cresult
#range 
#non for 0, norm for 1, >7 for 2, >8 for 3




#define insulin
#non for 0, steady for 1, up for 2, down for 3




#define change
#change for 1 no for 2;




#define diabetesMed
#Yes for 1, no for 2 




#define readmitted
#No& >30 as 1,  <30 as 0;

