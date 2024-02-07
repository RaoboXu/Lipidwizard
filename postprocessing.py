from molecule import MatchResult
import ecn_filter
import ert_filter
from alignment import AlignedResults,AlignedResult
from csvHelper import SaveDataCSV,ReadDataCSV

def FilterByECN(input:list[MatchResult],ecn_filt_type:str) -> list[MatchResult]:
    result: list[MatchResult]=[]
    log_tic = 0
    progress = "."
    for item in input:
        if ecn_filter.pass_ecn_filter_mr(item,ecn_filter.ecn_profile,ecn_filt_type):
           result.append(item)
        log_tic += 1
        if log_tic % 3000 == 0:
           progress += "."
           log_tic = 0
        if len(progress) > 16:
            progress = "."
        print("\r2D RT Filtering:{:16s}".format(progress), end="")
    print()
    print("2D RT Filtering Complete!")
    return result

def FilterByERT(input:list[MatchResult]) -> list[MatchResult]:
    result: list[MatchResult]=[]
    log_tic = 0
    progress = "."
    for item in input:
        if ert_filter.pass_ert_filter_mr(item,ert_filter.ert_profile):
            result.append(item)
        log_tic += 1
        if log_tic % 3000 == 0:
           progress += "."
           log_tic = 0
        if len(progress) > 16:
            progress = "."
        print("\r1D RT Filtering:{:16s}".format(progress), end="")
    print()
    print("1D RT Filtering Complete!")
    return result


def mergeSimilarResultsByMainClass(data: list[MatchResult]):
    data.sort(key=lambda item: item.main_class)
    data_new: list[MatchResult] = []
    data_new.append(data.pop(0))
    for row in data:
        if data_new[-1].main_class == row.main_class:
            data_new[-1].lm_id += ('*'+str(row.lm_id))
            data_new[-1].name += ('*'+str(row.name))
            data_new[-1].sub_class += ('*' + str(row.sub_class))
            # data_new[-1].abbreviation += ('*' + str(row.abbreviation))
        else:
            data_new.append(row)
    return data_new

def mergeSimilarResultsByCategory(data: list[MatchResult]):
    data.sort(key=lambda item: item.category)
    data_new: list[MatchResult] = []
    data_new.append(data.pop(0))
    for row in data:
        if data_new[-1].category == row.category:
            data_new[-1].lm_id += ('*'+str(row.lm_id))
            data_new[-1].name += ('*'+str(row.name))
            data_new[-1].main_class += ('*' + str(row.main_class))
            data_new[-1].sub_class += ('*' + str(row.sub_class))
        else:
            data_new.append(row)
    return data_new

def CombineSimilarResults(input:list[MatchResult],merge_level="MAIN_CLASS")->list[MatchResult]:
    input.sort(key= lambda item: (item.mz_exp,item.retention_time,item.ion))
    result:list[MatchResult] = []
    i = 0
    l_r = len(input)
    while i < l_r:
        j = i+1
        while j<l_r and input[j].mz_exp == input[i].mz_exp and input[i].retention_time == input[j].retention_time and input[j].ion == input[i].ion:
            j += 1
        if merge_level == "MAIN_CLASS":
            result += mergeSimilarResultsByMainClass(input[i:j])
        if merge_level == "CATEGORY":
            result += mergeSimilarResultsByCategory(input[i:j])
        i = j
    return result

def CombineSimilarAlignedResults(input:list[AlignedResult],merge_level="MAIN_CLASS")->list[AlignedResult]:
    input.sort(key= lambda item: (item.mz_exp,item.retention_time,item.ion))
    result:list[AlignedResult] = []
    i = 0
    l_r = len(input)
    while i < l_r:
        j = i+1
        while j<l_r and input[j].mz_exp == input[i].mz_exp and input[i].retention_time == input[j].retention_time and input[j].ion == input[i].ion:
            j += 1
        if merge_level == "MAIN_CLASS":
            result += mergeSimilarAlignedResultsByMainClass(input[i:j])
        if merge_level == "CATEGORY":
            result += mergeSimilarAlignedResultsByCategory(input[i:j])
        i = j
    return result

