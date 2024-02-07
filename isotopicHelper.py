from util import Normalize
from databaseHelper import readDatabaseFromCSV
from typing import List
import brainpy
from config import config
from molecule import MatchResult, Molecule, Peak, IsotopicVariants
from parameter import params
import csvHelper as csvh
from ert_filter import pass_ert_filter_iso, ert_profile
from ecn_filter import pass_ecn_filter_iso, ecn_profile

import numpy as np
from scipy.optimize import nnls

# isotopic_variants() returns peaks with attributes: mz, intensity, charge


def rel_delta(a: float, theory: float):
    return (a-theory) / theory


def SearchIsotopeByM0(m0: float, target: List[IsotopicVariants], var=1e-6, charges:list[int]=[]) -> List[IsotopicVariants]:
    result: List[IsotopicVariants] = list()
    end = len(target)
    low = 0
    high = end-1
    mid = 0
    while low <= high:
        mid = (high+low) // 2
        mass = float(target[mid].M0)
        delta = var+1
        if mass > 0:
            delta = rel_delta(m0, mass)
        if delta < -var:
            high = mid-1
        elif delta > var:
            low = mid+1
        else:
            if len(charges) == 0:
                result.append(target[mid])
            elif config.ION_CHARGE[target[mid].ION] in charges:
                result.append(target[mid])
            # find all neighbors which meet the condition
            # forward search
            i = mid+1
            while i < end:
                mass = float(target[i].M0)
                delta = var+1
                if mass > 0:
                    delta = rel_delta(m0, mass)
                if abs(delta) < var:
                    if len(charges) == 0:
                        result.append(target[i])
                    elif config.ION_CHARGE[target[i].ION] in charges:
                        result.append(target[i])
                    i += 1
                else:
                    break
            # backward search
            i = mid - 1
            while i >= 0:
                mass = float(target[i].M0)
                delta = var+1
                if mass > 0:
                    delta = rel_delta(m0, mass)
                if abs(delta) < var:
                    if len(charges) == 0:
                        result.append(target[i])
                    elif config.ION_CHARGE[target[i].ION] in charges:
                        result.append(target[i])
                    i -= 1
                else:
                    break
            break
    return result


def AverageIsotopic(isotopeList: List[IsotopicVariants]):
    isoNum = len(isotopeList)
    peakNum = isotopeList[0].peakNum
    ri_list = [0.0] * peakNum
    m0 = 0.0
    ion = isotopeList[0].ION
    for iso in isotopeList:
        m0 += float(iso.M0)
        for i in range(peakNum):
            ri_list[i] += iso.relIntensityList[i]
    ri_list = Normalize(ri_list)
    m0 = m0 / isoNum
    return IsotopicVariants(ion=ion,m0=m0, relIntensityList=ri_list)


def cal_isotopic_var(elements: dict[str, int], npeaks, charge=0) -> IsotopicVariants:
    if elements.__contains__('H'):
        elements['H'] -= charge
    peaks = list(brainpy.isotopic_variants(elements, npeaks, charge))
    real_peak_num = len(peaks)
    if real_peak_num < 2:
        return None
    del_mz = peaks[1].mz - peaks[0].mz
    # extend the peaks list with zero peaks to the length of npeaks
    while len(peaks) < npeaks:
        peaks.append(brainpy.Peak(peaks[-1].mz + del_mz, 0, charge))
    mz_list = list()
    abundance_list = list()
    for p in peaks:
        mz_list.append(p.mz)
        abundance_list.append(p.intensity)
    return IsotopicVariants(mz_list=mz_list, abundance_list=abundance_list)


def SaveAllIsotopicProfiles(isotopic_vars: List[IsotopicVariants], target: str):
    data = list()
    for m in isotopic_vars:
        data_raw = list()
        data_raw.append(m.LM_ID)
        data_raw.append(m.ION)
        data_raw.append(m.M0)
        for i in range(m.peakNum):
            data_raw.append(m.relIntensityList[i])
        data.append(data_raw)
    csvh.SaveDataCSV(target, data)

