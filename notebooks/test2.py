#Initialization<final>
import os
os.system("cls")
print("Loading Payroll Program...")
import pysftp
import pandas as pd
import numpy as np
from pathlib import Path
import datetime
import time
from time import sleep
import shutil 
import sys
from tqdm import tqdm
from dotenv import load_dotenv
import pdfkit
import warnings
warnings.filterwarnings("ignore")
import smtplib
now = datetime.datetime.now()
timestamp = str(now.strftime("%Y%m%d_%H%M%S"))
sleep_timer=0.1

def taxes_single(income):
        if income < 9950:
            tax = income * 0.1
        elif income > 9951 and income <= 40525:
            tax = ((income-9950)*(0.12)) + (9950 * 0.1)
        elif income > 40526 and income <= 86375:
            tax = ((income-40525)*(0.22)) + (9950 * 0.1) + ((40525 - 9950) * 0.12)
        elif income > 86376 and income <= 164925:
            tax = ((income-86375)*(0.24)) + (9950 * 0.1) + ((40525 - 9950) * 0.12) + ((86376 - 40525 - 9950) * 0.22)
        elif income > 164926 and income <= 209425:
            tax = ((income-164925)*(0.32)) + (9950 * 0.1) + ((40525 - 9950) * 0.12) + ((86376 - 40525 - 9950) * 0.22) + ((164925 - 86375 - 40525 - 9950) * 0.24)
        elif income > 209426 and income <= 523600:
            tax = ((income-209425)*(0.35)) + (9950 * 0.1) + ((40525 - 9950) * 0.12) + ((86376 - 40525 - 9950) * 0.22) + ((164925 - 86375 - 40525 - 9950) * 0.24) + ((209425 - 164925 - 86375 - 40525 - 9950) * 0.32)
        elif income > 523601:
            tax = ((income-523600)*(0.37)) + (9950 * 0.1) + ((40525 - 9950) * 0.12) + ((86376 - 40525 - 9950) * 0.22) + ((164925 - 86375 - 40525 - 9950) * 0.24) + ((209425 - 164925 - 86375 - 40525 - 9950) * 0.32) + ((523600 - 209425 - 164925 - 86375 - 40525 - 9950) * 0.35)
        return (tax / 52)

def taxes_married(income):
        if income < 19900:
            tax = income * 0.1
        elif income > 19901 and income <= 81050:
            tax = ((income-19900)*(0.12)) + (19900 * 0.1)
        elif income > 81051 and income <= 172750:
            tax = ((income-81050)*(0.22)) + (19900 * 0.1) + ((81050 - 19900) * 0.12)
        elif income > 172751 and income <= 329850:
            tax = ((income-172750)*(0.24)) + (19900 * 0.1) + ((81050 - 19900) * 0.12) + ((172751 - 81050 - 19900) * 0.22)
        elif income > 329851 and income <= 418850:
            tax = ((income-329850)*(0.32)) + (19900 * 0.1) + ((81050 - 19900) * 0.12) + ((172751 - 81050 - 19900) * 0.22) + ((329850 - 172750 - 81050 - 19900) * 0.24)
        elif income > 418851 and income <= 628300:
            tax = ((income-418850)*(0.35)) + (19900 * 0.1) + ((81050 - 19900) * 0.12) + ((172751 - 81050 - 19900) * 0.22) + ((329850 - 172750 - 81050 - 19900) * 0.24) + ((418850 - 329850 - 172750 - 81050 - 19900) * 0.32)
        elif income > 628301:
            tax = ((income-628300)*(0.37)) + (19900 * 0.1) + ((81050 - 19900) * 0.12) + ((172751 - 81050 - 19900) * 0.22) + ((329850 - 172750 - 81050 - 19900) * 0.24) + ((418850 - 329850 - 172750 - 81050 - 19900) * 0.32) + ((628300 - 418850 - 329850 - 172750 - 81050 - 19900) * 0.35)
        return (tax / 52)

def medicare(income):
        medicare_tax = income * 0.0145
        return medicare_tax

def ss(income):
        ss_tax = income * 0.0620
        return ss_tax

def goto(linenum):
    global line
    line = linenum

os.system("cls")
print("This is a Payroll Processing Program designed to retrieve information from the employee self service portal, validate / update data to Employee Master Records and process payroll with ACH file output")
os.system("pause")

#Creating Employee Master Backup<final>
os.system("cls")
print("Creating Employee Master Backup...") 
for i in tqdm(range(10)):
    sleep(sleep_timer)
