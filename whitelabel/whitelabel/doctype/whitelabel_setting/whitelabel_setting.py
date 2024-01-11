# -*- coding: utf-8 -*-
# Copyright (c) 2021, Bhavesh Maheshwari and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import cint
from whitelabel.api import get_frappe_version
from frappe.installer import update_site_config

class WhitelabelSetting(Document):
	def validate(self):
		if cint(get_frappe_version()) >= 13:
			if self.whitelabel_app_name:
				frappe.db.set_value("Website Settings","Website Settings","app_name",self.whitelabel_app_name)
			else:
				if "erpnext" in frappe.get_installed_apps():
					frappe.db.set_value("System Settings","System Settings","app_name","ERPNext")
				else:
					frappe.db.set_value("System Settings","System Settings","app_name","Frappe")

		if frappe.db.exists("DocType","Navbar Settings") and self.application_logo:
			frappe.db.set_value("Navbar Settings","Navbar Settings","app_logo",self.application_logo)
			frappe.db.set_value("Website Settings","Website Settings","app_logo",self.application_logo)
			self.app_logo_set = 1
			update_site_config("app_logo_url",self.application_logo)
			frappe.clear_cache()
		if self.app_logo_set and not self.application_logo:
			frappe.db.set_value("Navbar Settings","Navbar Settings","app_logo","")
			frappe.db.set_value("Website Settings","Website Settings","app_logo",self.application_logo)
			self.app_logo_set = 0
			update_site_config("app_logo_url",False)
			frappe.clear_cache()