def CalculateIsotopicProfiles(database: list[Molecule], ions: list[str]) -> List[IsotopicVariants]:
    print("Calculating Isotopic variants ...")
    i = 0.
    n = len(database)
    result: list[IsotopicVariants] = list()
    for mol in database:
        for ion in ions:
            var = cal_isotopic_var(mol.getElements(
                withIon=True, ion=ion), npeaks=config.ISOTOPIC_NUM, charge=0)
            var.LM_ID = mol.getValue('LM_ID')
            var.ION = ion
            var.M0 = float(mol.getValue(ion))
            var.mol = mol
            result.append(var)
        i += 1
        print('\r{:.2f}%'.format((i/n)*100), end=' ')
    print("\nCalculating Isotopic variants SUCCESS! ")
    return result

def CalculateIsotopicProfilesWithCharge2(database: list[Molecule], ions: list[str]) -> List[IsotopicVariants]:
    print("Calculating Isotopic variants ...")
    i = 0.
    n = len(database)
    result: list[IsotopicVariants] = list()
    for mol in database:
        for ion in ions:
            charges = config.ION_CHARGE[ion]
            var = cal_isotopic_var(mol.getElements(
                withIon=True, ion=ion), npeaks=config.ISOTOPIC_NUM*2, charge=charges)
            if var is None:
                continue
            var.LM_ID = mol.getValue('LM_ID')
            var.ION = ion
            var.M0 = float(mol.getValue(ion))
            var.mol = mol
            result.append(var)
        i += 1
        print('\r{:.2f}%'.format((i/n)*100), end=' ')
    print("\nCalculating Isotopic variants SUCCESS! ")
    return result

def RemoveIsotopicFromCluster(cluster: List[Peak], isotopic: IsotopicVariants, index=0, keepingThreshold=0.1) -> Peak:
    k = cluster[index].intensity * isotopic.relIntensityList[0]
    peakNum = len(cluster)
    if k > 0 and index < peakNum:
        endPos = min(peakNum, index + isotopic.peakNum)
        sub_i = 0
        for i in range(index, endPos):
            itOrigin = cluster[i].intensity
            if itOrigin > 0:
                subIntensity = k*isotopic.relIntensityList[sub_i]
                cluster[i].intensity -= subIntensity
                if cluster[i].intensity / float(itOrigin) < keepingThreshold:
                    cluster[i].intensity = 0.0
            sub_i += 1
        return Peak(cluster[index].mz, k, cluster[index].retention_time, cluster[index].rel_intensity, cluster[index].mzmin, cluster[index].mzmax, cluster[index].rtmin, cluster[index].rtmax)


def SearchByID(id: str, database: list[Molecule]):
    end = len(database)
    low = 0
    high = end-1
    mid = 0
    while low <= high:
        mid = (high+low) // 2
        _id = database[mid].getValue('LM_ID')
        if id < _id:
            high = mid-1
        elif id > _id:
            low = mid+1
        else:
            return database[mid]
    return None

def classify_iso_by_charge(iso_list: List[IsotopicVariants]) -> List[list[IsotopicVariants]]:
    result: List[list[IsotopicVariants]] = []
    for iso in iso_list:
        if iso.ION not in config.ION_CHARGE.keys():
            continue
        charge = abs(config.ION_CHARGE[iso.ION])
        while len(result) < charge+1:
            result.append([])
        result[charge].append(iso)
    return result