src = Path("../Resources/Source_data/master.csv")
dst = Path("../Resources/Source_data/Archive/"+timestamp+"MASTER_BACKUP.csv")
shutil.copy(src, dst)
print("Employee Master Backup Complete")
os.system("pause")
os.system("cls")

ques0 = input("Proceed with downloading employee updates and hours (Y / N) ?")
if ques0 == "Y": 
        os.system("cls")
        print("Downloading Data...")
        #Downloading Updates
        # load_dotenv()
        # server = os.getenv("ftp_server")
        # username = os.getenv("ftp_user")
        # password = os,getenv("ftp_pass")
        # cnopts = pysftp.CnOpts()
        # cnopts.hostkeys = None
        # sftp = pysftp.Connection(server, username=username, password=password, cnopts=cnopts)
        # sftp.get('/outbound/noonah_CHalling/updates.csv')
        # sftp.get('/outbound/noonah_CHalling/hours.csv')
        for i in tqdm(range(10)):
            sleep(sleep_timer)
        print("Download Complete")
        os.system("pause")
elif ques0 == "N":
        os.system("cls")
        print("Proceeding without updates")
        os.system("pause") 
else: 
    print("Please enter Y or N.") 

#Validating Employee Update Data<final>
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
upval_employee_data_bad_records.to_csv(Path("../Resources/Exceptions/bad_records.csv"), index=False, na_rep="")
upval_employee_data_issues_report = upval_employee_data_issues[["Issue"]]
for i in tqdm(range(10)):
    sleep(sleep_timer)
print("Validation Complete")
ques1 = input("Do you want to review (Y / N)?  ")
if ques1 == "Y": 
    print("Here are the records with issues:") 
    print(upval_employee_data_issues_report)
    ques2 = input("Do you want to fix the issues (Y / N)?  ")
    if ques2 == "Y":
        os.system("excel.bat")
        os.system("cls")
        print("Here are the records with issues:") 
        print(upval_employee_data_issues_report)
        os.system("pause")
        os.system("cls")
        ques3 = input("Do you want reprocess changes (Y / N)?  ")
        if ques3 == "Y":
                upval_employee_data_updates = pd.read_csv(Path("../Resources/Exceptions/bad_records.csv"), dtype = {"EMP_NO" : str, "SSN" : str, "BANK_RTN" : str, "BANK_ACC" : str}) 
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
                upval_employee_data_bad_records.to_csv(Path("../Resources/Exceptions/bad_records.csv"), index=False, na_rep="")
                upval_employee_data_issues_report = upval_employee_data_issues[["Issue"]]
                for i in tqdm(range(10)):
                    sleep(sleep_timer)
                print("Validation Complete")
                ques4 = input("FINAL review (Y / N)?  ")
                if ques4 == "Y": 
                    print("Here are the records with issues:") 
                    print(upval_employee_data_issues_report)
                    ques5 = input("FINAL reprocess changes (Y / N)?  ")
                    if ques5 == "Y":
                            upval_employee_data_updates = pd.read_csv(Path("../Resources/Exceptions/bad_records.csv"), dtype = {"EMP_NO" : str, "SSN" : str, "BANK_RTN" : str, "BANK_ACC" : str}) 
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
                            upval_employee_data_bad_records.to_csv(Path("../Resources/Exceptions/bad_records.csv"), index=False, na_rep="")
                            upval_employee_data_issues_report = upval_employee_data_issues[["Issue"]]
                            for i in tqdm(range(10)):
                                sleep(sleep_timer)
                            print("Validation Complete")
                            print("Here are the records with issues:") 
                            os.system("pause")
                            os.system("cls")
                    elif ques5 == "N":
                            os.system("cls")
                            print("Excluding Records and saving in Exceptions Folder. Following records will not be processed:")
                            print(upval_employee_data_bad_records)
                            os.system("pause")         
                elif ques4 == "N": 
                        os.system("cls")
                        print("Excluding Records and saving in Exceptions Folder. Following records will not be processed:")
                        print(upval_employee_data_bad_records)
                        os.system("pause") 
                else: 
                    print("Proceeding with Payroll Processing") 
        elif ques3 == "N":
                os.system("cls")
                print("Excluding Records and saving in Exceptions Folder. Following records will not be processed:")
                print(upval_employee_data_bad_records)
                os.system("pause") 
        else: 
                print("Proceeding with Payroll Processing")                
    elif ques2 == "N":
          os.system("cls")
          print("Excluding Records and saving in Exceptions Folder. Following records will not be processed:")
          print(upval_employee_data_bad_records)
          os.system("pause")  
    else: 
        print("Proceeding with Payroll Processing")  
