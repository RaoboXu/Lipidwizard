from util import Normalize
import os.path
from molecule import Peak
from typing import List
from config import config
import math
from parameter import params
import csvHelper as csvh
import xlHelper as xlh

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def SecToMin(sec: int):
    m = '{:.3f}'.format(float(sec) / 60)
    return float(m)


def NormalizeIntensity(peaks: List[Peak]):
    if len(peaks) == 0:
        return
    it_max = max(peaks, key=lambda peak: peak.intensity)
    for i in range(len(peaks)):
        if it_max.intensity == 0:
            peaks[i].rel_intensity = 0
        else:
            peaks[i].rel_intensity = DecimalToPercent(
                peaks[i].intensity / it_max.intensity)


def DecimalToPercent(value: float):
    return float('{:.6f}'.format(value*100))


def ReadPeaksCSV(file: str) -> list[Peak]:
    print("Reading Peak List ...")
    result: list[Peak] = list()
    data =[]
    if csvh.ReadDataCSV(file,data) == 'SUCCESS':
        data.pop(0)
        for row in data:
            result.append(Peak(row[0], row[1], row[2],
                               row[3], row[4], row[5], row[6], row[7]))
        print("Reading Peak List SUCCESS!")
        NormalizeIntensity(result)
    return result


def SavePeaksCSV(data: List[Peak],  target_path: str, newbook=True, sheet=''):
    titles = config.PeaksFinalColumnsTitles
    _data = []
    for peak in data:
        _data.append([peak.mz, peak.intensity,
                      peak.retention_time, peak.rel_intensity, peak.mzmin, peak.mzmax, peak.rtmin, peak.rtmax])
    csvh.SaveDataCSV(target_path, _data, titles)


def SaveClustersCSV(clusters: List[List[Peak]], target_path: str):
    titles = ['number'] + config.PeaksFinalColumnsTitles
    _data = []
    i = 0
    for peaks in clusters:
        NormalizeIntensity(peaks)
        for peak in peaks:
            _data.append([i, peak.mz, peak.intensity,
                          peak.retention_time, peak.rel_intensity]+peak.data)
        i += 1
    csvh.SaveDataCSV(target_path,_data,titles)


def SplitTable(source: str, targetFolder='./'):
    if os.path.exists(source):
        head = []
        data = []
        if xlh.readXlsx(source,data) != 'SUCCESS':
            print('file: '+str(source)+'not exist')
            return
        head = data.pop(0)
        print('row amount:\t'+str(len(data)))
        property_amount = len(config.XCMS_PROPERTIES)
        sample_amount = len(head)-property_amount
        data_row_num = len(data)
        print('sample amount:\t'+str(sample_amount))

        intensity_data = []  # Intensity
        intensity_norm = []
        intensity_percent = []
        mz_data = []  # m/z
        rt_data = []  # Retention Time
        mzmin_data = []  # m/z min
        rtmin_data = []  # Retention Time
        mzmax_data = []  # m/z
        rtmax_data = []  # Retention Time

        for i in range(sample_amount):
            intensity_data.append([])

        index_mz = head.index('mzmed')
        index_rt = head.index('rtmed')
        index_mzmin = head.index('mzmin')
        index_rtmin = head.index('rtmin')
        index_mzmax = head.index('mzmax')
        index_rtmax = head.index('rtmax')

        for row in data:
            mz_data.append(row[index_mz])
            rt_data.append(row[index_rt])
            mzmin_data.append(row[index_mzmin])
            rtmin_data.append(row[index_rtmin])
            mzmax_data.append(row[index_mzmax])
            rtmax_data.append(row[index_rtmax])
            for index_sample in range(sample_amount):
                intensity_data[index_sample].append(
                    safe_cast(row[property_amount+index_sample], float, 0.0))

        # Normalize intensity
        print('Normalize intensity data')
        for s in range(sample_amount):
            it = Normalize(intensity_data[s])
            intensity_norm.append(it)

        # Normalized rt decimal to percent
        print('Convert decimal intensity to percentage')
        for row in range(sample_amount):
            row_data = []
            for v in intensity_norm[row]:
                row_data.append(DecimalToPercent(v))
            intensity_percent.append(row_data)
        # Convert rt(sec) to rt(min)

        # print('Convert retention time form sec to min')
        # for i in range(data_row_num):
        #     rt_data[i] = SecToMin(int(rt_data[i]))

        # Write Data
        for i_s in range(sample_amount):
            print('start processing '+str(head[property_amount+i_s]))
            # Write title
            data = []
            for i in range(data_row_num):
                if intensity_data[i_s][i] == 0:
                    continue
                data_row = []
                data_row.append(mz_data[i])
                data_row.append(intensity_data[i_s][i])
                data_row.append(rt_data[i])
                data_row.append(intensity_percent[i_s][i])
                data_row.append(mzmin_data[i])
                data_row.append(mzmax_data[i])
                data_row.append(rtmin_data[i])
                data_row.append(rtmax_data[i])
                data.append(data_row)
            csvh.SaveDataCSV(targetFolder+'/'+head[property_amount+i_s] +
                         '_peak_list.csv', data, config.PeaksFinalColumnsTitles)
            print(str(head[property_amount+i_s])+'_peak_list.csv done!')
    else:
        print('file: '+str(source)+'not exist')


