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
    frappe.db.commit()