elif ques1 == "N": 
    os.system("cls")
else: 
    print("Proceeding with Payroll Processing") 

#Updating Employee Master<final>
print("Adding Good Records to Employee Master")
upval_employee_data = pd.read_csv(Path("../Resources/Source_data/master.csv"), index_col = "EMP_NO", keep_default_na = False, dtype = {"SSN" : str, "BANK_RTN" : str, "BANK_ACC" : str})
upval_employee_data_updates = pd.read_csv(Path("../Resources/Source_data/updates.csv"), index_col = "EMP_NO", keep_default_na = False, dtype = {"SSN" : str, "BANK_RTN" : str, "BANK_ACC" : str}) 
upval_employee_data = upval_employee_data[~upval_employee_data.index.isin(upval_employee_data_updates.index)].reset_index()
upval_employee_data_updates = upval_employee_data_updates.reset_index()
upval_employee_data = upval_employee_data.append(upval_employee_data_updates, ignore_index="True", verify_integrity="True").sort_values(by="EMP_NO").astype("str")
active_only = upval_employee_data[upval_employee_data["EMP_STATUS"]=="Inactive"].index
inactive_only = upval_employee_data.loc[active_only]
inactive_only.to_csv(Path("../Resources/Source_data/Archive/"+timestamp+"_TERMINATIONS.csv"), index=False)
upval_employee_data.drop(active_only, inplace=True)

upval_employee_data.to_csv(Path("../Resources/Source_data/master.csv"), index=False)
for i in tqdm(range(10)):
    sleep(sleep_timer)
print("Update Complete")
os.system("pause")
os.system("cls")
#Updating Employee Master<final>
print("Adding Good Records to Employee Master")
upval_employee_data = pd.read_csv(Path("../Resources/Source_data/master.csv"), index_col = "EMP_NO", keep_default_na = False, dtype = {"SSN" : str, "BANK_RTN" : str, "BANK_ACC" : str})
upval_employee_data_updates = pd.read_csv(Path("../Resources/Source_data/updates.csv"), index_col = "EMP_NO", keep_default_na = False, dtype = {"SSN" : str, "BANK_RTN" : str, "BANK_ACC" : str}) 
upval_employee_data = upval_employee_data[~upval_employee_data.index.isin(upval_employee_data_updates.index)].reset_index()
upval_employee_data_updates = upval_employee_data_updates.reset_index()
upval_employee_data = upval_employee_data.append(upval_employee_data_updates, ignore_index="True", verify_integrity="True").sort_values(by="EMP_NO").astype("str")
active_only = upval_employee_data[upval_employee_data["EMP_STATUS"]=="Inactive"].index
inactive_only = upval_employee_data.loc[active_only]
inactive_only.to_csv(Path("../Resources/Source_data/Archive/"+timestamp+"_TERMINATIONS.csv"), index=False)
upval_employee_data.drop(active_only, inplace=True)
upval_employee_data.to_csv(Path("../Resources/Source_data/master.csv"), index=False)
for i in tqdm(range(10)):
    sleep(sleep_timer)
print("Update Complete")
os.system("pause")
os.system("cls")
#Loading Employee Data
employee_data = pd.read_csv(Path("../Resources/Source_data/master1.csv"), header = 0, usecols = ["EMP_NO","FIRST_NAME","LAST_NAME","FEDFILINGSTATUS","EMP_STATUS","PAYCODE","PAYRATE"])
hour_data = pd.read_csv(Path("../Resources/Source_data/hours.csv")) 
employee_ach_data = pd.read_csv(Path("../Resources/Source_data/master1.csv"), header = 0, usecols = ["EMP_NO","FIRST_NAME","LAST_NAME","BANK_RTN","BANK_ACC"], dtype = {"BANK_RTN" : str, "BANK_ACC" : str})
#Generating Employee Report
print("Here is the list of employees DUE for this payroll")
employee_list = employee_data
employee_list["WAGE_RATE"] = np.where(employee_list["PAYCODE"] == "Salary", (employee_list["PAYRATE"]/52),employee_list["PAYRATE"])
print(employee_list.drop(["FEDFILINGSTATUS","PAYRATE"], axis=1).round(2))
os.system("pause")
os.system("clr")
print("Here are inactivated employees NOT DUE for this Payroll")
print(inactive_only)
os.system("pause")
os.system("cls")
print("Calculating Payroll...")
#Calculating Hourly Wages
hourly_emp_data = employee_data.loc[employee_data["PAYCODE"] == "Hourly"]
hourly_emp_data = employee_data.loc[employee_data["EMP_STATUS"] == "Active"]
hourly_grid = pd.merge(hourly_emp_data, hour_data, how = "inner", on = "EMP_NO")
hourly_grid["WAGES"] = np.where(hourly_grid["HOURS"] > 40, 
    ((hourly_grid["HOURS"]-40)*1.5*hourly_grid["PAYRATE"])+ (hourly_grid["PAYRATE"]*40), 
    (hourly_grid["HOURS"] * hourly_grid["PAYRATE"]))
