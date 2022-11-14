#!/usr/bin/env python3

from cProfile import label
import numpy as np
from matplotlib.ticker import LinearLocator, FixedLocator, AutoMinorLocator, MaxNLocator
import pandas as pd
import os
import sys
from shutil import which
import matplotlib.pyplot as plt
import json


from matplotlib import rc, rcParams
from matplotlib.image import NonUniformImage
from matplotlib import cm, ticker
from matplotlib.font_manager import FontProperties
import matplotlib
config = {
    "font.family": ["serif", "Times New Roman"],
    "font.size": 20,
    "mathtext.fontset": 'stix',
    "font.serif": ['Computer Modern'],
    "text.latex.preamble": r"\usepackage{amsmath}"
}
rcParams.update(config)
plt.rcParams['axes.formatter.min_exponent'] = 2
from matplotlib.ticker import LogFormatterSciNotation

class CustomTicker(LogFormatterSciNotation):
    def __call__(self, x, pos=None):
        if x not in [0.1,1,10]:
            return LogFormatterSciNotation.__call__(self,x, pos=None)
        else:
            return "{x:g}".format(x=x)

from matplotlib.colors import LinearSegmentedColormap
cmap_name = "self"
collist = ["#02004f", "#000b57", "#00165e", "#002166", "#012c6e", "#003875", '#00437d', "#004e85", "#00598c", "#026494", "#006f9c", "#007aa3", "#0085ab", "#0090b3", "#009cba", "#27a699", "#4bb178", "#70bc56", "#97c637", "#d2c70d", "#e8bd08", "#ffb300", "#ffbf2a", "#fecc55", "#ffd980", "#ffe6aa", "#ffe6aa"]
cmap = LinearSegmentedColormap.from_list(cmap_name, collist, N=256)

pwd = os.path.abspath(os.path.dirname(__file__))

# print(data)


fig = plt.figure(figsize=(10, 9))
axy = fig.add_axes([0.1026, 0.21, 0.09, 0.73 ])
axx = fig.add_axes([0.198, 0.104, 0.657, 0.1 ])
ax  = fig.add_axes([0.198, 0.21, 0.657, 0.73])
axc = fig.add_axes([0.86, 0.235, 0.02, 0.7])

# data = pd.read_csv(f"{pwd}/Data/WW_reportDF.csv")
# ax.text(0.02, 1.001, r"$W^+ W^-, W \to \mu \nu_{\mu}$", fontsize=26, ha='left', va='bottom', transform=ax.transAxes)
# xsect = 194.167
# nmc = 1.e6

# data = pd.read_csv(f"{pwd}/Data/ZZ_reportDF.csv")
# ax.text(0.02, 1.001, r"$ZZ\to \mu\mu \nu\nu$", fontsize=26, ha='left', va='bottom', transform=ax.transAxes)
# xsect = 15.6359
# nmc = 1.e6

# data = pd.read_csv(f"{pwd}/Data/smu50_chi0_reportDF.csv")
# ax.text(0.02, 1.001, r"$(m_{\tilde{\mu}}, m_{\tilde{\chi}_1^0}) = (50, 0)~{\rm GeV}$", fontsize=26, ha='left', va='bottom', transform=ax.transAxes)
# xsect = 56.12
# nmc = 1.e6

data = pd.read_csv(f"{pwd}/Data/Tau_reportDF.csv")
xsect = 1886.47 * 0.1739 * 0.1739
ax.text(0.02, 1.001, r"$\tau^+\tau^- \to \mu^+\mu^- \nu\nu\nu\nu $", fontsize=26, ha='left', va='bottom', transform=ax.transAxes)
nmc = 113317

# data = pd.read_csv(f"{pwd}/Data/smu100_chi0.csv")
# ax.text(0.02, 1.001, r"$(m_{\tilde{\mu}}, m_{\tilde{\chi}_1^0}) = (100, 0)~{\rm GeV}$", fontsize=26, ha='left', va='bottom', transform=ax.transAxes)
# xsect = 171.148
# nmc = 1.e6

# data = pd.read_csv(f"{pwd}/Data/smu100_chi40.csv")
# ax.text(0.02, 1.001, r"$(m_{\tilde{\mu}}, m_{\tilde{\chi}_1^0}) = (100, 40)~{\rm GeV}$", fontsize=26, ha='left', va='bottom', transform=ax.transAxes)
# xsect = 171.148
# nmc = 1.e6


ax.text(1.15, 1.01, r"$\int \mathcal{L} = 5.05~{\rm ab}^{-1}, \quad \sqrt{s} = 240~{\rm GeV}$", fontsize=18, ha='right', va='bottom', transform=ax.transAxes)

