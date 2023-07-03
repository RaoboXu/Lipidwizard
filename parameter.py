
import json
import util

class Params:
    def __init__(self) -> None:
        self.TimeStamp = ''
        self.mergMzVar=3.0
        self.mergRtVar=0.01
        self.asmtMzVar=5.00
        self.stripRiMinPct=0.0
        self.stripItMin=0.0
        self.asmtRiMinPct=0.0
        self.asmtItMin=0.0
        self.IsoIgnoreMinPct=15.0
        self.ClusterVar=5e-4
        self.TimeWindowMin = 0.01
        self.skipMerge = False
        self.skipIsoDeconvolution = False
        self.Ions=[]
        self.Catagories=[]
        self.MainClasses=[]
        self.alignmentRetentionTimeVar=self.mergRtVar
        self.OutputDirectory=''
        self.ECNFilter = False
        self.ERTFilter = False
        self.ECN_FILT_TYPE = 'CONFIDENCE'
        self.result_merge_level = 3
    
    def Save(self,dir, name):
        path='{}/{}_log.json'.format(dir,name)
        path=util.AddTimeStamp(path,self.TimeStamp)
        f = open(path, 'w')
        json.dump(self.__dict__, f, skipkeys=True, indent=4)
        f.close()
    def Load(self, path):
        f = open(path, 'r')
        self.__dict__ = json.load(f)
        f.close()

params = Params()
