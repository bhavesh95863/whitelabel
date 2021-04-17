from __future__ import unicode_literals
import frappe
import json
from frappe.utils import floor, flt, today, cint

def whitelabel_patch():
	#delete erpnext welcome page 
	frappe.delete_doc_if_exists('Page', 'welcome-to-erpnext', force=1)
	#update Welcome Blog Post
	if frappe.db.exists("Blog Post", "Welcome"):
		frappe.db.set_value("Blog Post","Welcome","content","")