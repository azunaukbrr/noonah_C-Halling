import pysftp
import pandas as pd
import numpy as np
from pathlib import Path
import datetime
import time
from time import sleep
import os
import shutil 
import sys
from tqdm import tqdm
from dotenv import load_dotenv
import pdfkit
now = datetime.datetime.now()
timestamp = str(now.strftime("%Y%m%d_%H%M%S"))
os.system("cls")
print("Validating Employee Update Data...")
upval_employee_data_updates = pd.read_csv(Path("../Resources/Source_data/updates.csv"), dtype = {"EMP_NO" : str, "SSN" : str, "BANK_RTN" : str, "BANK_ACC" : str}) 

upval_employee_data_updates["Issue"] = np.where(upval_employee_data_updates["EMP_NO"].isna(), "Employee Number is Missing",
    np.where(upval_employee_data_updates["FIRST_NAME"].isna(), "Name is Missing",
    np.where(upval_employee_data_updates["SSN"].isna(), "SSN is Missing",
    np.where(upval_employee_data_updates["JOBTITLE"].isna(), "Job Title is Missing",
    np.where(upval_employee_data_updates["HIREDATE"].isna(), "Hire Date is Missing",
    np.where(upval_employee_data_updates["DOB"].isna(), "Date of Birth is Missing",
    np.where(upval_employee_data_updates["FEDFILINGSTATUS"].isna(), "Federal Filing Status is Missing",
    np.where(upval_employee_data_updates["WORKSTATE"].isna(), "Work State is Missing",
    np.where(upval_employee_data_updates["BANK_RTN"].isna(), "Bank Routing Number is Missing",
    np.where(upval_employee_data_updates["BANK_ACC"].isna(), "Bank Account Number is Missing",
    np.where(upval_employee_data_updates["EMP_STATUS"].isna(), "Employment Status is Missing",
    np.where(upval_employee_data_updates["PAYCODE"].isna(), "Pay code is Missing",
    np.where(upval_employee_data_updates["PAYRATE"].isna(), "Pay rate is Missing","")))))))))))))

upval_employee_data_good_records = upval_employee_data_updates.dropna(subset=["FIRST_NAME","SSN","JOBTITLE","HIREDATE","DOB","FEDFILINGSTATUS","WORKSTATE","BANK_RTN","BANK_ACC","EMP_STATUS","PAYCODE","PAYRATE"])
upval_employee_data_good_records = upval_employee_data_good_records.drop(labels="Issue", axis=1)

upval_employee_data_issues = upval_employee_data_updates[upval_employee_data_updates["Issue"] != ""]
upval_employee_data_issues = upval_employee_data_issues.rename_axis(mapper="Record#", axis=1)
upval_employee_data_issues.index+= 1
upval_employee_data_bad_records = upval_employee_data_issues
upval_employee_data_bad_records.to_csv(Path("../Resources/Source_data/badrec.csv"), index=False, na_rep="")
upval_employee_data_issues_report = upval_employee_data_issues[["Issue"]]
for i in tqdm(range(10)):
    sleep(2)
print("Validation Complete")
ques1 = input("Do you want to review (Y / N)?  ")
if ques1 == "Y": 
    os.system("cls")
    print(upval_employee_data_issues_report)
    os.system("pause")
elif ques1 == "N": 
    os.system("cls")
    print("Updating Good Records to Employee Master")
else: 
    print("Please enter Y or N.") 