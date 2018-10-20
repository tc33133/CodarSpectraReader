## A Codar CSS/CSQ spectra reader

This repository includes readCS.py which is a reader of Codar Ocean Sensors CSS/CSQ spectra files written in python 3.


```
from readCS import readCS
spectra_file='Data/Spectra/2016_03_Mar/CSS_ANGU_16_03_10_0300.cs
(A1spectra,A2spectra,A3spectra,A12spectra,A13spectra,A23spectra)=readCS(spectra_file)
```
