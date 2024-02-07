from functools import total_ordering
from config import config
from alignment import AlignedResult
from threading import Lock
import csvHelper as csvh
from parameter import params
from PySide6.QtGui import QStandardItem

result_node_write_lock = Lock()
@total_ordering
class ResultNode(QStandardItem):
    def __init__(self,cls_name:str="root",sample_num:int=0, parent=None) -> None:
        super().__init__()
        self.cls_name = cls_name
        self.mz_theory = 0.0
        self.mz_exp = 0.0
        self.del_ppm = 0.0
        self.retention_time = 0.0
        self.ion = ""
        self.parent=parent
        self.level = 0
        self.result_list:list[AlignedResult]=[]
        self.sample_num = sample_num
        self.intensity_list:list[float] = [0.0]*sample_num
        self.children = list[ResultNode]()
        if parent is not None:
            self.level = parent.level + 1
        # self.populated = False
    
    def __eq__(self, o: object) -> bool:
        if isinstance(o, ResultNode):
            return self.cls_name == o.cls_name and self.level == o.level
        else:
            return False
    
    def __gt__(self, o: object) -> bool:
        if isinstance(o, ResultNode):
            if self.level > o.level:
                return True
            elif self.level < o.level:
                return False
            else:
                return self.cls_name > o.cls_name
        else:
            return False
    
    def locate_result(self,row:AlignedResult)->tuple[bool,int]:
        # binary search
        # return True and the first index of the result if found 
        # return False and the index that the result should be inserted
        if row is None:
            return False,0
        left = 0
        right = len(self.result_list)-1
        while left <= right:
            mid = (left+right)//2
            if self.result_list[mid] == row:
                return True,mid
            elif self.result_list[mid] < row:
                left = mid+1
            else:
                right = mid-1
        return False,left
        
    def find_child(self,child_name)->tuple[bool,int]:
        # binary search
        # return True and the first index of the child if found 
        # return False and the index that the child should be inserted
        if child_name is None:
            return False,0
        left = 0
        right = len(self.children)-1
        while left <= right:
            mid = (left+right)//2
            if self.children[mid].cls_name == child_name:
                return True,mid
            elif self.children[mid].cls_name < child_name:
                left = mid+1
            else:
                right = mid-1
        return False,left

    def insert_result(self,input:AlignedResult):
        if input is None:
            return
        if self.level == params.result_merge_level+1:
            self.mz_exp = input.mz_exp
            self.mz_theory = input.mz_theory
            self.del_ppm = input.del_ppm
            self.retention_time = input.retention_time
            self.ion = input.ion
            if len(self.result_list) == 0:
                for i in range(self.sample_num):
                    self.intensity_list[i] = input.intensity_list[i]
                parent = self.parent
                while parent is not None:
                    for i in range(self.sample_num):
                        parent.intensity_list[i] += input.intensity_list[i]
                    parent = parent.parent
            found, idx = self.locate_result(input)
            if not found:
                self.result_list.insert(idx,input)
        elif self.level == params.result_merge_level:
            found, idx = self.find_child(input.lm_id)
            if not found:
                for i in range(len(self.children)):
                    if input.is_sibling(self.children[i].result_list[0]):
                        found_, idx_ = self.children[i].locate_result(input)
                        if not found_:
                            self.children[i].result_list.insert(idx_,input)
                        return
                node = ResultNode(input.lm_id,self.sample_num,self)
                self.children.insert(idx,node)
                self.children[idx].insert_result(input)        
        else:
            cls_name = input.get_class(self.level+1)
            found, idx = self.find_child(cls_name)
            if not found:
                node = ResultNode(cls_name,self.sample_num,self)
                self.children.insert(idx,node)
            self.children[idx].insert_result(input)
        
    
    def child(self, index:int):
        if index < len(self.children):
            return self.children[index]
        else:
            return None

    def child_num(self):
        return len(self.children)

    def result_num(self):
        if self.child_num() == 0:
            return len(self.result_list)
        r = 0
        for child in self.children:
            r += child.result_num()
        return r

    def attr_num(self):
        return len(config.TreeNodeTitles)+self.sample_num
    
    def data(self,index):
        return self[index]
        
    def __getitem__(self,key):
        if type(key) is int:
            if key == 0:
                if self.child_num() > 0:
                    return self.cls_name
                else:
                    return None
            if key == 1:
                    return self.result_num()
            lm_ids =""
            names = ""
            abbrs = ""
            formulas = ""
            for r in self.result_list:
                lm_ids += r.lm_id + "*"
                names += r.name + "*"
                abbrs += r.abbreviation + "*"
                formulas += r.formula + "*"
            if len(self.result_list) >0:
                lm_ids = lm_ids[:-1]
                names = names[:-1]
                abbrs = abbrs[:-1]
                formulas = formulas[:-1]
            if key == 2:
                return lm_ids
            if key == 3 and len(self.result_list) > 0:
                return "{:.6f}".format(self.mz_theory)
            if key == 4 and len(self.result_list) > 0:
                return "{:.6f}".format(self.mz_exp)
            if key == 5 and len(self.result_list) > 0:
                return "{:.2f}".format(self.retention_time)
            if key == 6:
                return self.ion
            if key == 7:
                return names
            if key == 8:
                return formulas
            if key == 9:
                return abbrs
            if key > 9:
                return "{:.6f}".format(self.intensity_list[key-10])
        if type(key) is str:
            return None
        
    def to_list(self):
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
        result=[]
        result.append(self.mz_theory)
        result.append(self.mz_exp)
        result.append(self.retention_time)
        result.append(self.ion)
        ids = ""
        names = ""
        abbrs = ""
        formulas = ""
        category = ""
        main_class = ""
        sub_class = ""
        for r in self.result_list:
            ids += r.lm_id + "*"
            names += r.name + "*"
            abbrs += r.abbreviation + "*"
            formulas += r.formula + "*"
            category += r.category+ "*"
            main_class += r.main_class+ "*"
            sub_class += r.sub_class+ "*"
        if len(self.result_list) > 0:
            ids = ids[:-1]
            names = names[:-1]
            abbrs = abbrs[:-1]
            formulas = formulas[:-1]
            category = category[:-1]
            main_class = main_class[:-1]
            sub_class = sub_class[:-1]
        result.append(ids)
        result.append(names)
        if params.result_merge_level>0:
            result.append(category.split("*")[0])
        else:
            result.append(category)
        if params.result_merge_level>1:
            result.append(main_class.split("*")[0])
        else:
            result.append(main_class)
        if params.result_merge_level>2:
            result.append(sub_class.split("*")[0])
        else:
            result.append(sub_class)
        result.append(formulas)
        result.append(abbrs)
        result.extend(self.intensity_list)

        return result
        
    def to_aligned_result_list(self)->list:
        result_list = []
        if self.child_num() > 0:
            for child in self.children:
                result_list.extend(child.to_aligned_result_list())
        else:
            return [self.to_list()]
        return result_list
        
    def save_to_csv(self,path,samples:list[str]=None):
        result_list = self.to_aligned_result_list()
        csvh.SaveDataCSV(path, result_list, config.AlignedResultsTitles+samples)
        
    def stat(self,level:int)->list:
        if self.level == level:
            return [[self.cls_name, self.result_num()]+self.intensity_list]
        elif self.level < level:
            result = []
            for child in self.children:
                result.extend(child.stat(level))
            return result
        else:
            return None
        
