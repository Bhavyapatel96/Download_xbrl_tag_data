# -*- coding: utf-8 -*-
"""
Created on Sat May 12 00:19:29 2018

@author: bhavy

@README: This program will download values for given XBRL tags. You, the user can input as many tags as you want. The user can also specify the name of Excel
file where we will be storing our data. For each tag, we let user decide the name of the column for the particular tag. 
***IMPORTANT*** In order to run this program, you must have run "download_xbrl_for_ciks" program.
"""

import os
from xml.dom import minidom
from zipfile import *

'''
@get_data_from_tag function takes two inputs: 1) tagname that contains tag_name and 2) xmldoc that containts xml file to be parsed.
It returns value contained in that tag.
'''
def get_data_from_tag(tagname,xmldoc):
    c=xmldoc.getElementsByTagName(tagname)
    x=['.']
    if len(c)==0:
        x[0]='.'
        
    else:
        i=0
        for items in reversed(c): 
            try:
                per=float(items.firstChild.data)
            except:
                per=0
            finally:
                '''
                .5f means we are printing values rounded upto 5th decimal place. Change that value if you want more/less digits after decimal point.
                '''
                s1="{0:.5f}".format(per)
                x[i]=s1
                break
    return get_specific_header(x)

'''
@get_cik function takes input 1)file_name that is filename that we will be parsing. It returns CIK value.
'''
def get_cik(file_name):
    
    c=[]
    #Next line, we split filename with '-' as delimeter and take first value of that array. Array contains strings that got separated by delimeter we used. 
    p=file_name.split('-')[0]
    for i in range(len(p)):
        if p[i]!='0':
            c.append(p[i:])
            break
    s1=''
    s1=c[0]
    return s1

'''
@get_headers takes input number of headers user wants, and will ask user to give value for each header. This function basically sets your column names in 
the Excel file where we will be displaying our output.
'''
def get_headers(x):
    c=["CIK","REPORT_DATE"]
    for i in range(x):
        print("enter value of header you want: ")
        c.append(input())

    return get_specific_header(c)

'''
@get_period_of_report takes input 1)doc which is file that we are parsing and returns the report date of that file. 
'''
def get_period_of_report(doc):
    x=[]
    date=doc.split('-')[1]
    date=date.split('.')[0]
    x.append(date[4])
    x.append(date[5])
    x.append('/')
    x.append(date[6])
    x.append(date[7])
    x.append('/')
    for i in range (4):
        x.append(date[i])
    s1=''
    s1=s1.join(str(e) for e in x)
    return s1
'''
@get_specific_header returns entire row that we needed to add to excel file, separated by commas for each column value.
'''
def get_specific_header(c):
    s=''
    for i in range(len(c)):
        s=s+str(c[i])
        
        if i==len(c)-1:
            break
        else:
            s=s+','
    return s
'''
@xbrl_scrap takes two inputs. 1)filename is the Excel file where we want to store our data. 2) year for which we ran "download_xbrl_for_ciks" program before. 
Note: If you did not run that program, run it first and then run this program as it will need zip files to extract xml files which we parse. The function will
create Excel file containing appropriate tag_values.
'''
def xbrl_scrap(filename,year):
    #Ask user how many tags they want to use for this program.
    print("how many tags are we using here? ")
    #input() takes value from user.
    tag_qty=input()
    tag=[]
    for i in range(int(tag_qty)):
        print("please input tag : " + str(i+1))
        tag_value=input()
        tag.append(tag_value)
    #Change directory where you want to store Excel file. It will be different for your PC. By default, it is your current working directory.
    #os.chdir('C:\\Users\\bhavy\\Desktop')
    #open the file in write mode. And note that here, we also give .csv extension. This is important.
    f=open(filename+".csv","w")
    #get column names for excel file and convert it into string. We added commas because it is used to separate columns in .csv file.
    headers=get_headers(int(tag_qty))
    headers=str(headers)
    headers=headers+"\n"
    f.write(headers)
    #go to directory where we have our zip files stored.
    #os.chdir('C:\\Users\\bhavy\\Desktop\\Sec\\'+ year)
    os.chdir('sec\\'+year)
    #get list of directories ( here: the zip files that we have downloaded)
    directories=os.listdir(os.getcwd())
    #for each directory, we will perform  extraction using extract feature of ZipFile
    for directory in range(len(directories)):

        file_name=directories[directory]
        print(file_name)
        zip_archive = ZipFile(file_name)
        #get first file in that zip folder after extraction. This is the required xml file we want. 
        file=zip_archive.namelist()[0]
        zip_archive.extract(file)
        xmldoc=minidom.parse(file)
        #get report data
        por=get_period_of_report(file)


        '''
        Sample tag values for reference: **DONT INCLUDE QUOTES WHEN YOU ENTER TAG VALUES**
        tag1="us-gaap:EffectiveIncomeTaxRateReconciliationForeignIncomeTaxRateDifferential"
        tag2="us-gaap:EffectiveIncomeTaxRateReconciliationChangeInDeferredTaxAssetsValuationAllowance"
        '''

        #for each tag, we get data for that tag.
        data=[]
        for i in range(int(tag_qty)):
            #get specific tag value
            x=get_data_from_tag(tag[i],xmldoc)
            cik=get_cik(file_name)
            data.append(str(x))
        #get entire row value as string and add to file so .csv file automatically splits columns on ",".   
        h=get_specific_header(data)
        #write to file. 
        f.write(cik + "," +por +","+ str(h) + "\n")
    #Close the file and zip_archive    
    f.close()
    zip_archive.close()


#This is just for making program user interactive. It asks for user to enter their name.
print("Please enter your name:")
name=input()
#This is must, if you want user to pick a filename of their choice.
print("Welcome, " + name + " Please enter the file name where you want to see your data" )
filename=input()
#Here, you will enter the year for which you ran "download_xbrl_for_ciks" program. It is must in order to run this program. 
print("Please enter the year for which you have downloaded the zipfiles for CIK's ")
year=input()
#call our main function.
xbrl_scrap(filename,year)