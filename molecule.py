from functools import total_ordering
from util import Normalize
from config import config
import re
import copy


def rel_delta(a: float, theory: float):
    return (a-theory) / theory


def CalMass(elements: dict[str, float], charge=0):
    mass = 0.000000
    if len(elements) == 0:
        return mass
    for e in elements.keys():
        mass += float(config.ElementTable[e]) * elements[e]
    mass -= charge*config.E_MASS
    return mass


def CalMZ(elements: dict[str, float], charge=0):
    mass = CalMass(elements, charge)
    if charge == 0:
        return mass
    else:
        return mass/abs(charge)


def FormulaStr2Dict(strFormula: str) -> dict[str, int]:
    strFormula = re.sub(r'\[\d+\]', '', strFormula)
    assert strFormula.isalnum()
    dicFormula: dict[str, int] = dict()
    for i in range(len(strFormula)):
        ch_i = strFormula[i]
        if ch_i.isalpha() and ch_i.isupper():
            if i == len(strFormula)-1:
                dicFormula[ch_i] = 1
            else:
                ch_n = strFormula[i+1]
                name = ch_i
                num = 1
                str_num = ''
                if ch_n.isalpha() and ch_n.islower():
                    name += ch_n
                    i = i+1
                i = i+1
                while i < len(strFormula) and strFormula[i].isnumeric():
                    str_num += strFormula[i]
                    i += 1
                if str_num.isnumeric():
                    num = int(str_num)
                if name in dicFormula.keys():
                    dicFormula[name] += num
                else:
                    dicFormula[name] = num
    return dicFormula


def StatElements(formula: str):
    elements: dict[str, int] = dict()
    if formula.isalnum():
        for i in range(len(formula)):
            ch_i = formula[i]
            if ch_i.isalpha() and ch_i.isupper():
                if i == len(formula)-1:
                    if ch_i in elements.values:
                        elements[ch_i] += 1
                    else:
                        elements[ch_i] = 1
                else:
                    ch_n = formula[i+1]
                    name = ch_i
                    num = 1
                    str_num = ''
                    if ch_n.isalpha() and ch_n.islower():
                        name += ch_n
                        i = i+1
                    i = i+1
                    while i < len(formula) and formula[i].isnumeric():
                        str_num += formula[i]
                        i += 1
                    if str_num.isnumeric():
                        num = int(str_num)
                    if ch_i in elements.values:
                        elements[ch_i] += num
                    else:
                        elements[ch_i] = num
    return elements


def MergeElements(m1: dict[str, int], m2: dict[str, int]) -> dict[str, int]:
    r = copy.copy(m1)
    keys1 = r.keys()
    keys2 = m2.keys()
    for key in keys2:
        if key in keys1:
            r[key] += m2[key]
        else:
            r[key] = m2[key]
        if r[key] < 0:
            return dict()
    return r


class Molecule:
    def __init__(self):
        self.args = list(config.DatabaseColumnTitles)
        self.argv = []
        for i in range(len(self.args)):
            self.argv.append(None)

    def __len__(self):
        return len(self.args)

    def __getitem__(self, index):
        return self.argv[index]

    def getValue(self, arg_name: str):
        if arg_name in self.args:
            index = self.args.index(arg_name)
            r = self.argv[index]
            return r
        else:
            return None

    def setValue(self, arg_name: str, arg_value):
        if arg_name in self.args:
            self.argv[self.args.index(arg_name)] = arg_value
        else:
            self.args.append(arg_name)
            self.argv.append(arg_value)

    def getIonIndexRange(self):
        start_p = 0
        end_p = -1
        for i in range(len(self.args)):
            if self.args[i] in config.IONS:
                start_p = i
                break
        end_p = start_p + len(config.IONS)
        return (start_p, end_p)

    def statElements(self):
        elements = FormulaStr2Dict(self.getValue('FORMULA'))
        self.setValue('ELEMENTS', str(elements))

    def getElements(self, withIon=False, ion='') -> dict[str, int]:
        elements: dict[str, int] = eval(self.getValue('ELEMENTS'))
        if withIon and ion in config.IONS:
            return MergeElements(elements, config.ION_ELEMENTS[ion])
        else:
            return elements

    def is_legal(self) -> bool:
        el = self.getElements()
        for key in el.keys():
            if key not in config.ElementTable.keys():
                return False
        return True

    def calMZ(self):
        for ion in config.IONS:
            mass_n = CalMZ(self.getElements(
                withIon=True, ion=ion), config.ION_CHARGE[ion])
            self.setValue(ion, '{:.6f}'.format(mass_n))


