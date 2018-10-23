#/Users/tom/anaconda/bin/python
from datetime import datetime
import struct
import numpy as np

def datatoSS(a):
    return 10*np.log10(np.abs(a)) - (-40. + 5.8)

def tenlogten(a):
    return 10*np.log10(np.abs(a))

def secondsAdjust():
    d1 = datetime.strptime("1904-01-01", "%Y-%m-%d")
    d2 = datetime.strptime("1970-01-01", "%Y-%m-%d")
    return abs((d2 - d1).total_seconds())


def readCS(spectra_file):
    with open(spectra_file,'rb') as f:  

    ### Header stuff    
        data=f.read(72)
        (fileversion,filetime,v1extent,cskind,v2extent,sitecode,v3extent,
        coverageminutes,deletedsource,overridesource,centerfreq,
        sweepfreq,bandwidth,sweepup,nDopplerCells,nRangeCells,firstrangecell,
        rangecelldist,v4extent)=struct.unpack('>hIihi4siiiifffiiiifi',data)

        filetime=datetime.utcfromtimestamp(float(filetime-secondsAdjust()))

    #    print(fileversion,filetime,v1extent,cskind,v2extent,sitecode.decode('utf-8'),
    #          v3extent,coverageminutes,deletedsource,overridesource,centerfreq,
    #          sweepfreq,bandwidth,sweepup,dopplercells,nRangeCells,firstrangecell,
    #          rangecelldist,v4extent)

    ### Spectra data
        A1spectra=np.empty([nRangeCells,nDopplerCells],dtype=np.float)
        A2spectra=np.empty([nRangeCells,nDopplerCells],dtype=np.float)
        A3spectra=np.empty([nRangeCells,nDopplerCells],dtype=np.float)
        A12spectra=np.empty([nRangeCells,nDopplerCells],dtype=np.complex)
        A13spectra=np.empty([nRangeCells,nDopplerCells],dtype=np.complex)
        A23spectra=np.empty([nRangeCells,nDopplerCells],dtype=np.complex)
        if cskind==2:
            quality=np.empty([nRangeCells,nDopplerCells],dtype=np.float)

        for i in range(0,nRangeCells):
            for j in range(0,nDopplerCells):
                A1spectra[i,j]=struct.unpack('>f',f.read(4))[0]

            for j in range(0,nDopplerCells):
                A2spectra[i,j]=struct.unpack('>f',f.read(4))[0]

            for j in range(0,nDopplerCells):
                A3spectra[i,j]=struct.unpack('>f',f.read(4))[0]

            for j in range(0,nDopplerCells):
                real=struct.unpack('>f',f.read(4))[0]
                imag=struct.unpack('>f',f.read(4))[0]            
                A12spectra[i,j]=real+1j*imag

            for j in range(0,nDopplerCells):
                real=struct.unpack('>f',f.read(4))[0]
                imag=struct.unpack('>f',f.read(4))[0]
                A13spectra[i,j]=real+1j*imag

            for j in range(0,nDopplerCells):
                real=struct.unpack('>f',f.read(4))[0]
                imag=struct.unpack('>f',f.read(4))[0]
                A23spectra[i,j]=real+1j*imag  

            if cskind==2:
                for j in range(0,nDopplerCells):
                    quality[i,j]=struct.unpack('>f',f.read(4))[0]

        return A1spectra,A2spectra,A3spectra,A12spectra,A13spectra,A23spectra