from functools import total_ordering
from molecule import MatchResult
import math
from parameter import params
from molecule import MatchResult
from config import config
import csvHelper as csvh

@total_ordering
class AlignedResult:
    def __init__(self, sample_num: int,  result: MatchResult=None, result_index=0) -> None:
        if result is not None:
            self.mz_theory: float = result.mz_theory
            self.mz_exp: float = result.mz_exp
            self.del_ppm: float = result.del_ppm
            self.retention_time: float = result.retention_time
            self.ion: str = result.ion
            self.category: str = result.category
            self.main_class: str = result.main_class
            self.sub_class = result.sub_class
            self.abbreviation: str = result.abbreviation
            self.formula: str = result.formula
            self.lm_id: str = result.lm_id
            self.name: str = result.name
            self.intensity_list: list[float] = [0.0]*sample_num
            self.intensity_list[result_index] = result.intensity
        else:
            self.mz_theory: float = 0.0
            self.mz_exp: float = 0.0
            self.del_ppm: float = 0.0
            self.retention_time: float = 0.0
            self.ion: str = ""
            self.category: str = ""
            self.main_class: str = ""
            self.sub_class = ""
            self.abbreviation: str = ""
            self.formula: str = ""
            self.lm_id: str = ""
            self.name: str = ""
            self.intensity_list: list[float] = [0.0]*sample_num

    def can_be_aligned(self, input:MatchResult) -> bool:
        return self.mz_exp == input.mz_exp and abs(self.retention_time - input.retention_time) < params.alignmentRetentionTimeVar and self.ion == input.ion and self.lm_id == input.lm_id

    def add_result(self, result: MatchResult, result_index:int):
        if self.can_be_aligned(result):
            self.intensity_list[result_index] += result.intensity

    def __eq__(self, o: object) -> bool:
        if isinstance(o, AlignedResult):
            return self.ion == o.ion and self.mz_exp == o.mz_exp and abs(self.retention_time - o.retention_time) < params.alignmentRetentionTimeVar and self.lm_id == o.lm_id       
        else:
            return False

    def __gt__(self, o: object) -> bool:
        # comparison priority: ion,mz_exp,retention_time
        if isinstance(o, AlignedResult):
            if self.ion > o.ion:
                return True
            elif self.ion < o.ion:
                return False
            if self.mz_exp > o.mz_exp:
                return True
            elif self.mz_exp < o.mz_exp:
                return False
            if self.retention_time - o.retention_time > params.alignmentRetentionTimeVar:
                return True
            elif self.retention_time - o.retention_time < -params.alignmentRetentionTimeVar:
                return False
            if self.lm_id > o.lm_id:
                return True
            elif self.lm_id < o.lm_id:
                return False
        return False
    
    def is_sibling(self, o: object) -> bool:
        if isinstance(o, AlignedResult):
            return self.ion == o.ion and self.mz_exp == o.mz_exp and self.retention_time == o.retention_time and self.lm_id != o.lm_id
        else:
            return False
    

    # to list for csv output
    def to_list(self) -> list:
        # "mz_t",
        # "mt_exp",
        # "retention_time",
        # "ion",
        # "lm_id",
        # "name",
        # "category",
        # "main_class",
        # "sub_class",
        # "formula",
        # "abbr"
        result = []
        result.append(self.mz_theory)
        result.append(self.mz_exp)
        result.append(self.retention_time)
        result.append(self.ion)
        result.append(self.lm_id)
        result.append(self.name)
        result.append(self.category)
        result.append(self.main_class)
        result.append(self.sub_class)
        result.append(self.formula)
        result.append(self.abbreviation)
        result += self.intensity_list
        return result

    def get_class(self,level: int) -> str:
        if level == 0:
            return "root"
        elif level == 1:
            return self.category
        elif level == 2:
            return self.main_class
        elif level == 3:
            return self.sub_class
        elif level == 4:
            return self.lm_id
        return None

class AlignedResults:
    def __init__(self, samples: list[str]=[]) -> None:
        self.samples: list[str] = samples
        self.sample_num = len(samples)
        self.rows: list[AlignedResult] = []
        self.title_list = []
        self.title_list +=config.AlignedResultsTitles
        for sample in samples:
            self.title_list.append(sample)
        # print(self.title_list)

    def addSampleName(self,name: str):
        self.samples.append(name)
        self.sample_num +=1

    def find_aligned_result(self, input:AlignedResult) -> tuple[bool,int]:
        # binary search for index
        # return True and the first index if found
        # return False and the index to insert if not found
        left = 0
        right = len(self.rows)-1
        while left <= right:
            mid = (left+right)//2
            if self.rows[mid] == input:
                return True,mid
            elif self.rows[mid] > input:
                right = mid-1
            else:
                left = mid+1
        return False,left 
    
    def AddResult(self, row: MatchResult, sample_name: str):
        sample_index = self.samples.index(sample_name)
        data = AlignedResult(self.sample_num,row,sample_index)
        found, idx = self.find_aligned_result(data)
        if not found:
            self.rows.insert(idx, data)
        else:
            self.rows[idx].add_result(row,sample_index)

    def SaveCSV(self, target: str):
        print("Start aligning")
        data_to_be_save=[]
        for row in self.rows:
            data: list = row.to_list()
            for it in row.intensity_list:
                data.append(it)
            data_to_be_save.append(data)
        csvh.SaveDataCSV(target,data_to_be_save,self.title_list)
        print('Align results SUCCESS!')

if __name__ == "__main__":
    a = 5.8003
    b = 90.8917
    if math.isclose(a, b, abs_tol=0.01):
       print("{}={}".format(a,b))
    else:
        print("{}!={}".format(a,b))