# hourly_grid.drop(["EMP_STATUS","PAYCODE","PAYRATE","HOURS"], axis=1).round(2)

#Calculating Salary Wages
salary_grid = employee_data.loc[employee_data["PAYCODE"] == "Salary"]
salary_grid = salary_grid.loc[salary_grid["EMP_STATUS"] == "Active"]
salary_grid["WAGES"] = salary_grid["PAYRATE"] / 52
salary_grid.drop(["EMP_STATUS"], axis=1).round(2)

#Combining Salary and Hourly Wages
all_wages = hourly_grid.append(salary_grid, ignore_index=True, verify_integrity= True)
all_wages.drop(["EMP_STATUS","PAYRATE","HOURS"], axis=1).round(2)

#Tax Calculation
all_wages["WAGESANA"] = all_wages["WAGES"] * 52
tax_single_all_wages = all_wages.loc[all_wages["FEDFILINGSTATUS"] == "Single or Married filing separately"]
tax_single_all_wages["TAX"]=tax_single_all_wages["WAGESANA"].apply(taxes_single)

tax_married_all_wages = all_wages.loc[all_wages["FEDFILINGSTATUS"] == "Married or filing jointly"]
tax_married_all_wages["TAX"]=tax_married_all_wages["WAGESANA"].apply(taxes_single)

final_wages = tax_single_all_wages.append(tax_married_all_wages, ignore_index=True, verify_integrity= True)
final_wages["SOC_SEC"]=final_wages["WAGES"].apply(ss)
final_wages["MEDICARE"]=final_wages["WAGES"].apply(medicare)
final_wages["NET_WAGES"]=final_wages["WAGES"]-final_wages["SOC_SEC"]-final_wages["MEDICARE"]-final_wages["TAX"]
final_wage_summary = final_wages.drop(["EMP_STATUS","PAYRATE","HOURS","WAGESANA","PAYCODE","FEDFILINGSTATUS"], axis=1).round(2)

for i in tqdm(range(10)):
    sleep(sleep_timer)
print("Calculation Complete")
os.system("pause")
os.system("cls")
print("Here are the details:")
print(final_wage_summary)
ques6 = input("Do you want to finalize the payroll (Y / N)?  ")
if ques6 == "Y": 
    os.system("cls")
    print("Finalizing Payroll...")
    final_wage_summary.to_csv(Path("../Resources/Output_data/Archive/"+timestamp+"_PAYROLL_SUMMARY.csv"), index=False)
    final_wage_summary.to_csv(Path("../Resources/Output_data/PAYROLL_SUMMARY.csv"), index=False) 
    print("Payroll Summary finalized and saved in ""Output_data"" folder")
    os.system("pause")
    os.system("cls")
elif ques6 == "N":
    print("Payroll not saved")
    sys.exit("Exiting Program")
else:
    print("cont")
    os.system("cls")
    os.system("pause")

#Creating ACH File
print("Generating Bank Upload File")
employee_ach_data["NAME"] = (employee_ach_data["FIRST_NAME"]) + [" "] + (employee_ach_data["LAST_NAME"])
employee_ach_data1 = pd.merge(final_wages, employee_ach_data, how="inner", on = "EMP_NO")
employee_ach_data2 = employee_ach_data1.drop(["FEDFILINGSTATUS","WAGES","WAGESANA","TAX","EMP_STATUS","PAYCODE", "PAYRATE", "HOURS"], axis=1).round(2)
employee_ach_data2[["EMP_NO","NAME","BANK_RTN","BANK_ACC","NET_WAGES"]]
employee_ach_data2.to_csv(Path("../Resources/Output_data/Archive/"+timestamp+"_ACH_UPLOAD.csv"), index=False)
employee_ach_data2.to_csv(Path("../Resources/Output_data/ACH_UPLOAD.csv"), index=False) 
for i in tqdm(range(10)):
    sleep(sleep_timer)
print("Bank Upload Generation Complete and saved in ""Output_data"" folder")
os.system("pause")
os.system("cls")
#CHECKPOINT