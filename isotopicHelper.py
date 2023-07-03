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


def SearchIsotopeByM0(m0: float, target: List[IsotopicVariants], var=1e-6) -> List[IsotopicVariants]:
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
                    result.append(target[i])
                    i -= 1
                else:
                    break
            break
    return result


def AverageIsotopic(isotopeList: List[IsotopicVariants]):
    isoNum = len(isotopeList)
    ri_list = [0.0] * config.ISOTOPIC_NUM
    m0 = 0.0
    for iso in isotopeList:
        m0 += float(iso.M0)
        for i in range(config.ISOTOPIC_NUM):
            ri_list[i] += iso.relIntensityList[i]
    ri_list = Normalize(ri_list)
    m0 = m0 / isoNum
    return IsotopicVariants(m0=m0, relIntensityList=ri_list)


def isotopic_var(elements: dict[str, int], npeaks, charge=0) -> IsotopicVariants:
    peaks = brainpy.isotopic_variants(elements, npeaks, charge)
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


def GetIsotopicProfiles(molecules: List[Molecule], ions: List[str]) -> List[IsotopicVariants]:
    result = list()
    for mol in molecules:
        for ion in ions:
            # iso_var = isotopic_var(mol.getElements(
            #     withIon=True, ion=ion), npeaks=5, charge=config.ION_CHARGE[ion])
            iso_var = isotopic_var(mol.getElements(
                withIon=True, ion=ion), npeaks=config.ISOTOPIC_NUM, charge=0)
            iso_var.LM_ID = mol.getValue('LM_ID')
            iso_var.ION = ion
            iso_var.M0 = mol.getValue(ion)
            iso_var.mol = mol
            result.append(iso_var)
    result.sort(key=lambda x: float(x.M0))
    return result


def CalculateIsotopicProfiles(database: list[Molecule], ions: list[str]) -> List[IsotopicVariants]:
    print("Calculating Isotopic variants ...")
    i = 0.
    n = len(database)
    result: list[IsotopicVariants] = list()
    for mol in database:
        for ion in ions:
            var = isotopic_var(mol.getElements(
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

def ClusterMatch(cluster: List[Peak], profiles: List[IsotopicVariants], database: list[Molecule], var=1e-6, min_int_abs=0.0, min_it_rel=0.0) -> List[MatchResult]:
    result: list[MatchResult] = []
    cluster_size = len(cluster)
    mat_size = max(cluster_size, config.ISOTOPIC_NUM)
    M = np.zeros((mat_size, mat_size))
    A = [peak.intensity for peak in cluster]
    if len(A) < mat_size:
        A.extend([0.0]*(mat_size-len(A)))
    A = np.array(A)

    search_results = []
    candidate: list[list[IsotopicVariants]] = []
    for i in range(mat_size):
        if i >= cluster_size:
            search_results.append([0.0]*mat_size)
            candidate.append([])
            continue
        peak = cluster[i]
        iso_all: List[IsotopicVariants] = SearchIsotopeByM0(
                peak.mz, profiles, var=var)
        profile = []
        candidate_item =[]
        for iso in iso_all:
            if params.ERTFilter and pass_ert_filter_iso(iso,peak.retention_time,ert_profile) is False:
                continue
            if params.ECNFilter and pass_ecn_filter_iso(iso,peak.retention_time,ecn_profile,params.ECN_FILT_TYPE) is False:
                continue
            candidate_item.append(iso)
        if len(candidate_item) > 0:
            isoAvrg = AverageIsotopic(candidate_item)
            profile.extend(isoAvrg.relIntensityList)
            if len(profile) < mat_size:
                profile.extend([0.0]*(mat_size-len(profile)))
        else:
            profile.extend([0.0]*mat_size)
        candidate.append(candidate_item)
        search_results.append(profile)

    for i in range(mat_size):
        for j in range(cluster_size):
            M[j,i] = search_results[j][j-i]

    # minimum mse estimation that makes M*X close to A
    # X = np.linalg.lstsq(M_T, A, rcond=None)[0]
    X = nnls(M, A)[0]

    for i in range(cluster_size):
        iso_all = candidate[i]
        if len(iso_all) >0 and X[i] > min_int_abs and X[i] / np.max(X) > min_it_rel:
            peak = cluster[i]
            peak.intensity = X[i]
            for iso in iso_all:
                mol: Molecule = SearchByID(
                    iso.LM_ID, database)
                r = MatchResult(iso.ION, peak, mol)
                result.append(r)

    # calculate the mse of X*M and A
    # mse = np.sum((np.dot(X,M) - A)**2) / row_num
    # print("MSE: ", mse)

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
        r = ClusterMatch(
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

    profile_resolution = 4
    cluster_size = 5

    mat_size = max(cluster_size,cluster_size)

    coeffs = [10000, 0, 20000, 30000]
    print("Expected coefficients:")
    print(coeffs)
    print()

    profile1 = [1.0, 0.6, 0.4, 0.2]
    profile3 = [1.0, 0.5, 0.25, 0.1]
    profile4 = [1.0, 0.4, 0.1, 0.05]

    profiles = []
    for i in range(mat_size):
        if i == 0:
            if len(profile1) < mat_size:
                profile1.extend([0]*(mat_size-len(profile1)))
            profiles.append(profile1)
            continue
        if i == 2:
            if len(profile3) < mat_size:
                profile3.extend([0]*(mat_size-len(profile3)))
            profiles.append(profile3)
            continue
        if i == 3:
            if len(profile4) < mat_size:
                profile4.extend([0]*(mat_size-len(profile4)))
            profiles.append(profile4)
            continue
        profiles.append([0]*mat_size)

    # cluster = [10000, 6000, 24000, 42000, 17000, 5000, 1500]
    # cluster = [10000, 6000, 24000, 42000, 17000]
    cluster = [10000, 6000, 24000, 42000, 12000]
    if len(cluster) < mat_size:
        cluster.extend([0]*(mat_size-len(cluster)))

    M = np.zeros((mat_size, mat_size))
    for i in range(mat_size):
        if i == 1:
            continue
        for j in range(i, cluster_size):
            M[j, i] = profiles[i][j-i]

    print("M:")
    print(M)
    print()

    A = cluster

    print("A:")
    print(A)
    print()

    X, residuals = nnls(M, np.array(A))
    mse = residuals
    print("Predict coefficients:")
    print(X)
    print()

    print("MSE:")
    print(mse)
    print()

    print("Real cluster:")
    print(cluster)
    print()

    Y = M@X
    print("Predict cluster:")
    print(Y)
    print()
