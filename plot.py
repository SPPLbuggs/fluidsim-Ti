import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.io import FortranFile
import glob
from scipy.ndimage import zoom

size = 12
med_size = 13
big_size = 14

plt.rc('font', size=size)
plt.rc('axes', titlesize=size)
plt.rc('axes', labelsize=med_size)
plt.rc('xtick', labelsize=size)
plt.rc('ytick', labelsize=size)
plt.rc('legend', fontsize=size)
plt.rc('figure', titlesize=big_size)
plt.rcParams['figure.figsize'] = (4.5, 3)
plt.rcParams['figure.autolayout'] = True

cm_subsection = np.linspace(0.0, 1.0, 4) 
colors = [ cm.plasma(x) for x in cm_subsection ]

path = 'output/'
x = np.fromfile('output/meshx.dat',dtype=float)
y = np.fromfile('output/meshy.dat',dtype=float)
t = np.fromfile('output/time.dat', dtype=float)

nx = len(x)
ny = len(y)
ts = len(t)

phi = np.zeros([nx,ny,ts])
ne = np.zeros([nx,ny,ts])
ni = np.zeros([nx,ny,ts])
nt = np.zeros([nx,ny,ts])
nm = np.zeros([nx,ny,ts])

temp = np.fromfile('output/phi.dat',dtype=float)
phi = temp.reshape([ts, ny, nx])

temp = np.fromfile('output/ni.dat',dtype=float)
ni = temp.reshape([ts, ny, nx])

temp = np.fromfile('output/ne.dat',dtype=float)
ne = temp.reshape([ts, ny, nx])

temp = np.fromfile('output/nt.dat',dtype=float)
nt = temp.reshape([ts, ny, nx])
nt = nt / ne / 1.5

temp = np.fromfile('output/nm.dat',dtype=float)
nm = temp.reshape([ts, ny, nx])

sv = True

if (False):
    t = zoom(t, 200./ts)
    phi = zoom(phi, [200./ts, 1, 1])
    ne = zoom(ne, [200./ts, 1, 1])
    ni = zoom(ni, [200./ts, 1, 1])
    nt = zoom(nt, [200./ts, 1, 1])
    nm = zoom(nm, [200./ts, 1, 1])
    ts = len(t)

xx,tt = np.meshgrid(x,t)
yloc = 0

tloc = [ts/10,ts/2,-1]
tloc[0] = np.argmin(np.abs(t-0.2))

nxticks = np.array([1e12, 1e13, 1e14, 1e15, 1e16, 1e17, 1e18, 1e19, 1e20])
nxlim   = [3e14, 5e19]

# *** phi Plot ***
fig,axes = plt.subplots(1,2,sharey=True,figsize=[8,3])
(ax1,ax2) = axes
ax1.plot(phi[tloc[0],yloc,:],x,label='{:.1f}us'.format(t[tloc[0]]), color = colors[0])
ax1.plot(phi[tloc[1],yloc,:],x,label='{:.1f}us'.format(t[tloc[1]]), color = colors[1])
ax1.plot(phi[tloc[2],yloc,:],x,label='{:.1f}us'.format(t[tloc[2]]), color = colors[2])
ax1.set_xlabel('Electric Potential (V)')
ax1.set_ylabel('x (mm)')
ax1.set_ylim([0, 7.5])
ax1.set_yticks(np.arange(0,7.6,1.5))
ax1.legend(frameon=False, loc='best')

im = ax2.contourf(tt,xx,phi[:,yloc,:],30, cmap = 'plasma', zorder = -20)
ax2.set_xlabel('Time ($\mu$s)')
plt.suptitle(r'(a) Electric Potential ($\phi$)')
clb = fig.colorbar(im)
clb.ax.set_title('(V)')
ax2.set_xscale('log')
#ax2.set_rasterization_zorder(-10)

if (sv):
    plt.savefig('figures/phi_streak.eps', dpi=300, frameon=None)

