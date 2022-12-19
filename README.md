# perthfuel2
Perth Fuel for Python WA.  Based on lessons from http://www.pythonwa.com


## Installation


Make sure the correct version of python is in use.

Note: python is python 3.8

```{wsl}
sudo update-alternatives --install /usr/bin/python python $(readlink -f $(which python3)) 3
```

```{wsl}
sudo apt-get install python3-pip
sudo apt-get install python3-venv
```


```{wsl}
python -m venv perthfuel
source perthfuel/bin/activate
```

## Running

```{wsl}
# brings the library back
python -m pip install -r requirements.txt
```

```
# on Windows 
set FLASK_ENV=development
# on Unix
export FLASK_ENV=development
```

```{wsl}
python basic.py
```
## Finish up

CTRL + C
```{wsl}
deactivate
```

## Responsive Design

https://css-tricks.com/responsive-data-tables/