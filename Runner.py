import os
import sys
import time
import unittest

from Common import Get
from Core.HTMLTestRunner import HTMLTestRunner
from Plugins import Mail, Jenkins
from TestCase.App import AppNative
from TestCase.Web import UserCenter

# job_name = 'LFT_test_9.27_java_ehome_app-native-http_liuyu8080'
job_name = sys.argv[1]
job_name_list = []
for item in Jenkins.get_jobs_info():
    job_name_list.append(item['name'])
if job_name not in job_name_list:
    print('Please input correct job name!!!')
    exit()

print('\n')
print('==============================================================================')
print('Automation Test Script')
print('==============================================================================')

x, y, z = Jenkins.get_job_info(job_name)
jenkins_ls = [('Job Name', job_name),
              ('Version', x),
              ('Builder', y),
              ('Build Finish Time', z)]
print('Get jenkins info successfully...')

# test_suite = unittest.TestSuite()
# test_suite.addTests([UserCenter('saveUserInfo')])
user_center = unittest.TestLoader().loadTestsFromTestCase(UserCenter)
app_native = unittest.TestLoader().loadTestsFromTestCase(AppNative)
total_test = unittest.TestSuite([user_center, app_native])

timeStampArr = time.localtime(time.time())
folder = Get.base_dir() + '/Html/' + time.strftime('%Y-%m-%d', timeStampArr) + '/'
os.makedirs(folder, exist_ok=True)
file = folder + time.strftime('%H-%M-%S') + '.html'

with open(file, 'w', encoding='utf-8') as f:
    HTMLTestRunner(stream=f, title='Automation Script Report', description=u'').run(total_test, jenkins_ls)
print('Finish to run test case...')
print('Generate report successfully...')
with open(file, 'r') as f:
    content = f.read()
if Mail.send_mail('Automation Script Report', content):
    print('Email is sent to builder...')
