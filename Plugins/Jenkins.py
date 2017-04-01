import jenkins
import time
import os
from Common import Get
from configparser import ConfigParser


def get_job_info(job_name):
    jenkins_conf_path = os.path.join(Get.base_dir(), 'Conf', 'Jenkins.ini')
    cf = ConfigParser()
    cf.read(jenkins_conf_path, 'utf-8')
    server = jenkins.Jenkins(cf.get('base', 'host'), username=cf.get('base', 'username'),
                             password=cf.get('base', 'password'))
    # user = server.get_whoami()
    # version = server.get_version()
    # print('Hello %s from Jenkins %s' % (user['fullName'], version))

    # jobs=server.get_jobs()
    # print(jobs)

    last_build_number = \
        server.get_job_info(job_name)['lastCompletedBuild'][
            'number']
    build_info = server.get_build_info(job_name, last_build_number)

    version = ''
    starter = ''
    # print(build_info)
    # exit()
    for i1 in build_info['actions']:
        if 'parameters' in i1:
            for i2 in i1['parameters']:
                if 'value' in i2 and 'name' in i2:
                    version += i2['name'] + ':' + i2['value'] + ' '

        if 'causes' in i1:
            for i2 in i1['causes']:
                if 'userName' in i2:
                    starter += i2['userName'] + ' '

    version = version.rstrip(' ')
    starter = starter.rstrip(' ')
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(build_info['timestamp'] / 1000))
    return version, starter, date
