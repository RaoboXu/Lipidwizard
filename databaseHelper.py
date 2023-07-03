import os.path
import os
from typing import List

import requests

from config import config
from molecule import Molecule, Peak, MatchResult
import zipfile
import csvHelper as csvh

def DownloadDatabase(url: str, where_to_save: str):
    print('Downloading from: '+url)
    file = 'a.zip'
    r = requests.get(url, allow_redirects=True)
    open(file, 'wb').write(r.content)
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(where_to_save))
    os.remove('a.zip')
    print('Download SUCCESS!')


def statCategories(database: List[Molecule]):
    config.CATEGORIES.clear()
    config.MAIN_CLASSES.clear()
    config.SUB_CLASSES.clear()
    for molecule in database:
        cat_name = molecule.getValue('CATEGORY')
        main_cls_name = cat_name+"."+molecule.getValue('MAIN_CLASS')
        sub_cls = molecule.getValue('SUB_CLASS')
        if sub_cls is None:
            sub_cls = ''
        sub_cls_name = main_cls_name+'.'+ sub_cls
        if cat_name and cat_name != '' and cat_name not in config.CATEGORIES:
            config.CATEGORIES.append(cat_name)
        if main_cls_name and main_cls_name != ''and main_cls_name not in config.MAIN_CLASSES:
            config.MAIN_CLASSES.append(main_cls_name)
        if sub_cls_name and sub_cls_name !='' and sub_cls_name not in config.SUB_CLASSES:
            config.SUB_CLASSES.append(sub_cls_name)


def readDatabaseFromCSV(file: str,database:list):
    xlData = []
    if csvh.ReadDataCSV(file,xlData) == 'SUCCESS':
        args = xlData.pop(0)
        database+=readMolecule(xlData,args)
        return 'SUCCESS'
    return "FAILED"


def readSDF(source='') -> List[Molecule]:
    print("Loading database")
    if source != '' and os.path.exists(source):
        f = open(source, 'r', encoding='utf8')
        database = []
        molecule = Molecule()
        line = f.readline()
        i=0
        while line:
            if line[0] == '>':
                i0 = line.rindex('<')+1
                i1 = line.rindex('>')
                attrName = line[i0: i1]
                if attrName in config.DatabaseColumnTitles:
                    attrValue = f.readline()
                    attrValue = attrValue[0: len(attrValue)-1]
                    molecule.setValue(attrName, attrValue)
            if len(line) >= 4 and line[0: 4] == '$$$$':
                molecule.statElements()
                if molecule.is_legal():
                    molecule.calMZ()
                    database.append(molecule)
                else:
                    # print(molecule.getValue('FORMULA'))
                    pass
                molecule = Molecule()
            line = f.readline()
            i = (i+1)%1e9
            if(i%1e6 == 0):
                print("\rLoading{dot}".format(dot="."*int(i//1e6)),end=' ')
        f.close()
        print("\n\rLoading database finished")
        return database
    else:
        print('source file: \'' + source + '\' does not exists')
        return []


def readMolecule(xlsx_data: List, args: List[str]) -> List[Molecule]:
    res = list()
    for row in xlsx_data:
        molecule = Molecule()
        molecule.args = args
        molecule.argv = row
        res.append(molecule)
    return res


def SaveMoleculesToCSV(data: List[Molecule], target: str):
    _data = []
    for m in data:
        _data.append(m.argv)
    if len(data) > 0:
        csvh.SaveDataCSV(target,_data,data[0].args)


def UpdateDatabase():
    DownloadDatabase(config.DatabaseUrl, config.DatabaseFile)
    database = readSDF(config.DatabaseFile)
    statCategories(database)
    config.UpdateConfig()
    # SaveMoleculesToXlsx(ms, config.DatabaseXlsxFile)
    SaveMoleculesToCSV(database, config.DatabaseCSVFile)


def FilterByClass(molecules: List[Molecule],
                  cat_filters: List[str],
                  cls_filters: List[str]):
    rs = []
    if len(cat_filters) == 0 or cls_filters == 0:
        return rs
    if cat_filters == 'ALL':
        return molecules
    for comp in molecules:
        cat = comp.argv[comp.args.index('CATEGORY')]
        cls = comp.argv[comp.args.index('MAIN_CLASS')]
        if cat in cat_filters and cls in cls_filters:
            rs.append(comp)
    return rs

database = []
db=[]
iso_profiles=[]

if __name__ == '__main__':
    print('test')
    # database = readDatabaseFromXlsx("./data/database_simple.xlsx")
    # database = readSDF("./data/structures.sdf")
    # cats = statCategories(database)
    # config.CATEGORY_ROOT = cats
    db=[]
    readDatabaseFromCSV(config.DatabaseCSVFile,db)
    statCategories(db)
    config.UpdateConfig()
    # UpdateDatabase()
    # database.sort(key=lambda molecule: float(molecule.getValue('EXACT_MASS')))
    # peak = Peak(200.2012364,	1058397.427,	70.84439746,	0.002374)
    # res_i = binary_match(peak, database, "[M+H]+", 2.1e-6)
    # print(res_i)
    # for i in res_i:
    #     print(database[i])
