"""
Home page for Studio when logged in.
"""
from bok_choy.page_object import PageObject

from common.test.acceptance.pages.studio import BASE_URL


class HomePage(PageObject):
    """
    Home page for Studio when logged in.
    """

    url = BASE_URL + "/home"

    def is_browser_on_page(self):
        return all([self.q(css='.page-header').visible,
                    'Studio Home' == self.q(css='.page-header')[0].text])
