from isotopicHelper import IsotopicVariants
from matplotlib import pyplot as plt
import numpy as np
from peakHelper import Peak
from typing import List


def histRelativeIntensity(peaks: List[Peak]):
    peaks.sort(key=lambda peak: peak.mz)
    mz_list = []
    it_list = []
    for peak in peaks:
        mz_list.append(peak.mz)
        it_list.append(peak.rel_intensity * 100)

    for i_x, i_y in zip(mz_list, it_list):
        plt.text(i_x, i_y, '({:.7f}, {:.7f})'.format(i_x, i_y))
    rg = mz_list[-1] - mz_list[0]
    plt.xlim(mz_list[0]-rg/2, mz_list[-1]+rg/2)
    plt.ylim(0, max(it_list)*1.5)

    # draw the profile
    plt.bar(x=mz_list, height=it_list, width=0.01)
    plt.xlabel("m/z")
    plt.ylabel("Intensity")
    plt.show()


def histIntensity(peaks: List[Peak]):
    peaks.sort(key=lambda peak: peak.mz)
    mz_list = []
    it_list = []
    for peak in peaks:
        mz_list.append(peak.mz)
        it_list.append(peak.intensity)

    for i_x, i_y in zip(mz_list, it_list):
        plt.text(i_x, i_y, '({:.7f}, {:.7f})'.format(i_x, i_y))
    rg = mz_list[-1] - mz_list[0]
    plt.xlim(mz_list[0]-rg/2, mz_list[-1]+rg/2)
    plt.ylim(0, max(it_list)*1.5)

    # draw the profile
    plt.bar(x=mz_list, height=it_list, width=0.01)
    plt.xlabel("m/z")
    plt.ylabel("Intensity")
    plt.show()


def plotGaussian(iso_vars: IsotopicVariants):

    peaks: list(Peak) = list()
    for i in range(iso_vars.peakNum):
        peaks.append(iso_vars.GetPeak(i))
    peaks.sort(key=lambda peak: peak.mz)
    mz_list = []
    ri_list = []
    for peak in peaks:
        mz_list.append(peak.mz)
        ri_list.append(peak.rel_intensity*100)
    mz_grid = np.arange(peaks[0].mz - 1,
                        peaks[-1].mz + 1, 0.02)
    ri = np.zeros_like(mz_grid)
    sigma = 0.002
    for peak in peaks:
        # Add gaussian peak shape centered around each theoretical peak
        ri += peak.rel_intensity * np.exp(-(mz_grid - peak.mz) ** 2 / (2 * sigma)
                                          ) / (np.sqrt(2 * np.pi) * sigma)

    # Normalize profile to 0-100
    # ri *= 100

    # draw the profile

    for i_x, i_y in zip(mz_list, ri_list):
        plt.text(i_x, i_y*2, '({:.7f}, {:.4f}%)'.format(i_x, i_y))
    plt.title("Isotopic Distribution")
    plt.plot(mz_grid, ri)
    plt.xlabel("m/z")
    plt.ylabel("Relative intensity(%)")
    plt.show()



if __name__ == '__main__':
    print('Test: ')
    iso_var = IsotopicVariants(mz_list=[101,102,103,104,105],abundance_list=[0.87,0.08,0.03,0.015,0.005])
    plotGaussian(iso_var)
    pass