class Peak:
    def __init__(self, mz=0.0, it=0.0, rt=0.0, ri=0.0, mzmin=0.0, mzmax=0.0, rtmin=0.0, rtmax=0.0, params=list(), data=list()) -> None:
        if len(params) == 8:
            self.mz = float(params[0])
            self.intensity = float(params[1])
            self.retention_time = float(params[2])
            self.rel_intensity = float(params[3])
            self.mzmin = float(params[4])
            self.mzmax = float(params[5])
            self.rtmin = float(params[6])
            self.rtmax = float(params[7])
        elif len(params) == 2:
            self.mz = float(params[0])
            self.intensity = float(params[1])
            self.retention_time = float(rt)
            self.rel_intensity = float(ri)
            self.mzmin = float(mzmin)
            self.mzmax = float(mzmax)
            self.rtmin = float(rtmin)
            self.rtmax = float(rtmax)
        else:
            self.mz = float(mz)
            self.intensity = float(it)
            self.retention_time = float(rt)
            self.rel_intensity = float(ri)
            self.mzmin = float(mzmin)
            self.mzmax = float(mzmax)
            self.rtmin = float(rtmin)
            self.rtmax = float(rtmax)
        self.data = data

    def __add__(self, other):
        result = Peak()
        result.mz = self.mz
        result.retention_time = self.retention_time
        result.rel_intensity = 0
        result.intensity = self.intensity + other.intensity
        return result

    def __truediv__(self, divider: float):
        result = Peak()
        result.mz = self.mz
        result.retention_time = self.retention_time
        result.rel_intensity = 0
        result.intensity = self.intensity/divider
        return result

    def __str__(self) -> str:
        return str((self.mz, self.intensity, self.retention_time, self.rel_intensity))

    def to_short_str(self) -> str:
        return str(('{:.6f}'.format(self.mz), '{:.6f}'.format(self.rel_intensity)))


class IsotopicVariants:
    def __init__(self, lm_id='', ion='', m0: float = 0.0, mz_list=list(), abundance_list=list(), relIntensityList=list(), mol:Molecule=None) -> None:
        self.LM_ID = lm_id
        self.ION = ion
        self.M0 = m0
        self.abundanceList = list()
        self.relIntensityList = list()
        self.mz_list = mz_list
        self.mol = mol
        if len(mz_list) > 0:
            self.M0 = mz_list[0]
        if len(relIntensityList) > 0:
            self.relIntensityList += relIntensityList
        elif (len(abundance_list) > 0):
            self.abundanceList.append(abundance_list[0])
            for i in range(1, len(mz_list)):
                if mz_list[i] - mz_list[i-1] < 0.5:
                    self.abundanceList[-1] += abundance_list[i]
                elif mz_list[i] - mz_list[i-1] > 1.5:
                    self.abundanceList.append(0.0)
                    self.abundanceList.append(abundance_list[i])
                else:
                    self.abundanceList.append(abundance_list[i])
            self.relIntensityList: list(float) = Normalize(self.abundanceList)
        # self.peakNum = peak_num
        self.peakNum = len(self.relIntensityList)

    def __str__(self):
        return str(self.LM_ID) + self.ION

    def GetFirstPeak(self, intensity_coefficient=1) -> Peak:
        return Peak(self.M0, it=self.relIntensityList[0]*intensity_coefficient, ri=self.relIntensityList[0], rt=0.0)

    def GetPeak(self, index, intensity_coefficient=1) -> Peak:
        return Peak(self.mz_list[index], it=self.relIntensityList[index]*intensity_coefficient, ri=self.relIntensityList[index], rt=0.0)


