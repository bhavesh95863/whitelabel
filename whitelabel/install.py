import frappe
import re

def after_install():
    ob_steps = frappe.db.get_all("Onboarding Step")
    brand_name = frappe.get_hooks("brand_name")[0]
    print(brand_name)
    t = 0
    for step in ob_steps:
        doc = frappe.get_doc("Onboarding Step", step.name, ["title", "description"])
        if doc.title:
            doc.title = re.sub("ERPNext", brand_name, doc.title)
        if doc.description:
            doc.description = re.sub("ERPNext", brand_name, doc.description)
        doc.save(ignore_permissions=True)
        if t < 4:
            print(doc.title, doc.description)
        t += 1
    frappe.db.sql(
        """Update `tabDocField` set label='OneHash' where fieldname='erpnext_user' and parent='Employee'"""
    )
    onboard_module_details = frappe.get_all(
        "Module Onboarding", filters={}, fields=["name"]
    )
    for row in onboard_module_details:
        doc = frappe.get_doc("Module Onboarding", row.name)
        doc.title = re.sub("ERPNext", brand_name, doc.title)
        print(doc.as_dict())
        doc.success_message = re.sub("ERPNext", brand_name, doc.success_message)
        doc.documentation_url = ""
        doc.flags.ignore_mandatory = True
        doc.save(ignore_permissions=True)
    
    whitelabel()
    frappe.db.commit()




def whitelabel():
    # set deault otp issuer name
    frappe.db.set_value("System Settings","System Settings","otp_issuer_name","OneHash")
    # set login page app name
    frappe.db.set_value("Website Settings","Website Settings","app_name","OneHash" )
    brand_name = frappe.get_hooks("brand_name")[0]
    frappe.db.set_value("Website Settings","Website Settings","app_name",brand_name )
    frappe.db.set_value("System Settings","System Settings","app_name",brand_name )
    
    