from bs4 import BeautifulSoup
import requests
import json

import tkinter as tk
from  tkinter import ttk 
import tkinter.messagebox

k = 0
k1 = 0
total = 0
ALL = []
def check(m,n,line):
    global k,k1
    if type(m[n]) == dict:
        for i in m[n]:
            line =  line + str(n)
            check(m[n],i,line)
    elif type(m[n]) == list:
        for i in m[n]:
            line = line + n
            check(m[n],m[n].index(i),line)
    else:
        if n == "resourceType" and m[n] == "Observation":
            ALL.append({"Number":k1*20+k+1,"Id":"","Status":"","Category":"","Code":"","Code1":"","Code2":"","Subject":"","Display":"","Time":"","Value":"","Units":"","Display1":"","Display2":"","Value1":"","Value2":""})
        if n == "id" and line[-8:] == "resource":
            ALL[k]["Id"] = str(m[n])
        if n == "status":
            ALL[k]["Status"] = str(m[n])
        if n == "code" and  line[-12:-2] == "codecoding":
            if ALL[k]["Code"] == "35094-2" and m[n] == "8462-4":
                ALL[k]["Code1"] = str(m[n])
            elif ALL[k]["Code"] == "35094-2" and m[n] == "8480-6":
                ALL[k]["Code2"] = str(m[n])
            else:
                ALL[k]["Code"] = str(m[n])
        if n == "display":
            if line[-18:-3] == "category0coding":
                ALL[k]["Category"] = str(m[n])
            else:
                if ALL[k]["Code"] == "35094-2" and ALL[k]["Code1"] == "8462-4" and ALL[k]["Display1"] == "":
                    ALL[k]["Display1"] = str(m[n])
                elif ALL[k]["Code"] == "35094-2" and ALL[k]["Code2"] == "8480-6" and ALL[k]["Display2"] == "":
                    ALL[k]["Display2"] = str(m[n])
                else:
                    ALL[k]["Display"] = str(m[n])
        if n == "effectiveDateTime":
            #print(n," : ",str(m[n]),end="\n\n")
            ALL[k]["Time"] = str(m[n])
        if n == "reference":
            #print(n," : ",str(m[n])[8:],end="\n\n")
            ALL[k]["Subject"] = str(m[n])
        if n == "value":
            if ALL[k]["Code"] == "35094-2":
                if ALL[k]["Code1"] == "8462-4" and ALL[k]["Value1"] == "":
                    ALL[k]["Value1"] = str(m[n])
                if ALL[k]["Code2"] == "8480-6" and ALL[k]["Value2"] == "":
                    ALL[k]["Value2"] = str(m[n])
            else:
                ALL[k]["Value"] = str(m[n])
            return 
        elif n == "unit":
            #print(m[n],end="\n\n")
            ALL[k]["Units"] = str(m[n])
            return 
        if n == "mode" and m[n] == "match":
            #print("=="*20,end="\n\n")
            k += 1
            
def link(m,n):
    global k1,relation
    if type(m[n]) == dict:
        for i in m[n]:
            line =  i + " : "
            link(m[n],i)
    elif type(m[n]) == list:
        for i in m[n]:
            link(m[n],m[n].index(i))
    else:
        if relation == "self":
            ALL_url[k1]["self"] = m[n].replace("amp;","")
            relation = ""
        if relation == "next":
            ALL_url[k1]["next"] = m[n].replace("amp;","")
            relation = ""
        if relation == "previous":
            ALL_url[k1]["previous"] = m[n].replace("amp;","")
            relation = ""
        if m[n] == "self":
            relation = "self"
        if m[n] == "next":
            relation = "next"
        if m[n] == "previous":
            relation = "previous"


window=tk.Tk()
window.title("Code Search")
window.geometry("1000x600+250+15")



label = tk.Label(window, text = 'code')
label.pack()
var = tk.StringVar()
entry = tk.Entry(window, textvariable=var,width = 40 )

entry.pack()

tree=ttk.Treeview(window)
s = ttk.Style().configure("Treeview",rowheight=50)

word=tree["columns"]=("Id","Status","Category","Code","Subject","Display","Time","Value","Units")

tree.heading("#0",text="Number")
tree.heading("Id",text="Id")
tree.heading("Status",text="Status")
tree.heading("Category",text="Category")
tree.heading("Code",text="Code")
tree.heading("Subject",text="Subject")
tree.heading("Display",text="Display")
tree.heading("Time",text="effectiveDateTime")  
tree.heading("Value",text="Value")
tree.heading("Units",text="Units")
    
ALL_url = []
relation = ""
    
