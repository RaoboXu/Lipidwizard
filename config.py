import json
import os.path
class Config():
    def __init__(self, config_path:str):
        self.config_path = config_path
        if config_path == '':
            self.DatabaseXlsxFile = ''
            self.DatabaseCSVFile = ''
            self.DatabaseFile = ''
            self.DatabaseUrl = ''
            self.ECN_DATA_DIRECTORY=''
            self.ERTFile = ''
            self.E_MASS = 0.0
            self.ECN_K_RANGE=tuple()
            self.C_ISO_DIFF = 0.0
            self.DatabaseColumnTitles = list()
            self.IONS = list()
            self.ElementTable = dict[str, float]()
            self.MatchedResultsTitles = list()
            self.AlignedResultsTitles = list()
            self.TreeNodeTitles = list()
            self.AlignTitles = list()
            self.PeaksOriginalTitlesSingle= list()
            self.PeaksOriginalTitlesPairwise = list()
            self.PeaksFinalColumnsTitles = list()
            self.ION_ELEMENTS = dict()
            self.ION_CHARGE = dict()
            self.ISOTOPIC_NUM = 0
            self.CATEGORIES=[]
            self.MAIN_CLASSES=[]
            self.SUB_CLASSES=[]
            self.XCMS_PROPERTIES = []
        elif os.path.exists(config_path):
            self.LoadConfig()

    def UpdateConfig(self):
        jstr = json.dumps(self.__dict__, skipkeys=True, indent=4)
        f = open(self.config_path, 'w')
        f.write(jstr)
        f.close()

    def LoadConfig(self):
        f = open(self.config_path, 'r')
        data = dict(json.load(f))
        f.close()
        self.DatabaseXlsxFile = str(data['DatabaseXlsxFile'])
        self.DatabaseCSVFile = str(data['DatabaseCSVFile'])
        self.DatabaseFile = str(data['DatabaseFile'])
        self.DatabaseUrl = str(data['DatabaseUrl'])
        self.ECN_DATA_DIRECTORY=str(data['ECN_DATA_DIRECTORY'])
        self.ERTFile=str(data['ERTFile'])
        self.E_MASS = float(data['E_MASS'])
        self.ECN_K_RANGE = tuple(data['ECN_K_RANGE'])
        self.DatabaseColumnTitles = list(data['DatabaseColumnTitles'])
        self.XCMS_PROPERTIES = list(data['XCMS_PROPERTIES'])
        self.IONS = list(data['IONS'])
        self.ElementTable = dict[str, float](data['ElementTable'])
        self.MatchedResultsTitles = list(data['MatchedResultsTitles'])
        self.AlignedResultsTitles = list(data['AlignedResultsTitles'])
        self.TreeNodeTitles = list(data['TreeNodeTitles'])
        self.AlignTitles = list(data['AlignTitles'])
        self.PeaksFinalColumnsTitles = list(data['PeaksFinalColumnsTitles'])
        self.ION_ELEMENTS = dict[str, dict[str, int]](data['ION_ELEMENTS'])
        self.ION_CHARGE = dict[str, dict[str, int]](data['ION_CHARGE'])
        self.C_ISO_DIFF = float(data['C_ISO_DIFF'])
        self.ISOTOPIC_NUM = int(data['ISOTOPIC_NUM'])
        self.CATEGORIES = list(data['CATEGORIES'])
        self.MAIN_CLASSES = list(data['MAIN_CLASSES'])
        self.SUB_CLASSES = list(data['SUB_CLASSES'])
        


config: Config = Config(config_path='./config.json')

if __name__ == '__main__':
    config.UpdateConfig()
    pass
    # cat_root = config.CATEGORY_ROOT
    # r = cat_root.locate_by_names(["Fatty Acyls [FA]","Fatty Acids and Conjugates [FA01]","Unsaturated fatty acids [FA0103]"])
    # if r:
    #     print(r.get_exp_rt_range())
    # else:
    #     print("Not found")
    # config.UpdateCategories("./updated_categories.json")
    # i = 4
    # if type(i) is int:
    #     print(str(i)+" is an integer")
    # print(config)
