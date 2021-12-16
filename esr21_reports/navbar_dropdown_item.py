from django.urls.base import reverse

from edc_navbar import NavbarItem


class NavBarDropdownItem(NavbarItem):

    template_name = 'esr21_reports/navbar_dropdown_item.html'

    def __init__(self, dropdown=True, dropdown_items={}, **kwargs):
        NavbarItem.__init__(self, **kwargs)
        self.dropdown = dropdown
        for name, url in dropdown_items.items():
            if url == '#':
                continue
            reversed_url = reverse(url)
            dropdown_items.update({name: reversed_url})
        self.dropdown_items = dropdown_items