def bt():
    global relation,k1,total,ALL_url
    code = var.get()
    #url = "https://oauth.dicom.org.tw/fhir/Observation?code="+code
    url = "http://192.168.50.3:10610/gateway/fhir/Observation?code="+code
    Token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL29hdXRoLmRpY29tLm9yZy50dyIsInN1YiI6IlRDU0jlnJjpmooiLCJhdWQiOiIxNTAuMTE3LjEyMS42NyIsImlhdCI6MTYwMzA4ODQzMywiZXhwIjoxNjA2NjY1NjAwLCJqdGkiOiIwMWNhZWVmOC1hYTk1LTQzYzQtODI4My01ODE0NmE5MGFmM2IifQ.cyJOd_1r5UvNHzm0h7k2IaCQBZyP2InOq644GOjtP-0d3M53kLJtjfdtHqsgD8fQrMI8D8t5WkoGQ2VPx-uDzzgknUWx5L70tfZadsPxJvnGFoZfIXfim4GasaBndB6fMyXq22BUudslwZPuBHOgLQaU-g6kZ6sxh4_dmmrbQNe0S9L1Z7NtzsqOS_48cWZuVOZBKLkLO5zfFcxn76Ntw81QRX85-wJp8L3kNozsqMc8JCmC79sFq6kI34h3ZIx-jV5D9w8F1T6qCdCn4MuDwco9oGxeAgelnAtXGkqlbHEBoz_E2aTssHE_y-edeXe2C9kxQJA6plJsM3IG75kMnw"
    r = requests.get(url, headers={'Authorization': Token})
    soup = BeautifulSoup(r.text,'html.parser')
    dicts = json.loads(str(soup))
    ALL_url = []
    for i in dicts:
            line = i
            if i == "total":
                total = dicts[i]
            if i == "link":
                ALL_url.append({"self":"","next":"","previous":""})
                relation = ""
                link(dicts,i)
                k1 += 1
                
    while total - k1*20 > 0:
        r = requests.get(ALL_url[k1-1]["next"], headers={'Authorization': Token})
        soup = BeautifulSoup(r.text,'html.parser')
        dicts = json.loads(str(soup))
        for i in dicts:
            line = i
            if i == "link":
                ALL_url.append({"self":"","next":"","previous":""})
                relation = ""
                link(dicts,i)
                k1 += 1
    k1 = 0
    main()


def main():
    tree.delete(*tree.get_children())
    global ALL,k,ALL_url
    ALL = []
    k = 0
    Token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL29hdXRoLmRpY29tLm9yZy50dyIsInN1YiI6IlRDU0jlnJjpmooiLCJhdWQiOiIxNTAuMTE3LjEyMS42NyIsImlhdCI6MTYwMzA4ODQzMywiZXhwIjoxNjA2NjY1NjAwLCJqdGkiOiIwMWNhZWVmOC1hYTk1LTQzYzQtODI4My01ODE0NmE5MGFmM2IifQ.cyJOd_1r5UvNHzm0h7k2IaCQBZyP2InOq644GOjtP-0d3M53kLJtjfdtHqsgD8fQrMI8D8t5WkoGQ2VPx-uDzzgknUWx5L70tfZadsPxJvnGFoZfIXfim4GasaBndB6fMyXq22BUudslwZPuBHOgLQaU-g6kZ6sxh4_dmmrbQNe0S9L1Z7NtzsqOS_48cWZuVOZBKLkLO5zfFcxn76Ntw81QRX85-wJp8L3kNozsqMc8JCmC79sFq6kI34h3ZIx-jV5D9w8F1T6qCdCn4MuDwco9oGxeAgelnAtXGkqlbHEBoz_E2aTssHE_y-edeXe2C9kxQJA6plJsM3IG75kMnw"
    r = requests.get(ALL_url[k1]["self"], headers={'Authorization': Token})
    soup = BeautifulSoup(r.text,'html.parser')
    dicts = json.loads(str(soup))
    for i in dicts:
            line = i
            check(dicts,i,line)

    
    for i in ALL:
        if i["Code"] == "35094-2":
            ALL.insert(ALL.index(i)+1,{"Number":i["Number"],"Id":i["Id"],"Status":i["Status"],"Category":i["Category"],"Code":i["Code1"],"Subject":i["Subject"],"Display":i["Display1"],"Time":i["Time"],"Value":i["Value1"],"Units":i["Units"]})
            ALL.insert(ALL.index(i)+2,{"Number":i["Number"],"Id":i["Id"],"Status":i["Status"],"Category":i["Category"],"Code":i["Code2"],"Subject":i["Subject"],"Display":i["Display2"],"Time":i["Time"],"Value":i["Value2"],"Units":i["Units"]})
            ALL.remove(i)
    
    
        
    
    tree.column("#0",width=50)
    tree.column("Id",width=50)
    tree.column("Status",width=50)
    tree.column("Category",width=70)
    tree.column("Code",width=80)
    tree.column("Subject",width=100)
    tree.column("Display",width=200)
    tree.column("Time",width=150)   
    tree.column("Value",width=70)
    tree.column("Units",width=100)
    

    for i in range(len(ALL)):
        tree.insert("",i,text=ALL[i]["Number"],values=(ALL[i]["Id"],ALL[i]["Status"],ALL[i]["Category"],ALL[i]["Code"],ALL[i]["Subject"],ALL[i]["Display"],ALL[i]["Time"],ALL[i]["Value"],ALL[i]["Units"]))

    tree.pack()
              

def nextpage():
    global k1
    if total - k1*20 > 20:
        k1 += 1
        main()
def prepage():
    global k1
    if k1 > 0:
        k1 -= 1
        main()

button = tk.Button(window, text = "搜尋",command=bt)
button.pack()


button1 = tk.Button(window, text = "上一頁",command=prepage)
button1.pack()

button2 = tk.Button(window, text = "下一頁",command=nextpage)
button2.pack()

window.mainloop()
