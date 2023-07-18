import os, pandas as pd
from collections import namedtuple, OrderedDict
from prettytable import PrettyTable
import matplotlib.pyplot as plt

FILENAME = ".\\data_nilai_semester.csv"
COLUMNS_NAME = ["Semester", "Mata Kuliah", "Jumlah SKS", "Nilai"]
ANGKAMUTU = {
        "A" : 4,
        "A-" : 3.75,
        "B+" : 3.5,
        "B" : 3,
        "B-" : 2.75,
        "C+" : 2.5,
        "C" : 2,
        "D" : 1,
        "E" : 0
    }

def checkFile():
    if os.path.exists(FILENAME):
        return True
    else:
        emptyFile = pd.DataFrame(columns=COLUMNS_NAME)
        emptyFile.to_csv(f"{FILENAME}", index=False)

def readData():
    readData = pd.read_csv(f"{FILENAME}")
    currentData = readData.values.tolist()
    semester = readData["Semester"].drop_duplicates().tolist()
    if currentData:
        semesterDuplicate, mataKuliah, SKS, nilai = map(list, zip(*currentData))
    else:
        semesterDuplicate, mataKuliah, SKS, nilai = ([] for _ in range(4))
    dataNilai = namedtuple("dataNilai", [
        "currentData",
        "semesterDuplicate",
        "semester",
        "mataKuliah",
        "SKS",
        "nilai"])
    
    return dataNilai (currentData, semesterDuplicate, semester, mataKuliah, SKS, nilai)

def writeData(new_data):
    data = readData()
    tempData = data.currentData

    tempData.extend(new_data)

    saveData = pd.DataFrame(tempData,columns=COLUMNS_NAME)
    saveData.to_csv(f"{FILENAME}", index=False)

def newData(urutanSemester, indeks):
    os.system("cls")
    print(f"Input data mata kuliah ke-{indeks + 1}")
    mataKuliah = input("Nama mata kuliah : ").title()
    SKS = int(input("Jumlah SKS : "))
    nilai = input("Nilai : ").upper()
    data = [urutanSemester, mataKuliah, SKS, nilai]

    return data

def inputData():
    data = readData()
    listData = []
    urutanSemester = int(input("Semester : "))
    
    while urutanSemester in data.semester:
        print(f"Data semester {urutanSemester} sudah tersedia!")
        urutanSemester = int(input("Semester : "))
    
    banyakMataKuliah = int(input("Banyak mata kuliah : "))
    for i in range(banyakMataKuliah):
        tempData = newData(urutanSemester, i)
        
        listData.append(tempData)
    
    writeData(listData)

def hitungIPK():
    data = readData()
    totalSKS = 0
    totalSKSxM = 0

    for i in range(len(data.currentData)):
        totalSKS += data.SKS[i]
        totalSKSxM += ANGKAMUTU[data.nilai[i]] * data.SKS[i]
    
    IPK = totalSKSxM / totalSKS
    
    return IPK

def hitungIP(semester):
    data = readData()

    jumlah = data.semesterDuplicate.count(semester)
    indeks = data.semesterDuplicate.index(semester)
    totalSKS = 0
    totalSKSxM = 0

    for i in range(indeks, indeks + jumlah):
        totalSKS += data.SKS[i]
        totalSKSxM += ANGKAMUTU[data.nilai[i]] * data.SKS[i]
    
    IP = totalSKSxM / totalSKS
    return IP

def showData():
    os.system("cls")
    data = readData()
    IPK = hitungIPK()
    
    tableIPK = PrettyTable()
    tableIPK.field_names = ["IPK Anda"]
    tableIPK.add_row(["{:.2f}".format(IPK)])
    
    print(tableIPK)

    table = PrettyTable()
    table.field_names = ["Semester", "Mata Kuliah", "SKS", "Nilai", "Mutu", "SKS x Nilai"]
    table.align["Mata Kuliah"] = "l"
    for semester in data.semester:
        jumlah = data.semesterDuplicate.count(semester)
        indeks = data.semesterDuplicate.index(semester)
        IP = hitungIP(semester)

        for i in range(indeks, indeks + jumlah):
            SKSxNilai = data.SKS[i] * ANGKAMUTU[data.nilai[i]]
            table.add_row([semester ,data.mataKuliah[i], data.SKS[i], data.nilai[i], ANGKAMUTU[data.nilai[i]], SKSxNilai])
        print(table)
        table.clear_rows()

        tableIP = PrettyTable()
        tableIP.field_names = [f"IP Semester {semester}"]
        tableIP.add_row(["{:.2f}".format(IP)])
        print(tableIP)

def showChart():
    data = readData()
    listIP = []

    for semester in data.semester:
        IP = hitungIP(semester)
        listIP.append(round(IP, 2))
    
    print("Menampilkan grafik...")
    plt.plot(data.semester, listIP, marker = "o")
    plt.title("Grafik IPK")
    plt.xlabel("Semester")
    plt.ylabel("IP")
    plt.show()

def main():
    while True:
        os.system("cls")
        checkFile()
        print("-"*30)
        print("|{:^28}|".format("Menu Utama"))
        print("-"*30)
        print("[1] Input Nilai")
        print("[2] Lihat IP & IPK")
        print("[3] Lihat Grafik")
        print("[0] Exit")
        choose = int(input("Pilih menu: "))

        if choose == 1:
            inputData()
        elif choose == 2:
            showData()
        elif choose == 3:
            showChart()
        elif choose == 0:
            print("Exit program...")
            exit()
        else:
            print("Menu yang dipilih tidak tersedia")
        
        status = input("Continue ? [Y or Any Key/N] : ").upper()

        if status == "N":
            print("Exit program...")
            exit()

main()