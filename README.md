[![CircleCI](https://circleci.com/gh/PLsergent/pdc_itlink.svg?style=shield&circle-token=c11bd2d91f03487614b7310d8552680f5a0aec6d)](https://circleci.com/gh/PLsergent/pdc_itlink)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

_Special thanks to [IT Link](https://www.itlink.fr/) that gave me the opportunity to develop this application during my 10 weeks internship._

# Outil\_PDC

## Installation

Clone the repository :

```text
git clone https://github.com/PLsergent/pdc_itlink
```

Install dependencies :

```text
cd pdc_itlink/
pipenv install
```

Run the application :

```text
cd pdc_app/
pipenv run python manage.py runserver
```

By default got to this url : [http://127.0.0.1:8000/pdc/](http://127.0.0.1:8000/pdc/)

Default super_user :
- username : admin
- password : admin

Good to go !

## Description

Internal management web application used to manage workloads planed. Through the application you can manage your projects, clients, tasks and assignments.

## Screenshots

![projets](https://github.com/PLsergent/pdc_itlink/blob/master/pdc_app/pdc_core_app/static/image/projets_screen.png?raw=true)
![collab](https://github.com/PLsergent/pdc_itlink/blob/master/pdc_app/pdc_core_app/static/image/collab_screen.png?raw=true)


