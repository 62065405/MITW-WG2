from bs4 import BeautifulSoup
import requests
import json

def check(m,n,line):
        if type(m[n]) == dict:
            for i in m[n]:
                line =  i + " : "
                #print(i,":",end=" ")
                check(m[n],i,line)
        elif type(m[n]) == list:
            for i in m[n]:
                check(m[n],m[n].index(i),line)
        else:
            if n == "resourceType":
                print(line+str(m[n]),end="\n\n")
            if n == "id":
                print(line+str(m[n]),end="\n\n")
            if n == "display":
                print(str(m[n]),end="\n\n")
            if n == "effectiveDateTime":
                print(line+str(m[n]),end="\n\n")
            if n == "value":
                print(line+str(m[n]),end=" ")
                return
            elif n == "unit":
                print(m[n],end="\n\n")
                return
            #print(line+str(m[n]),end="\n\n")


#url = "https://startfhir.dicom.org.tw/fhir/Observation/4603"
Id = input("Please Enter the Id: ")
if Id != "":
    try:
        url = "https://startfhir.dicom.org.tw/fhir/Observation/" + Id
        url = "https://startfhir.dicom.org.tw/fhir/Observation?subject=fd418b74-308d-4991-b262-ded08c889031"
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        dicts = json.loads(str(soup))

        
        print()
        for i in dicts:
            #print("="*49+"\n")
            line = i + " : "
            #print(i,":",end=" ")
            check(dicts,i,line)
    except:
        print("\nCan't Find.")
else:
    print("\nCan't Find")