lint = 5050
weight = xsect * lint / nmc
# weight = xsect * lint
data['weight'] = weight
# print(data)

cc = ax.hist2d(data['mLSPmax'], data['mRecoil'], 120, weights=data['weight'], range=[[0, 120], [0, 240]], cmap=cmap, cmin=weight, norm=matplotlib.colors.LogNorm(vmin=weight), zorder=10)
axx.hist(data['mLSPmax'], 120, color='#2e66ff', histtype="stepfilled", alpha=0.5, orientation='vertical', zorder=10)
axx.hist(data['mLSPmax'], 120, color='#231aa5', histtype="step", alpha=1, orientation='vertical', zorder=10)
axy.hist(data['mRecoil'], 120, color='#2e66ff', histtype="stepfilled", alpha=0.5, orientation='horizontal', zorder=10)
axy.hist(data['mRecoil'], 120, color='#231aa5', histtype="step", alpha=1, orientation='horizontal', zorder=10)

axy.grid(axis="both", which='major', alpha=0.8, zorder=1)
ax.grid(axis="both", which='major', alpha=0.8, zorder=1)
axx.grid(axis="both", which='major', alpha=0.8, zorder=1)
axy.grid(axis="both", which='minor', alpha=0.2, zorder=1)
ax.grid(axis="both", which='minor', alpha=0.2, zorder=1)
axx.grid(axis="both", which='minor', alpha=0.2, zorder=1)
fig.colorbar(cc[3], cax=axc)

axx.set_xlim(0, 120)
axy.set_ylim(0, 240)
ax.set_xlim(0,120)
ax.set_ylim(0,240)
# axc.set_ylim(0, 300)

# ax.yaxis.set_minor_locator(FixedLocator(np.linspace(0, 120, 26)))
ax.yaxis.set_major_locator(FixedLocator(np.linspace(0, 240, 7)))
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.tick_params(
    which='both',
    direction="in",
    left=True,
    right=True,
    bottom=True,
    top=True
)
ax.tick_params(which="major", length=10, width=1.2)
ax.tick_params(which="minor", length=4, width=1.2)
ax.set_xticklabels([])
ax.set_yticklabels([])

axc.tick_params(
    which='both',
    direction="in",
    labelsize=20,
    left=False,
    right=True,
    bottom=False,
    top=False
)
axc.tick_params(which="major", length=7, width=2.0, color='w')
axc.tick_params(which="minor", length=4, width=1.2, color='w')

axx.xaxis.set_minor_locator(AutoMinorLocator())
axx.yaxis.set_major_locator(MaxNLocator(2))
axx.yaxis.set_minor_locator(AutoMinorLocator())
axx.yaxis.tick_right()
# axx.yaxis.set_major_formatter(CustomTicker())

axx.tick_params(
    which='both',
    direction="in",
    labelsize=16,
    left=True,
    right=True,
    bottom=True,
    top=True
)
axx.tick_params(which="major", length=10, width=1.2)
axx.tick_params(which="minor", length=4, width=1.2)
# axx.set_xticklabels([])
# axx.set_yticklabels([])

axy.yaxis.set_major_locator(FixedLocator(np.linspace(0, 240, 7)))
axy.yaxis.set_minor_locator(AutoMinorLocator())
axy.xaxis.set_major_locator(MaxNLocator(2))
axy.xaxis.set_minor_locator(AutoMinorLocator())
axy.xaxis.tick_top()
axy.tick_params(
    which='both',
    direction="in",
    labelsize=16,
    left=True,
    right=True,
    bottom=True,
    top=True
)
axy.tick_params(which="major", length=6, width=1.2)
axy.tick_params(which="minor", length=3.6, width=1.2)
# axy.xaxis.set_major_formatter(CustomTicker())

# axy.set_xticklabels([])
# axy.set_yticklabels([])

axx.set_xlabel(r"$m_{\rm LSP}^{\rm max}~[{\rm GeV}]$", fontsize=30, loc='right')
axy.set_ylabel(r"$m_{\rm Recoil}~[{\rm GeV}]$", fontsize=30, loc='top')
axc.set_ylabel(r"Events $\left/ (1~{\rm GeV}\times 1~{\rm GeV})\right.$", fontsize=30, loc='top')


# plt.show()
# plt.savefig("Figure/ww2d1.pdf")
# plt.savefig("Figure/zz2d1.pdf")
# plt.savefig("Figure/smuon2d1.pdf")
plt.savefig("Figure/tau2d1.pdf")
# plt.savefig("Figure/smuon100_0_2d1.pdf")
# plt.savefig("Figure/smuon100_40_2d1.pdf")