def unify_iso_profile(iso:IsotopicVariants) -> IsotopicVariants:
    # insert zero between two peaks if charges is 0 or 1 and make the profile length equal to ISOTOPIC_NUM*2
    # get the charge of the ion
    charge = abs(config.ION_CHARGE[iso.ION])
    peak_num = config.ISOTOPIC_NUM*2
    abundance_list = [0.0]*peak_num
    rel_intensity_list = [0.0]*peak_num
    if charge == 0 or charge == 1:
        for i in range(config.ISOTOPIC_NUM):
            abundance_list[i*2] = iso.abundanceList[i]
            rel_intensity_list[i*2] = iso.relIntensityList[i]
    if charge == 2:
        for i in range(iso.peakNum):
            abundance_list[i] = iso.abundanceList[i]
            rel_intensity_list[i] = iso.relIntensityList[i]
    return IsotopicVariants(lm_id =iso.LM_ID, ion=iso.ION,m0=iso.M0, mz_list= iso.mz_list,abundance_list=abundance_list,relIntensityList=rel_intensity_list,mol=iso.mol)

def deconv(cluster, profiles_a, profiles_b):
    N = len(cluster)
    M = len(profiles_a[0])

    # Construct the coefficient matrix
    coef_matrix_A = np.zeros((N, N))
    coef_matrix_B = np.zeros((N, N))
    for i in range(N):
        for j in range(i, min(M, N-i)):
            coef_matrix_A[i, j] = profiles_a[i, j-i]
            coef_matrix_B[i, j] = profiles_b[i, j-i]
    coef_matrix = np.concatenate((coef_matrix_A.T, coef_matrix_B.T), axis=1)

    # Vectorize A
    A = np.array(cluster)
    # A = A.T
    x_y, err = nnls(coef_matrix,A)
    # Split the solution into x and y
    x = x_y[:N]
    y = x_y[N:]
    
    return x, y

def ClusterMatchWithCharge2(cluster: List[Peak], profiles: List[IsotopicVariants], database: list[Molecule], var=1e-6, min_int_abs=0.0, min_it_rel=0.0) -> List[MatchResult]:
    result: list[MatchResult] = []
    A = [peak.intensity for peak in cluster]
    cluster_size = len(cluster)

    profile_resolution = config.ISOTOPIC_NUM*2

    profiles_charge01 = np.zeros((cluster_size, profile_resolution))
    profiles_charge2 = np.zeros((cluster_size, profile_resolution))

    candidates_01: list[list[IsotopicVariants]] = [[]]*cluster_size
    candidates_2: list[list[IsotopicVariants]] = [[]]*cluster_size

    for i in range(cluster_size):
        peak = cluster[i]
        if peak.intensity <= 0:
            continue
        iso_charge01: List[IsotopicVariants] = SearchIsotopeByM0(
                peak.mz, profiles, var=var, charges=[-1,0,1])
        iso_charge2: List[IsotopicVariants] = SearchIsotopeByM0(
                peak.mz, profiles, var=var, charges=[-2,2])
        for iso in iso_charge01:
            if params.ERTFilter and pass_ert_filter_iso(iso,peak.retention_time,ert_profile) is False:
                continue
            if params.ECNFilter and pass_ecn_filter_iso(iso,peak.retention_time,ecn_profile,params.ECN_FILT_TYPE) is False:
                continue
            candidates_01[i].append(unify_iso_profile(iso))
        for iso in iso_charge2:
            if params.ERTFilter and pass_ert_filter_iso(iso,peak.retention_time,ert_profile) is False:
                continue
            if params.ECNFilter and pass_ecn_filter_iso(iso,peak.retention_time,ecn_profile,params.ECN_FILT_TYPE) is False:
                continue
            candidates_2[i].append(unify_iso_profile(iso))
    
    for i in range(cluster_size):
        if len(candidates_01[i]) > 0:
            avg = AverageIsotopic(candidates_01[i])
            for j in range(min(len(avg.relIntensityList), profile_resolution)):
                profiles_charge01[i,j] = avg.relIntensityList[j]
        if len(candidates_2[i]) > 0:
            avg = AverageIsotopic(candidates_2[i])
            for j in range(min(len(avg.relIntensityList), profile_resolution)):
                profiles_charge2[i,j] = avg.relIntensityList[j]
    charge01_intensities, charge2_intensities = deconv(A, profiles_charge01, profiles_charge2)

    for i in range(cluster_size):
        if charge01_intensities[i] > min_int_abs and charge01_intensities[i]  / np.max(charge01_intensities) > min_it_rel:
            peak = cluster[i]
            peak.intensity = charge01_intensities[i]
            for iso in candidates_01[i]:
                mol: Molecule = SearchByID(
                    iso.LM_ID, database)
                r = MatchResult(iso.ION, peak, mol)
                result.append(r)
        if charge2_intensities[i] > min_int_abs and charge2_intensities[i] / np.max(charge2_intensities) > min_it_rel:
            peak = cluster[i]
            peak.intensity = charge2_intensities[i]
            for iso in candidates_2[i]:
                mol: Molecule = SearchByID(
                    iso.LM_ID, database)
                r = MatchResult(iso.ION, peak, mol)
                result.append(r)
    return result


