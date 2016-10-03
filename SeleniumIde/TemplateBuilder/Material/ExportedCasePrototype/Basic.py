# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from argparse import RawTextHelpFormatter
import unittest, time, re, inspect, os, os.path, json, argparse


TEST_SUITE_CLASS_NAME = "__template_className__"


class __template_className__(unittest.TestCase):
    def __init__(self, driver, opts):
        super(__template_className__, self).__init__("__template_methodName__")

        self.driver_name = driver
        self.profile = TestProfile(opts['profile'])
        self.wait_time = opts['wait_time']

    def setUp(self):
        self.driver = self._get_web_driver(self.driver_name)
        self.driver.implicitly_wait(30)
        self.base_url = self.profile.param("base_url", "__template_baseURL__")
        self.verificationErrors = []
        self.accept_next_alert = True

    def tearDown(self):
        self.driver.save_screenshot(self._build_screenshot_name())
        self.driver.quit()
        if self._is_successful() and not self.profile.file_exists():
            self.profile.save_profile_file()

        self.assertEqual([], self.verificationErrors)

    def __template_methodName__(self):
        __template_param_getter__ = self.profile.param
        __template_receiver__ = self.driver

    # Footer

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    @staticmethod
    def _get_web_driver(driver_name):
        if driver_name == 'chrome':
            return webdriver.Chrome()
        elif driver_name == 'firefox':
            return webdriver.Firefox()
        elif driver_name == 'ie':
            return webdriver.Ie()
        elif driver_name == 'edge':
            return webdriver.Edge()
        elif driver_name == 'safari':
            return webdriver.Safari()
        else:
            raise ValueError

    def _is_successful(self):
        result = self._resultForDoCleanups
        return len(result.failures) == 0 and len(result.errors) == 0

    def _build_screenshot_name(self):
        png_root = os.getcwd() + os.sep
        local_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        screenshot_id = '_'.join((self.__class__.__name__, self.driver_name, local_time))
        return png_root + screenshot_id + '.png'


class TestProfile:
    def __init__(self, profile_filename):
        self.test_dict = {}
        self.profile_filename = profile_filename

        if self.file_exists():
            self.load_profile_file()

    def param(self, param, default_value):
        if not self.file_exists():
            self.test_dict[param] = default_value
        return self.test_dict[param]

    @staticmethod
    def profile_file_exists_with(filename):
        return os.path.isfile(filename)

    def file_exists(self):
        return self.profile_file_exists_with(filename=self.profile_filename)

    def save_profile_file_with(self, filename):
        with open(filename, 'w') as profile:
            json.dump(self.test_dict, profile)

    def save_profile_file(self):
        self.save_profile_file_with(filename=self.profile_filename)

    def load_profile_file_with(self, filename):
        with open(filename) as profile:
            self.test_dict = json.load(profile)

    def load_profile_file(self):
        self.load_profile_file_with(filename=self.profile_filename)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Python-Based Selenium Web Test Case for ' + TEST_SUITE_CLASS_NAME,
        formatter_class=RawTextHelpFormatter)

    group = parser.add_argument_group('options')
    group.add_argument('-p', '--profile',
                       dest='profile',
                       type=str,
                       default=TEST_SUITE_CLASS_NAME + '_profile.json',
                       help='''determine a file path of test profile;
a default profile will be generated after execution
if this option not specified''')

    group.add_argument('-d', '--driver',
                       dest='web_driver',
                       type=str,
                       required=True,
                       help='''specify a webdriver you would like to test with,
including:
 - chrome:  Google Chrome
 - firefox: Mozilla Firefox
 - ie:      Microsoft Internet Explorer
 - edge:    Microsoft Edge (not tested yet)
 - safari:  Apple Safari (not tested yet)''')

    group.add_argument('-t', '--time-wait',
                       dest='time_in_sec',
                       type=float,
                       default=0,
                       help='''determine the waiting time in seconds (decimal)
between two steps (default: 0)''')

    args = parser.parse_args()
    opts = {
        'profile': args.profile,
        'wait_time': args.time_in_sec
    }

    test_suite_class = eval(TEST_SUITE_CLASS_NAME)
    suite = unittest.TestSuite()
    suite.addTest(test_suite_class(args.web_driver, opts))
    unittest.TextTestRunner().run(suite)
