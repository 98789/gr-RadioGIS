# gr-RadioGIS
RadioGIS GNU Radio Blocks

## Prerequisites ##

* A Linux-based OS.
* GNU Radio.
* UHD.
* git.

Python 2.x is also required, but it comes by default with any Linux distribution. You need to install GNU Radio either manually from source or using the build script (if not you won't be able to install UHD nor install the blocks).

## Installing the blocks ##

* Clone this repository:  

```
#!bash

git clone https://bitbucket.org/radiogisuis/gr-radiogis
```

* Navigate to the innermost gr-RadioGIS folder:  

```
#!bash

cd gr-RadioGIS/gr-RadioGIS
```

* Create a build folder and navigate to it:  

```
#!bash

mkdir build && cd build
```

* Install the blocks:  

```
#!bash

cmake ..  
make  
sudo make install  
sudo ldconfig
```


now you are good to go, blocks will be available both from the command line and from grc.  
  
If you find issues or, want to suggest an improvement or request the addition of new features, please write to jmunoz@radiogis.uis.edu.co or dacosta@radiogis.uis.edu.co.