def ClustersMatch(clusters: List[List[Peak]], isotopic_profiles: list[IsotopicVariants], database: list[Molecule]):
    print("Start matching clusters")
    print("Size of database:\t{dbsize}\nSize of cluster:\t{clustersize}".format(
        dbsize=len(database), clustersize=len(clusters)))
    db = sorted(database, key=lambda item: item.getValue('LM_ID'))
    res = []
    i = 0
    matched_num = 0
    while i < len(clusters):
        cluster = clusters[i]
        # r = ClusterMatch(
        #     cluster, isotopic_profiles, db, params.asmtMzVar * 1e-6, params.stripItMin, params.stripRiMinPct/100.0)
        r = ClusterMatchWithCharge2(
            cluster, isotopic_profiles, db, params.asmtMzVar * 1e-6, params.stripItMin, params.stripRiMinPct/100.0)
        if len(r) > 0:
            res += r
            matched_num += len(r)
            clusters.pop(i)
            i -= 1
        i += 1
    print("Clusters matched num:\t{num}".format(num=matched_num))
    print("Clusters matching finished!\n")
    return res




if __name__ == '__main__':
    cluster = [10000, 20000, 12000, 2000, 25000, 0, 42000, 0, 17000, 0, 5000, 0, 1500, 0]
    # cluster = [10000, 20000, 12000, 2000, 25000, 0, 42000, 0, 17000]
    cluster_size = len(cluster)

    coeffs = [10000,20000, 20000, 30000]
    print("Expected coefficients:")
    print(coeffs)
    print()

    profile_a0 = [1.0, 0, 0.6, 0, 0.4 , 0, 0.2 , 0]
    profile_a2 = [1.0, 0, 0.5, 0, 0.25, 0, 0.1 , 0]
    profile_a3 = [1.0, 0, 0.4, 0, 0.1 , 0, 0.05, 0]

    profile_b1 = [1.0, 0.3, 0.1, 0.05, 0 , 0, 0, 0]

    profile_resolution = len(profile_a0)

    profiles_charge01 = np.zeros((cluster_size, profile_resolution))
    profiles_charge2 = np.zeros((cluster_size, profile_resolution))

    profiles_charge01[0] = profile_a0
    profiles_charge01[4] = profile_a2
    profiles_charge01[6] = profile_a3

    profiles_charge2[1] = profile_b1



    # place_holder = [0]*8
    # profiles_charge01 = [profile1, place_holder, place_holder, place_holder, profile3, place_holder, profile4, place_holder, place_holder, place_holder, place_holder, place_holder,place_holder, place_holder]
    # profiles_charge01 = np.array(profiles_charge01)

    # profiles_charge2 = [place_holder, profile2, place_holder, place_holder, place_holder, place_holder, place_holder, place_holder,place_holder, place_holder, place_holder, place_holder,place_holder, place_holder]
    # profiles_charge2 = np.array(profiles_charge2)

    x,y=deconv(cluster, profiles_charge01, profiles_charge2)
    print("x:")
    print(x)
    print()
    print("y:")
    print(y)
    print()
    
