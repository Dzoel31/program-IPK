import os, pandas as pd
from collections import namedtuple
from prettytable import PrettyTable

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

def checkFile() -> bool:
    if os.path.exists(FILENAME):
        return True
    else:
        emptyFile = pd.DataFrame(columns=COLUMNS_NAME)
        emptyFile.to_csv(f"{FILENAME}", index=False)

def readData():
    readData = pd.read_csv(f"{FILENAME}")
    currentData = readData.values.tolist()
    if currentData:
        semester, mataKuliah, SKS, nilai = map(list, zip(*currentData))
    else:
        semester, mataKuliah, SKS, nilai = ([] for _ in range(4))
    dataNilai = namedtuple("dataNilai", [
        "currentData",
        "semester",
        "mataKuliah",
        "SKS",
        "nilai"])
    
    return dataNilai (currentData, semester, mataKuliah, SKS, nilai)

def writeData(new_data):
    data = readData()
    tempData = data.currentData

    tempData.extend(new_data)

    saveData = pd.DataFrame(tempData,columns=COLUMNS_NAME)
    saveData.to_csv(f"{FILENAME}", index=False)

def inputData():
    data = readData()
    listData = []
    urutanSemester = int(input("Semester : "))
    
    while urutanSemester in data.semester:
        print(f"Data semester {urutanSemester} sudah tersedia!")
        urutanSemester = int(input("Semester : "))
    
    banyakMataKuliah = int(input("Banyak mata kuliah : "))
    for _ in range(banyakMataKuliah):
        mataKuliah = input("Nama mata kuliah : ")
        SKS = int(input("Jumlah SKS : "))
        nilai = input("Nilai : ")
        
        tempData = [urutanSemester, mataKuliah, SKS, nilai]
        
        listData.append(tempData)
    
    writeData(listData)

def hitungIPK():
    data = readData()
    totalSKS = 0
    totalIndeksPrestasi = 0

    for i in range(len(data.currentData)):
        totalSKS += data.SKS[i]
        totalIndeksPrestasi += ANGKAMUTU[data.nilai[i]] * data.SKS[i]
    
    IPK = totalIndeksPrestasi / totalSKS
    
    return IPK


def showData():
    data = readData()
    IPK = hitungIPK()
    print("="*20)
    print("|{:<15}{}|".format("IPK Anda : ", IPK))
    print("="*20)
    
    table = PrettyTable()
    table.field_names = ["Semester", "Mata Kuliah", "SKS", "Nilai", "Mutu", "SKS x Nilai"]

    for i in range(len(data.currentData)):
        SKSxNilai = data.SKS[i] * ANGKAMUTU[data.nilai[i]]
        table.add_row([data.semester[i],data.mataKuliah[i], data.SKS[i], data.nilai[i], ANGKAMUTU[data.nilai[i]], SKSxNilai])
    
    print(table)

def main():
    while True:
        os.system("cls")
        checkFile()
        print("-"*30)
        print("|{:^28}|".format("Menu Utama"))
        print("-"*30)
        print("[1] Input Nilai")
        print("[2] Lihat IP & IPK")
        print("[3] Exit")
        choose = int(input("Pilih menu: "))

        if choose == 1:
            inputData()
        elif choose == 2:
            showData()
        elif choose == 3:
            print("Exit program...")
            exit()
        else:
            print("Menu yang dipilih tidak tersedia")
        
        status = input("Continue ? [Y or Any Key/N] : ").upper()

        if status == "N":
            print("Exit program...")
            exit()

main()