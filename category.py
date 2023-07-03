import json
class CATEGORY_NODE():
    def __init__(self,name:str="root",parent=None) -> None:
        self.args = []
        self.argv = []
        self.args.append('name')
        self.argv.append(name)
        self.args.append("child number")
        self.argv.append(0)
        self.args.append("est_rt_lo_m")
        self.argv.append(None)
        self.args.append("est_rt_up_m")
        self.argv.append(None)
        self.children = list[CATEGORY_NODE]()
        self.parent=parent
        self.level = 0
        self.match_results=[]
        if parent is not None:
            self.level = parent.level + 1
    def setValue(self, arg_name, arg_value):
        if arg_name in self.args:
            self.argv[self.args.index(arg_name)] = arg_value
        else:
            self.args.append(arg_name)
            self.argv.append(arg_value)
            
    def getValue(self, arg_name: str):
        if arg_name in self.args:
            index = self.args.index(arg_name)
            r = self.argv[index]
            return r
        else:
            return None
    def data(self, index:int):
        if index < len(self.argv):
            return self.argv[index]
        else:
            return None
        
    def add_child(self,child):
        assert(isinstance(child,CATEGORY_NODE))
        child.parent = self
        child.level = self.level + 1
        self.children.append(child)
        self.setValue("child number",self["child number"] + 1)
    
    def find_child(self,child_name):
        if child_name is None:
            return False
        for i in range(len(self.children)):
            if child_name == self.children[i]["name"]:
                return i
        return False
    
    def locate_by_names(self,cat_names:list[str]):
        if len(cat_names) == 0:
            return None
        i = self.find_child(cat_names[0])
        if i is not False:
            if len(cat_names) == 1:
                return self.child(i)
            else:
                cat_names_popped = cat_names[1:]
                return self.child(i).locate_by_names(cat_names_popped)
        else:
            return None
    
    def get_exp_rt_range(self):
        t_lo = self["est_rt_lo_m"]
        t_up = self["est_rt_up_m"]
        if t_lo is None and t_up is None and self.parent is not None:
            t_lo = self.parent.get_exp_rt_range()[0]
            t_up = self.parent.get_exp_rt_range()[1]
        if t_lo is not None:
            t_lo = float(t_lo)
        if t_up is not None:
            t_up = float(t_up)
        return (t_lo,t_up)

    def child(self, index:int):
        if index < len(self.children):
            return self.children[index]
        else:
            return None

    def child_num(self):
        return len(self.children)

    def attr_num(self):
        return len(self.argv)
    
    def __getitem__(self,key):
        if type(key) is int and key < len(self.argv):
            return self.argv[key]
        if type(key) is str:
            return self.getValue(key)
        else:
            return None
    def __setitem__(self, key, value):
        if type(key) is int and key < len(self.argv):
            self.argv[key] = value
        elif type(key) is str:
            self.setValue(key,value)

    @staticmethod
    def from_json(json_dict:dict):
        cat = CATEGORY_NODE(json_dict['name'])
        cat['est_rt_lo_m'] = json_dict['est_rt_lo_m']
        cat['est_rt_up_m'] = json_dict['est_rt_up_m']
        if "CATEGORIES" in json_dict.keys():
            categories_json = list(json_dict['CATEGORIES'])
            for category_jason in categories_json:
                sub_cat = CATEGORY_NODE.from_json(category_jason)
                sub_cat.level = 1
                cat.add_child(sub_cat)
        if "MAIN_CLASSES" in json_dict.keys():
            main_classes_json = list(json_dict['MAIN_CLASSES'])
            for main_cls_jason in main_classes_json:
                sub_cat = CATEGORY_NODE.from_json(main_cls_jason)
                sub_cat.level = 2
                cat.add_child(sub_cat)
        if "SUB_CLASSES" in json_dict.keys():
            sub_classes_json = list(json_dict['SUB_CLASSES'])
            for sub_cls_jason in sub_classes_json:
                sub_cat  = CATEGORY_NODE.from_json(sub_cls_jason)
                sub_cat.level = 3
                cat.add_child(sub_cat)
        return cat

    def to_json(self):
        json_dict=dict()
        json_dict["name"]=self.getValue('name')
        json_dict["est_rt_lo_m"]=self['est_rt_lo_m']
        json_dict["est_rt_up_m"]=self['est_rt_up_m']
        children_str = []
        for child in self.children:
            children_str.append(json.loads(child.to_json()))
        if self.level == 0 and len(children_str) > 0:
            json_dict["CATEGORIES"]=children_str
        if self.level == 1 and len(children_str) > 0:
            json_dict["MAIN_CLASSES"]=children_str
        if self.level == 2 and len(children_str) > 0:
            json_dict["SUB_CLASSES"]=children_str
        return json.dumps(json_dict, skipkeys=True, indent=4)
                




 