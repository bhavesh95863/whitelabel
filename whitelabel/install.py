import frappe
import re

def after_install():
    ob_steps = frappe.db.get_all("Onboarding Step")
    brand_name = frappe.get_hooks("brand_name")[0]
    t = 0
    for step in ob_steps:
        doc = frappe.get_doc("Onboarding Step", step.name, ["title", "description"])
        if doc.title:
            doc.title = re.sub("ERPNext", brand_name, doc.title)
        if doc.description:
            doc.description = re.sub("ERPNext", brand_name, doc.description)
        doc.save(ignore_permissions=True)
        
    # frappe.db.sql(
    #     """Update `tabDocField` set label='OneHash' where fieldname='erpnext_user' and parent='Employee'"""
    # )
    onboard_module_details = frappe.get_all(
        "Module Onboarding", filters={}, fields=["name"]
    )
    for row in onboard_module_details:
        doc = frappe.get_doc("Module Onboarding", row.name)
        doc.title = re.sub("ERPNext", brand_name, doc.title)
        doc.success_message = re.sub("ERPNext", brand_name, doc.success_message)
        doc.documentation_url = ""
        doc.flags.ignore_mandatory = True
        doc.save(ignore_permissions=True)
    
    whitelabel()
    frappe.db.commit()




def whitelabel():
    # set deault otp issuer name
    # sys_setting = frappe.get_single("System Settings")
    # sys_setting.otp_issuer_name = "OneHash"
    # sys_setting.save(ignore_permissions=True)
    # set otp_issuer_name in system settings to OneHash
    frappe.db.set_value("System Settings","System Settings","otp_issuer_name","OneHash" )
    frappe.db.set_value("Website Settings","Website Settings","app_name","OneHash" )
    brand_name = frappe.get_hooks("brand_name")[0]
    frappe.db.set_value("Website Settings","Website Settings","app_name",brand_name )
    frappe.db.set_value("System Settings","System Settings","app_name",brand_name )
   # frappe.db.set_value("Module Def","ERPNext Integrations","module_name","OneHash Integrations" ,update_modified=False)
   # frappe.db.set_value("Module Def","ERPNext Integrations","name","OneHash Integrations" ,update_modified=False)
    frappe.db.commit()
    