# *** Ne Plot ***
if ne.max() > nxlim[0]:
    fig,axes = plt.subplots(1,2,sharey=True,figsize=[8,3])
    (ax1,ax2) = axes
    ax1.plot(ne[tloc[0],yloc,:],x,label='{:.1f}us'.format(t[tloc[0]]), color = colors[0])
    ax1.plot(ne[tloc[1],yloc,:],x,label='{:.1f}us'.format(t[tloc[1]]), color = colors[1])
    ax1.plot(ne[tloc[2],yloc,:],x,label='{:.1f}us'.format(t[tloc[2]]), color = colors[2])
    ax1.set_xlabel('Density (m-3)')
    ax1.set_xscale('log')
    ax1.set_xticks(nxticks)
    ax1.set_xlim(nxlim)
    ax1.set_ylabel('x (mm)')
    ax1.set_ylim([0, 7.5])
    ax1.set_yticks(np.arange(0,7.6,1.5))
    ax1.legend(frameon=False, loc='best')
    
    v = np.linspace(np.log10(nxlim[0]), np.log10(nxlim[-1]),30)
    im = ax2.contourf(tt,xx, np.maximum(np.log10(ne[:,yloc,:]),v[0]), v,
                      cmap='plasma', zorder=-20)
    ax2.set_xlabel('Time ($\mu$s)')
    plt.suptitle('(b) Electron Density (n$_e$)')
    v = np.log10(nxticks)
    clb = fig.colorbar(im, ticks =v)
    clb.ax.set_title('(log$_{10}$m$^{-3}$)')
    ax2.set_xscale('log')
    #ax2.set_rasterization_zorder(-10)
    
    if (sv):
        plt.savefig('figures/ne_streak.eps', dpi=300, frameon=None)

# *** Ni Plot ***
if ni.max() > nxlim[0]:
    fig,axes = plt.subplots(1,2,sharey=True,figsize=[8,3])
    (ax1,ax2) = axes
    ax1.plot(ni[tloc[0],yloc,:],x,label='{:.1f}us'.format(t[tloc[0]]), color = colors[0])
    ax1.plot(ni[tloc[1],yloc,:],x,label='{:.1f}us'.format(t[tloc[1]]), color = colors[1])
    ax1.plot(ni[tloc[2],yloc,:],x,label='{:.1f}us'.format(t[tloc[2]]), color = colors[2])
    ax1.set_xlabel('Density (m-3)')
    ax1.set_xscale('log')
    ax1.set_xticks(nxticks)
    ax1.set_xlim(nxlim)
    ax1.set_ylabel('x (mm)')
    ax1.set_ylim([0, 7.5])
    ax1.set_yticks(np.arange(0,7.6,1.5))
    ax1.legend(frameon=False, loc='best')
    
    v = np.linspace(np.log10(nxlim[0]), np.log10(nxlim[-1]),30)
    im = ax2.contourf(tt,xx,np.maximum(np.log10(ni[:,yloc,:]),v[0]), v,
                      cmap='plasma', zorder=-20)
    ax2.set_xlabel('Time ($\mu$s)')
    plt.suptitle('(c) Ion Density (n$_i$)')
    v = np.log10(nxticks)
    clb = fig.colorbar(im, ticks = v)
    clb.ax.set_title('(log$_{10}$m$^{-3}$)')
    ax2.set_xscale('log')
    #ax2.set_rasterization_zorder(-10)
    
    if (sv):
        plt.savefig('figures/ni_streak.eps', dpi=300, frameon=None)

