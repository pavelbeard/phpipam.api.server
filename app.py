import json

from flask import Flask
from markupsafe import escape
from logic.php_ipam_gateway import PhpIpamGateway

app = Flask(__name__)

# configure api

api = PhpIpamGateway(
    server="http://10.146.1.34/phpipam",
    app_id="cumsk_invent",
    username="borodinpa",
    password="BPA444nkl444"
)


@app.route('/all_sections')
def all_sections():  # put application's code here
    response = api.get_all_sections()
    return json.dumps(response)


@app.route('/subnets/<section_id>')
def subnets_from_section(section_id):
    response = api.get_subnets_from_section(section_id)
    return json.dumps(response)


@app.route('/subnets/<subnet_id>/addresses')
def return_subnet(subnet_id):
    response = api.get_addresses_from_subnet(subnet_id)
    return json.dumps(response)

if __name__ == '__main__':
    app.run()
