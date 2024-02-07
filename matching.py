from molecule import MatchResult,Molecule,Peak
from config import config
from time import process_time
import csvHelper as csvh

def rel_delta(a: float, theory: float):
    return (a-theory) / theory

def SaveMatchResultCSV(results: list[MatchResult], target:str):
    data = []
    for r in results:
        data.append(r.to_list())
    csvh.SaveDataCSV(target, data, config.MatchedResultsTitles)

def ReadMatchResultsCSV(source:str)->list[MatchResult]:
    rs:list[MatchResult]=[]
    data = []
    if csvh.ReadDataCSV(source,data,config.MatchedResultsTitles) == 'SUCCESS':
        data.pop(0)
        for row in data:
            r = MatchResult()
            if r.from_list(row) == 'SUCCESS':
                rs.append(r)
    else:
        print("Reading csv failed")    
    return rs

def pass_category_filter(result:MatchResult,filter:list[str]):
    return result.category and result.category != '' and result.category in filter

def pass_main_class_filter(result:MatchResult,filter:list[str]):
    return result.main_class and result.main_class != '' and result.main_class in filter

def binary_match(peak: Peak, database: list[Molecule], comparator: str, var: float):
    end = len(database)
    low = 0
    high = end-1
    mid = 0
    rs = list()
    while low <= high:
        mid = (high+low) // 2
        mz = float(peak.mz)
        mass = float(database[mid].getValue(comparator))
        delta = var+1
        if mass > 0:
            delta = rel_delta(mz, mass)
        if delta < -var:
            high = mid-1
        elif delta > var:
            low = mid+1
        else:
            rs.append(mid)
            # find all neighbors which meet the condition
            # forward search
            i = mid+1
            while i < end:
                mass = float(database[i].getValue(comparator))
                delta = var+1
                if mass>0:
                    delta = rel_delta(mz, mass)
                if abs(delta) < var:
                    rs.append(i)
                    i += 1
                else:
                    break
            # backward search
            i = mid - 1
            while i >= 0:
                mass = float(database[i].getValue(comparator))
                delta = var + 1
                if mass > 0:
                    delta = rel_delta(mz, mass)
                if abs(delta) < var:
                    rs.append(i)
                    i -= 1
                else:
                    break
            break
    return rs

def matchDatabase(database: list[Molecule], peaks: list[Peak], comparators: list[str], var: float):
    print('Number of peak need to match:\t{}'.format(len(peaks)))
    print('size of database:\t{}'.format(len(database)))
    t0 = process_time()
    res = []
    catch_num = 0
    var *= 1e-6
    i = 0
    while i < len(peaks):
        peak = peaks[i]
        matched = False
        for ion in comparators:
            res_i = binary_match(peak, database, ion, var)
            l_r = len(res_i)
            for mi in res_i:
                molecule = database[mi]
                r = MatchResult(ion, peak, molecule)
                # resultnode.root.add_result(r_cpy)
                # if pass_category_filter(r,params.Catagories) and pass_main_class_filter(r,params.MainClasses):
                res.append(r)
            if l_r >0:
                catch_num += 1
                matched = True
        if matched: 
            peaks.pop(i)
        else:
            i += 1
    t1 = process_time()
    print('Number of matched peaks:\t{}'.format(catch_num))
    print('Remains:\t\t{}'.format(len(peaks)))
    print("time cost: " + str(t1-t0))
    return res


if __name__ == '__main__':
    print('test')
    # database = readDatabaseFromXlsx(config.DatabaseXlsxFile)
    # database.sort(key=lambda molecule: float(molecule.getValue('EXACT_MASS')))
    # peak = Peak(200.2012364,	1058397.427,	70.84439746,	0.002374)
    # res_i = binary_match(peak, database, "[M+H]+", 2.1e-6)
    # print(res_i)
    # for i in res_i:
    #     print(database[i])