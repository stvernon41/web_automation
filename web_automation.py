import abc
import os
import subprocess
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


PHONE_NUMBER = '15551234567'
APPLE_ID = 'XXXXX@gmail.com'


class WebsiteChecker(object):

    def __init__(self, sites):
        self._sites = sites

    def run(self):
        driver = webdriver.Safari()
        try:
            site = self._wait_for_elem_enable(driver)
            msg = '%s Available! %s' % (site.name, site.url)
            self._notify(msg)
        except KeyboardInterrupt:
            pass
        except:
            traceback.print_exc()
            self._notify('Script Error!')
        finally:
            driver.close()

    def _wait_for_elem_enable(self, driver):
        while True:
            for site in self._sites:
                driver.get(site.url)
                if site.is_available(driver):
                    return site

                time.sleep(3)

    def _notify(self, msg):
        self._send_macos_notification(msg)
        self._send_imessage(msg)

    def _send_macos_notification(self, msg):
        os.system(f'osascript -e \'display notification "{msg}"\'')

    def _send_imessage(self, msg):
        cmd = f'osascript -e \'tell application "Messages" to send "{msg}" to buddy "{PHONE_NUMBER}" of service "{APPLE_ID}"\''
        subprocess.call(cmd, shell=True)


class Site(object, metaclass=abc.ABCMeta):
    url = None
    name = None
    available_elem_class_name = None
    unavailable_elem_class_name = None

    def is_available(self, driver):
        if self.available_elem_class_name:
            try:
                elem = driver.find_element_by_class_name(self.available_elem_class_name)
                return elem.is_enabled()
            except NoSuchElementException:
                return False
        elif self.unavailable_elem_class_name:
            try:
                elem = driver.find_element_by_class_name(self.unavailable_elem_class_name)
                return not elem.is_enabled()
            except NoSuchElementException:
                return True
        else:
            raise Exception('Inproperly configured.  Need DOM elem class_name to search for')


class BowflexDumbbells(Site):
    url = "https://www.bowflex.com/selecttech/1090/710000.html"
    name = 'Bowflex Dumbbells'
    available_elem_class_name = "add-to-cart"


class PowerblockDumbbels(Site):
    url = 'https://powerblock.com/product/pro-series-expandable/'
    name = 'Powerblock Dumbbells'
    unavailable_elem_class_name = 'bundle_unavailable'


class RougeBench(Site):
    url = "https://www.roguefitness.com/rogue-adjustable-bench-2-0"
    name = 'Rouge Bench'
    available_elem_class_name = "btn-add-to-cart"


class RougeElitePowerBlocks(Site):
    url = "https://www.roguefitness.com/powerblock-series-elite-exp-dumbbells"
    name = 'Rouge Elite Power Blocks'
    available_elem_class_name = "btn-add-to-cart"


class RougePowerBlocks(Site):
    url = "https://www.roguefitness.com/powerblock-series-exp-dumbbells"
    name = 'Rouge Power Blocks'
    available_elem_class_name = "btn-add-to-cart"


if __name__ == '__main__':
    WebsiteChecker(
        [
            BowflexDumbbells(),
            PowerblockDumbbels(),
            RougePowerBlocks(),
            RougeElitePowerBlocks(),
            RougeBench()
        ]
    ).run()
    