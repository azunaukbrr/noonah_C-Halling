def goto(linenum):
    global line
    line = linenum

ques1 = input("Do you want to review 1 , 2  ")
if ques1 == "1": 
    goto(13)
elif ques1 == "2": 
    goto(15)
else: 
    sys.exit("Bye")

print("this lis 13")

print("15")