@total_ordering
class MatchResult:
    def __init__(self, ion=None, peak: Peak = None, mol: Molecule = None) -> None:
        self.peak = peak
        self.mol = mol
        self.mz_theory = ''
        self.mz_exp = ''
        self.del_ppm = ''
        self.retention_time = ''
        self.intensity = ''
        self.lm_id = ''
        self.ion = ''
        self.name = ''
        self.category = ''
        self.main_class = ''
        self.sub_class = ''
        self.formula = ''
        self.abbreviation = ''
        if peak is not None:
            self.mz_theory = float(mol.getValue(ion))
            self.mz_exp = peak.mz
            # self.rel_delta = '{:.2f}'.format(
            #     rel_delta(float(self.mz_exp), float(self.mz_theory)*1e6))
            self.del_ppm = rel_delta(
                float(self.mz_exp), float(self.mz_theory))*1e6
            self.retention_time = peak.retention_time
            self.intensity = peak.intensity
        if mol is not None:
            self.lm_id = str(mol.getValue('LM_ID'))
            self.name = str(mol.getValue('NAME'))
            self.category = str(mol.getValue('CATEGORY'))
            self.main_class = str(mol.getValue('MAIN_CLASS'))
            self.sub_class = str(mol.getValue('SUB_CLASS'))
            self.formula = str(mol.getValue('FORMULA'))
            self.abbreviation = str(mol.getValue('ABBREVIATION'))
        if ion is not None:
            self.ion = ion

    def __str__(self):
        return str((self.mz_theory, self.mz_exp, self.del_ppm, self.retention_time, self.intensity, self.ion, self.lm_id, self.name, self.category, self.main_class, self.sub_class, self.formula, self.abbreviation))


    def __eq__(self, other):
        if isinstance(other, MatchResult):
            if self.mz_exp == other.mz_exp and self.retention_time == other.retention_time and self.ion == other.ion and self.lm_id == other.lm_id:
                return True
        return False
        
    def __gt__(self, other):
        assert isinstance(other, MatchResult)
        # comparison order: ion, category, main_class, sub_class, lm_id, mz_exp, retention_time, 
        if self.ion > other.ion:
            return True
        elif self.ion < other.ion:
            return False
        if self.category > other.category:
            return True
        elif self.category < other.category:
            return False
        if self.main_class > other.main_class:
            return True
        elif self.main_class < other.main_class:
            return False
        if self.sub_class > other.sub_class:
            return True
        elif self.sub_class < other.sub_class:
            return False
        if self.lm_id > other.lm_id:
            return True
        elif self.lm_id < other.lm_id:
            return False
        if self.mz_exp > other.mz_exp:
            return True
        elif self.mz_exp < other.mz_exp:
            return False
        if self.retention_time > other.retention_time:
            return True
        elif self.retention_time < other.retention_time:
            return False
        return False
           
    def similar(self,other)->bool:
        if self.mz_exp == other.mz_exp and self.retention_time == other.retention_time and self.ion == other.ion and self.lm_id != other.lm_id:
            return True
        else:
            return False

    def to_list(self):
        return [float(self.mz_theory), self.mz_exp, self.del_ppm, self.retention_time, self.intensity, self.ion, self.lm_id, self.name, self.category, self.main_class, self.sub_class, self.formula, self.abbreviation]

    def from_list(self, data: list):
        if len(data) != 13:
            return 'FAILED'
        self.mz_theory = float(data[0])
        self.mz_exp = float(data[1])
        self.del_ppm = float(data[2])
        self.retention_time = float(data[3])
        self.intensity = float(data[4])
        self.ion = data[5]
        self.lm_id = data[6]
        self.name = data[7]
        self.category = data[8]
        self.main_class = data[9]
        self.sub_class = data[10]
        self.formula = data[11]
        self.abbreviation = data[12]
        return 'SUCCESS'

    def toAlignData(self):
        return ['{}{}'.format(self.lm_id, self.ion), self.name, self.retention_time, '{}_{}_{}'.format(self.category, self.main_class, self.sub_class), float(self.mz_theory), self.intensity, self.abbreviation, '']


if __name__ == '__main__':
    d1 = {'C': 12, 'H': 12, 'O': 12}
    d2 = {'C': 10, 'O': -5, 'P': 1}
    r = MergeElements(d1, d2)
    print(r)
