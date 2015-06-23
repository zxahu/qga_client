__author__ = 'zhang11'

from novaclient.v1_1 import client
from cinderclient import client as cclient
from keystoneclient.v2_0 import client as kclient
from glanceclient import Client as gclient
import re

import commands

user = 'admin'
password = 'ec@openstack'
tenant = 'admin'
auth_url = 'http://10.239.19.216:35357/v2.0/'



class OpenStack(object):

    image_list ={}
    nt = None
    ct = None
    kt = None

    def __init__(self):

        self.nt = client.Client(user, password, tenant, auth_url, service_type="compute")
        self.ct = cclient.Client('1',user,password,tenant,auth_url)
        #self.kt = kclient.Client(username=user, password=password, tenant_name=tenant, auth_url=auth_url)
        search_opts = {'all_tenants': '--all-tenants'}
        self.get_images()

    def get_uuid(self,guest):
        reg_f = r'instance-\S{8}'
        reg = r'<uuid>\S{36}</uuid>'
        guest = re.search(reg_f,guest).group(0)
        command = "virsh dumpxml "+guest
        (status, output) = commands.getstatusoutput(command)
        match = re.search(reg,output)
        if match:
            uuid = match.group(0)
            return uuid[6:42]
        else:
            return "uuid not found"

    def get_images(self):
        images = self.nt.images.list()
        for image in images:
            self.image_list[image.id]=image.name


    def get_os(self,uuid):
        vm = self.nt.servers.get(uuid)
        image_id = vm.image['id']
        if image_id == '':
            # means boot from volume
            vol = getattr(vm,'os-extended-volumes:volumes_attached')
            vol_id = vol[0]['id']
            volume = self.ct.volumes.get(vol_id)
            image_id = volume.volume_image_metadata['image_id']

        image = self.image_list[image_id]
        return image



