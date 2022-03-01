import redis
import json
from jinja2 import Environment, FileSystemLoader
import os

r = redis.Redis(
            host='127.0.0.1',
                port=6379)

data = r.get('www.quanlm1999-testz.tk')
dict = json.loads(data.decode("UTF-8"))
print(dict["waf"]["enable"])
print(dict["waf"]["rule"])
print(dict["waf"]["lb"])

rule_config = "/usr/local/openresty/nginx/modsec/" + dict["waf"]["rule"] + ".conf"
file_loader = FileSystemLoader('/root/config-generator/template/')
jinja_env = Environment(loader=file_loader)
template = jinja_env.get_template('nginx_cdn_template')
if dict["waf"]["lb"]:
    with open(rule_config, 'w') as f:
        f.write(template.render(rule_path=rule_config,
                                domain="www.quanlm1999-testz.tk",
                                lb_ip=dict["waf"]["lb"]
                                ))

else:
    with open(rule_config, 'w') as f:
        f.write(template.render(rule_path=rule_config,
                                domain="www.quanlm1999-testz.tk"
                                ))
os.chmod(rule_config, 0o644)