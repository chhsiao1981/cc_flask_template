cc_flask_template
================


Usage
-----
project name/directory is recommended to fit python style (using underscore as project name/directory):

* good: backend_temp
* bad: backend-temp, backendTemp, BackendTemp

```
git clone https://github.com/chhsiao1981/cc_flask_template.git cc; ./cc/scripts/init_dev.sh; . __/bin/activate; ./cc/scripts/init_proj.sh;
```

* create a module: ./scripts/dev_module.sh

Introduction
-----
This template intends to efficiently develop with the following libraries:

* cookiecutter (scaffolding)
* type / str / unicode
* timestamp (by millisecond) / sec_timestamp / datetime / arrow
* sniffer / nosetests (autotest)
* pymongo (db)
* grequests (http post/get)
* ujson (json)
* argparse
* pandas
* lock
* send email
* oauth2
* flask

All are welcome to improve this template


python-social-auth
-----
1. For now, social-auth is for authentication only.
2. need to change data-clientid to the corresponding clientid in /static/login.html
3. need to change social\_auth\_google\_plus\_key and social\_auth\_google\_plus\_secret in .ini
4. The token on client-side should be revoked immediately once the ajax to login complete (success or error).
5. Once the ajax to login successfully complete, the response return \{id, username, first\_name, last\_time, url\}
