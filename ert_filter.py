import os
from config import config
import xlHelper as xlh
from matching import MatchResult
from molecule import IsotopicVariants

def ReadERTProfiles():
    ert_profile = dict()
    file_path = config.ERTFile
    if os.path.exists(file_path):
        data=[]
        xlh.readXlsx(file_path,data)
        data.pop(0)
        for row in data:
            class_name = [x for x in str(row[0]).split('.') if x][-1]
            ert_profile[class_name]=(row[1],row[2])
            print("{cls}:\r{space}{rts}-{rte}".format(cls=class_name,space='\t'*12,rts=row[1],rte=row[2]))
    return ert_profile

def pass_ert_filter_mr(item:MatchResult,ert_profile:dict):
    passed = True
    if item.category in ert_profile.keys():
        rt_range = ert_profile[item.category]
        if item.retention_time<rt_range[0] or item.retention_time>rt_range[1]:
            passed = False
    if item.main_class in ert_profile.keys():
        rt_range = ert_profile[item.main_class]
        if item.retention_time<rt_range[0] or item.retention_time>rt_range[1]:
            passed = False
    if item.sub_class in ert_profile.keys():
        rt_range = ert_profile[item.sub_class]
        if item.retention_time<rt_range[0] or item.retention_time>rt_range[1]:
            passed = False
    return passed

def pass_ert_filter_iso(item:IsotopicVariants, rt: float, ert_profile:dict):
    category = item.mol.getValue("CATEGORY")
    main_class = item.mol.getValue("MAIN_CLASS")
    sub_class = item.mol.getValue("SUB_CLASS")

    passed = True
    if category in ert_profile.keys():
        rt_range = ert_profile[category]
        if rt<rt_range[0] or rt>rt_range[1]:
            passed = False
    if main_class in ert_profile.keys():
        rt_range = ert_profile[main_class]
        if rt<rt_range[0] or rt>rt_range[1]:
            passed = False
    if sub_class in ert_profile.keys():
        rt_range = ert_profile[sub_class]
        if rt<rt_range[0] or rt>rt_range[1]:
            passed = False
    return passed

ert_profile=ReadERTProfiles() # item of ecn contains [0]:ci(ecn)[0]-lowerbound, ci[ecn][1]-upperbound; [1]:k- used for calc_ecn
