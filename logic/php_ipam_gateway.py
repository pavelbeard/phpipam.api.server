import requests
import json


class PhpIpamGateway:
    def __init__(self, server, app_id, username, password):
        self.__server = server
        self.__appid = app_id
        self.__username = username
        self.__password = password
        self.__baseurl = f"{self.__server}/api/{self.__appid}"

    def __get_auth_token(self):
        res = requests\
            .post(f"{self.__baseurl}/user/", auth=(self.__username, self.__password))
        token = json.loads(res.content)['data']['token']
        return {'token': token}

    #not working
    def get_all_subnets_not_work(self, token, search_iterations):
        subnets_list = set()

        try:
            res = requests.get(f"{self.__baseurl}/sections/", headers=token)
            subnets = res.json()['data']
            subnets_id_list = []

            for subnet in subnets:
                subnets_id_list.append(subnet)

            j = search_iterations
            for subnet_id in subnets_id_list:
                try:
                    res = requests.get(f"{self.__baseurl}/subnets/{subnet_id}/", headers=token)
                    data = res.json()['data']
                    subnets_list.add(f"{data['subnet']}/{data['mask']}")
                except BaseException as ex:
                    while j > 0:
                        if j != subnet_id:
                            try:
                                res = requests.get(f"{self.__baseurl}/subnets/{j}/", headers=token)
                                data = res.json()['data']
                                if not (f"{data['subnet']}/{data['mask']}" in subnets_list):
                                    subnets_list.add(f"{data['subnet']}/{data['mask']}")
                                    break
                                else:
                                    raise Exception('item has exist')
                            except BaseException as ex:
                                j -= 1
                                print(j)

            return subnets_list
        except BaseException as ex:
            print(ex)
            return subnets_list

    def get_subnet_by_id(self, subnet_id):
        try:
            res = requests.get(f"{self.__baseurl}/subnets/{subnet_id}/", headers=self.__get_auth_token())
            return res.json()['data']
        except BaseException as ex:
            return ex

    def get_section_by_name(self, name):
        try:
            res = requests.get(f"{self.__baseurl}/sections/{name}/", headers=self.__get_auth_token())
            return res.json()['data']
        except BaseException as ex:
            return ex

    def get_all_sections(self):
        try:
            res = requests.get(f"{self.__baseurl}/sections/", headers=self.__get_auth_token())
            sections = res.json()['data']

            data = []

            for section in sections:
                data.append({'section_id': section['id'], 'section_name': section['name']})

            return data
        except BaseException as ex:
            return ex

    def get_subnets_from_section(self, section_id):
        try:
            res = requests.get(f"{self.__baseurl}/sections/{section_id}/subnets", headers=self.__get_auth_token())
            subnets = res.json()['data']

            data = []

            for subnet in subnets:
                data.append({'subnet_id': subnet['id'], 'subnet': f"{subnet['subnet']}/{subnet['mask']}"})

            return data
        except BaseException as ex:
            return ex

    def get_addresses_from_subnet(self, subnet_id):
        try:
            # запрашиваем адреса в подсети
            res = requests.get(f"{self.__baseurl}/subnets/{subnet_id}/addresses", headers=self.__get_auth_token())
            addresses = res.json()['data']

            subnet_data = requests.get(f"{self.__baseurl}/subnets/{subnet_id}", headers=self.__get_auth_token())
            subnet = subnet_data.json()['data']
            subnet = f"{subnet['subnet']}/{subnet['mask']}"

            # формируем список адресов в подсети
            data = {subnet: []}

            for address in addresses:
                data[subnet].append(address['ip'])

            return data
        except BaseException as ex:
            return ex