def mergePeak(peak1: Peak, peak2: Peak) -> Peak:
    it = peak1.intensity + peak2.intensity
    ri = peak1.rel_intensity + peak2.rel_intensity
    mz = (peak1.mz * peak1.intensity + peak2.mz * peak2.intensity) / it
    mzmin = (peak1.mzmin * peak1.intensity +
             peak2.mzmin * peak2.intensity) / it
    mzmax = (peak1.mzmax * peak1.intensity +
             peak2.mzmax * peak2.intensity) / it
    rt = (peak1.retention_time * peak1.intensity +
          peak2.retention_time * peak2.intensity) / it
    rtmin = (peak1.rtmin * peak1.intensity +
             peak2.rtmin * peak2.intensity) / it
    rtmax = (peak1.rtmax * peak1.intensity +
             peak2.rtmax * peak2.intensity) / it

    return Peak(mz, it, rt, ri, mzmin, mzmax, rtmin, rtmax)


def MergePeaks(data: List[Peak]):
    data_s = sorted(data, key=lambda peak: float(peak.mz))
    rs = list()
    for i in range(0, len(data_s), 2):
        if i == len(data_s)-1:
            rs.append(data_s[i])
            break
        peak1 = data_s[i]
        peak2 = data_s[i+1]
        # if abs(peak2.mz-peak1.mz) < mz_threshold and abs(
        #         peak2.retention_time-peak1.retention_time) < rt_threshold:
        #     peak = mergePeak(peak1, peak2)
        #     rs.append(peak)
        if math.isclose(peak2.mz, peak1.mz, rel_tol=params.mergMzVar) and math.isclose(
                peak2.retention_time, peak1.retention_time, abs_tol=params.mergRtVar):
            peak = mergePeak(peak1, peak2)
            rs.append(peak)
        else:
            rs.append(peak1)
            rs.append(peak2)
    if len(data_s) != len(rs):
        MergePeaks(rs)
    return rs


def PeakFilterByAbsIntensity(peaks: List[Peak], min_it: float):
    rs = []
    i = 0
    while i < len(peaks):
        peak = peaks[i]
        if peak.intensity < min_it:
            rs.append(peak)
            peaks.remove(peak)
            i -= 1
        i += 1
    return rs


def PeakFilterByRelIntensity(peaks: List[Peak], min_ri: float) -> List[Peak]:
    rs = []
    i = 0
    while i < len(peaks):
        peak = peaks[i]
        if peak.rel_intensity < min_ri:
            rs.append(peak)
            peaks.remove(peak)
            i -= 1
        i += 1
    return rs


def PeakFilter(peaks: list[Peak], min_ri=0.0, min_it=0.0):
    r = peaks.copy()
    if min_ri > 0:
        r = [peak for peak in r if peak.rel_intensity >= min_ri]
    if min_it > 0:
        r = [peak for peak in r if peak.intensity >= min_it]
    return r