def mergeSimilarAlignedResultsByMainClass(data: list[AlignedResult]):
    data.sort(key=lambda item: item.main_class)
    data_new: list[AlignedResult] = []
    data_new.append(data.pop(0))
    for row in data:
        if data_new[-1].main_class == row.main_class:
            data_new[-1].lm_id += ('*'+str(row.lm_id))
            data_new[-1].name += ('*'+str(row.name))
            data_new[-1].sub_class += ('*' + str(row.sub_class))
        else:
            data_new.append(row)
    return data_new

def mergeSimilarAlignedResultsByCategory(data: list[AlignedResult]):
    data.sort(key=lambda item: item.category)
    data_new: list[AlignedResult] = []
    data_new.append(data.pop(0))
    for row in data:
        if data_new[-1].category == row.category:
            data_new[-1].lm_id += ('*'+str(row.lm_id))
            data_new[-1].name += ('*'+str(row.name))
            data_new[-1].main_class += ('*' + str(row.main_class))
            data_new[-1].sub_class += ('*' + str(row.sub_class))
        else:
            data_new.append(row)
    return data_new

def CombineByCategory(data:AlignedResults, save_path:str):
    rst:dict[str,list]={}
    for item in data.rows:
        if item.category in rst:
            for i in range(len(rst[item.category])):
                rst[item.category][i] += item.sample_intensity[i]
        else:
            rst[item.category] = item.sample_intensity.copy()
    to_save=[["Category"]+data.samples]
    for key in rst.keys():
        to_save.append([key]+rst[key])
    SaveDataCSV(save_path,to_save)

def CombineByMainClass(data:AlignedResults, save_path:str):
    rst:dict[str,list]={}
    for item in data.rows:
        if item.main_class in rst:
            for i in range(len(rst[item.main_class])):
                rst[item.main_class][i] += item.sample_intensity[i]
        else:
            rst[item.main_class] = item.sample_intensity.copy()
    to_save=[["MainClass"]+data.samples]
    for key in rst.keys():
        to_save.append([key]+rst[key])
    SaveDataCSV(save_path,to_save)

def CombineBySubClass(data:AlignedResults, save_path:str):
    rst:dict[str,list]={}
    for item in data.rows:
        all_sub_cls = [i for i in item.sub_class.split('*') if len(i)>0]
        sub_cls_set =set()
        for sub_class in all_sub_cls:
            sub_cls_set.add(sub_class)
        for sub_class in sub_cls_set:
            if sub_class in rst:
                for i in range(len(rst[sub_class])):
                    rst[sub_class][i] += item.sample_intensity[i]
            else:
                rst[sub_class] = item.sample_intensity.copy()
    to_save=[["SubClass"]+data.samples]
    for key in rst.keys():
        to_save.append([key]+rst[key])
    SaveDataCSV(save_path,to_save)
                

def CombineBySubClassPure(data:AlignedResults, save_path:str):
    rst:dict[str,list]={}
    for item in data.rows:
        if(len(item.sub_class)==0):
            continue
        if len(item.sub_class)>0 and ('*' == item.sub_class[0] or '*' == item.sub_class[-1] or "**" in item.sub_class):
            continue
        all_sub_cls = [i for i in item.sub_class.split('*')]
        sub_cls_set =set()
        for sub_class in all_sub_cls:
            sub_cls_set.add(sub_class)
        if len(sub_cls_set) == 1:
            sub_class=sub_cls_set.pop()
            if sub_class in rst:
                for i in range(len(rst[sub_class])):
                    rst[sub_class][i] += item.sample_intensity[i]
            else:
                rst[sub_class] = item.sample_intensity.copy()
    to_save=[["SubClassPure"]+data.samples]
    for key in rst.keys():
        to_save.append([key]+rst[key])
    SaveDataCSV(save_path,to_save)

if __name__ == '__main__':
    print("test")
    test_data = []
    test_aligned_results = AlignedResults()
    if ReadDataCSV("./test/test.csv", test_data) == 'SUCCESS':
        test_data.pop(0)
        for row in test_data:
            match_result = MatchResult(row)
            match_result.sub_class=row[8]
            aligned_result=AlignedResult(match_result,69)
            for i in range(69):
                aligned_result.sample_intensity[i]=float(row[i+11])
            test_aligned_results.rows.append(aligned_result)
    CombineBySubClass(test_aligned_results,"./test/test_sub_class_2.csv")
    CombineBySubClassPure(test_aligned_results,"./test/test_sub_class_pure_2.csv")
        
            
