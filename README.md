# perthfuel2
Perth Fuel for Python WA.  Based on lessons from http://www.pythonwa.com

Deployed to https://perthfuel2.herokuapp.com


Still neeed to learn about Heroku


## Setup Environment
sudo apt-get install python3-pip
sudo apt-get install python3-venv

python3 -m venv perthfuel
source perthfuel/bin/activate

Install packages
```
pip3 install -r requirements.txt
```


Saving
```
pip3 freeze > requirements2.txt
```

## Running

```
# on Windows 
set FLASK_ENV=development
# on Unix
export FLASK_ENV=development

flask run
python3 basic.py
```


## Responsive Design

https://css-tricks.com/responsive-data-tables/