def ExtractClusters(peaks: List[Peak], var: float = 5e-4, time_window=0.01) -> List[List[Peak]]:
    results: List[List[Peak]] = list()
    peaks.sort(key=lambda peak: peak.mz)
    i = 0
    while i < len(peaks)-1:
        mz = peaks[i].mz
        rt = peaks[i].retention_time
        matched = False
        cluster: List[Peak] = list()
        j = i+1
        while j < len(peaks):
            _mz = peaks[j].mz
            _rt = peaks[j].retention_time
            if _mz > mz+config.C_ISO_DIFF+var:
                break
            if (math.isclose(mz+config.C_ISO_DIFF, _mz, abs_tol=var)) and math.isclose(rt, _rt, abs_tol=time_window):
            # if (math.isclose(mass+config.C_ISO_DIFF, _m, abs_tol=var) or math.isclose(mass, _m, abs_tol=var)) and math.isclose(rt, _rt, abs_tol=time_window):
                mz = _mz
                rt = _rt
                if not matched:
                    cluster.append(peaks.pop(i))
                    matched = True
                    i -= 1
                    j -= 1
                cluster.append(peaks.pop(j))
                j -= 1
            j += 1
        if matched is True:
            cluster.sort(key=lambda peak: peak.mz)
            results.append(cluster)
        i += 1
    return results

def ExtractClustersWithCharge2(peaks: List[Peak], var: float = 5e-4, time_window=0.01) -> List[List[Peak]]:
    results: List[List[Peak]] = list()
    half_diff = config.C_ISO_DIFF/2.0
    peaks.sort(key=lambda peak: peak.mz)
    i = 0
    while i < len(peaks)-1:
        mz = peaks[i].mz
        rt = peaks[i].retention_time
        matched = False
        cluster: List[Peak] = list()
        j = i+1
        while j < len(peaks):
            _mz = peaks[j].mz
            _rt = peaks[j].retention_time
            if _mz > mz+config.C_ISO_DIFF+var:
                break
            if math.isclose(mz+half_diff, _mz, abs_tol=var) and math.isclose(rt, _rt, abs_tol=time_window):
                if not matched:
                    cluster.append(peaks.pop(i))
                    matched = True
                    i -= 1
                    j -= 1
                cluster.append(peaks.pop(j))
                j -= 1
                mz = _mz
                rt = _rt
            elif math.isclose(mz+config.C_ISO_DIFF, _mz, abs_tol=var) and math.isclose(rt, _rt, abs_tol=time_window):
                if not matched:
                    cluster.append(peaks.pop(i))
                    matched = True
                    i -= 1
                    j -= 1
                cluster.append(Peak(mz+half_diff, 0, rt, 0,mz+half_diff, mz+half_diff, rt, rt))
                cluster.append(peaks.pop(j))
                j -= 1
                mz = _mz
                rt = _rt
            j += 1
        if matched is True:
            cluster.sort(key=lambda peak: peak.mz)
            results.append(cluster)
        i += 1
    return results


if __name__ == '__main__':
    print('test')
    # peaks: list[Peak] = list()
    # data = list()
    # if readXlsx('./test/brain_neg.xlsx', data) == 'SUCCESS':
    #     data.pop(0)
    #     for row in data:
    #         peaks.append(Peak(row[7], row[21], row[10], 0., data=row))
    # NormalizeIntensity(peaks)
    # SplitTable('./test/input template_pairwise.xlsx', './test/')
    # peaks = ReadPeaksFromXlsx('./test/20210122_neg_B315_peak_list.xlsx')
    # clusters =ExtractClusters(peaks)
    # SaveClustersAsXlsx(clusters,'./test/test.xlsx')
    # org_l = len(peaks)
    # print('size of the original peak list: ' + str(org_l))
    # clusters = ExtractClusters(peaks)
    # flat_cluster = [item for sublist in clusters for item in sublist]
    # print('num of cluster: ' + str(len(clusters)))
    # print('num of remained peaks: ' + str(len(peaks)))
    # print('{}+{}={}'.format(len(flat_cluster), len(peaks), len(flat_cluster)+len(peaks)))