# *** Nt Plot ***
if nt.max() > 1.01:
    fig,axes = plt.subplots(1,2,sharey=True,figsize=[8,3])
    (ax1,ax2) = axes
    ax1.plot(nt[tloc[0],yloc,:],x,label='{:.1f}us'.format(t[tloc[0]]), color = colors[0])
    ax1.plot(nt[tloc[1],yloc,:],x,label='{:.1f}us'.format(t[tloc[1]]), color = colors[1])
    ax1.plot(nt[tloc[2],yloc,:],x,label='{:.1f}us'.format(t[tloc[2]]), color = colors[2])
    ax1.set_xlabel('Temperature (eV)')
    ax1.set_xscale('log')
    ax1.set_xlim([0.2, 150])
    ax1.set_ylabel('x (mm)')
    ax1.set_ylim([0, 7.5])
    ax1.set_yticks(np.arange(0,7.6,1.5))
    ax1.legend(frameon=False, loc='best')
    
    v = np.linspace(-0.7,2.5,30)
    im = ax2.contourf(tt,xx,np.maximum(np.log10(nt[:,yloc,:]),v[0]),v,
                      cmap='plasma', zorder=-20)
    ax2.set_xlabel('Time ($\mu$s)')
    plt.suptitle('(d) Electron Temperature (T$_e$)')
    v = np.arange(-1,3,1)
    clb = fig.colorbar(im, ticks=v)
    clb.ax.set_title('(log$_{10}$eV)')
    ax2.set_xscale('log')
    #ax2.set_rasterization_zorder(-10)
    
    if (sv):
        plt.savefig('figures/nt_streak.eps', dpi=300, frameon=None)

# *** Nm Plot ***
if nm.max() > nxlim[0]:
    xx,tt = np.meshgrid(x,t)
    fig,axes = plt.subplots(1,2,sharey=True,figsize=[8,3])
    (ax1,ax2) = axes
    ax1.plot(nm[tloc[0],yloc,:],x,label='{:.1f}us'.format(t[tloc[0]]), color = colors[0])
    ax1.plot(nm[tloc[1],yloc,:],x,label='{:.1f}us'.format(t[tloc[1]]), color = colors[1])
    ax1.plot(nm[tloc[2],yloc,:],x,label='{:.1f}us'.format(t[tloc[2]]), color = colors[2])
    ax1.set_xlabel('Density (m-3)')
    ax1.set_xscale('log')
    ax1.set_xticks(nxticks)
    ax1.set_xlim(nxlim)
    ax1.set_ylabel('x (mm)')
    ax1.set_ylim([0, 7.5])
    ax1.set_yticks(np.arange(0,7.6,1.5))
    ax2.set_xscale('log')
    ax1.legend(frameon=False, loc='best')
    
    v = np.linspace(np.log10(nxlim[0]), np.log10(nxlim[-1]),30)
    im = ax2.contourf(tt,xx,np.maximum(np.log10(nm[:,yloc,:]),v[0]),v,
                      cmap='plasma',zorder=-20)
    ax2.set_xlabel('Time ($\mu$s)')
    plt.suptitle('(e) Metastable Density (n$_m$)')
    v = np.log10(nxticks)
    clb = fig.colorbar(im,ticks=v)
    clb.ax.set_title('(log$_{10}$m$^{-3}$)')
    #ax2.set_rasterization_zorder(-10)
    
    if (sv):
        plt.savefig('figures/nm_streak.eps', dpi=300, frameon=None)

# *** 2D Plots ***
if len(y) > 1:
    fig = plt.figure(figsize=(4.0,3.5))
    plt.xlabel('y')
    plt.ylabel('x')
    plt.axis('equal')
    plt.contourf(y, x, phi[-1,:,:].T, 30, zorder=-20, cmap = 'plasma')
    plt.colorbar()
    plt.title('(f) 2D Potential ($\phi$)')
    #plt.rasterization_zorder(-10)
    
    if (sv):
        plt.savefig('figures/phi_2d.eps', dpi=300, frameon=None)
    
    
    fig = plt.figure(figsize=(4.0,3.5))
    plt.xlabel('y')
    plt.ylabel('x')
    plt.axis('equal')
    v = np.linspace(np.log10(nxlim[0]), np.log10(nxlim[-1]),30)
    plt.contourf(y, x, np.maximum(np.log10(ne[-1,:,:].T+1), v[0]), v, 
                 zorder=-20, cmap = 'plasma')
    v = np.log10(nxticks)
    clb = fig.colorbar(im, ticks = v)
    plt.title('(g) 2D Electron Density (n$_e$)')
    #plt.rasterization_zorder(-10)
    
    if (sv):
        plt.savefig('figures/ne_2d.eps', dpi=600, frameon=None)


plt.show()