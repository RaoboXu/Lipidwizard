import os.path
import csv

def SaveDataCSV(target_path: str, data: list, titles: list[str] = list()):
    print('Writing data to file:'+target_path)
    with open(target_path, 'w', newline='',encoding='utf8') as file:
        # Create a CSV writer object
        writer = csv.writer(file)
        # Write the data to the CSV file
        if(len(titles)>0):
            writer.writerow(titles)
        for row in data:
            writer.writerow(row)
    print('Writing data'+target_path+' SUCCESS!')

def checkTableTitles(tableTitles: list, targetTitles=[]):
    for col in targetTitles:
        if not tableTitles.count(col):
            return False
        return True
    
def ReadDataCSV(target_path:str, result:list,  headers=[]):
    print("Start reading {file_name}".format(file_name=target_path))
    if(not os.path.exists(target_path)):
        print(target_path+"does not exist!")
        return "FAILED"
    with open(target_path, 'r',encoding='utf8') as file:
        # Create a CSV reader object
        reader = csv.reader(file)
        row0=[]
        for row in reader:
            row0 = row
            break
        # Loop through each row in the CSV file
        if(len(headers)>0 and checkTableTitles(row0,headers) is False):
            print(target_path + 'has no content you want to read')
            return "FAILED"
        i =0
        result.append(row0)
        for row in reader:
            result.append(row)
            i += 1
            if(i%1000==0):
                print(("\rReading{dot}").format(dot="."*(i//1000)),end=" ")
        print()
        print("Complete reading {file_name}".format(file_name=target_path))
        return 'SUCCESS'
    