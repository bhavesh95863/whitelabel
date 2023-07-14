from __future__ import unicode_literals
import frappe
import json
from frappe.utils import floor, flt, today, cint
from frappe import _
def get_room(customer_id):    
    try:
        print("customer_id",customer_id)
        site = frappe.db.get_list('SaaS sites', filters={'cus_id': customer_id},fields=["site_name"],ignore_permissions=True)[0]["site_name"]
        return f"{site}:website"
    except Exception as e:
        print("error",e)

def whitelabel_patch():
    # delete erpnext welcome page
    frappe.delete_doc_if_exists("Page", "welcome-to-erpnext", force=1)
    # update Welcome Blog Post
    if frappe.db.exists("Blog Post", "Welcome"):
        frappe.db.set_value("Blog Post", "Welcome", "content", "")
    update_field_label()    


def update_field_label():
    """Update label of section break in employee doctype"""
    frappe.db.sql(
        """Update `tabDocField` set label='ERP' where fieldname='erpnext_user' and parent='Employee'"""
    )


def get_frappe_version():
    return frappe.db.get_value(
        "Installed Application", {"app_name": "frappe"}, "app_version"
    ).split(".")[0]


def update_onboard_details():
    update_onboard_module()
    update_onborad_steps()


def update_onboard_module():
    onboard_module_details = frappe.get_all(
        "Module Onboarding", filters={}, fields=["name"]
    )
    for row in onboard_module_details:
        doc = frappe.get_doc("Module Onboarding", row.name)
        doc.documentation_url = ""
        doc.flags.ignore_mandatory = True
        doc.save(ignore_permissions=True)


def update_onborad_steps():
    onboard_steps_details = frappe.get_all(
        "Onboarding Step", filters={}, fields=["name"]
    )
    for row in onboard_steps_details:
        doc = frappe.get_doc("Onboarding Step", row.name)
        doc.intro_video_url = ""
        doc.description = ""
        doc.flags.ignore_mandatory = True
        doc.save(ignore_permissions=True)


def boot_session(bootinfo):
    """boot session - send website info if guest"""
    if frappe.session["user"] != "Guest":
        bootinfo.whitelabel_setting = frappe.get_doc(
            "Whitelabel Setting", "Whitelabel Setting"
        )
    bootinfo.app_name = frappe.get_hooks("brand_name")[-1]
    


@frappe.whitelist()
def ignore_update_popup():
    if not frappe.db.get_single_value("Whitelabel Setting", "disable_new_update_popup"):
        show_update_popup_update()


@frappe.whitelist()
def show_update_popup_update():
    cache = frappe.cache()
    user = frappe.session.user
    update_info = cache.get_value("update-info")
    if not update_info:
        return

    updates = json.loads(update_info)

    # Check if user is int the set of users to send update message to
    update_message = ""
    if cache.sismember("update-user-set", user):
        for update_type in updates:
            release_links = ""
            for app in updates[update_type]:
                app = frappe._dict(app)
                release_links += "<b>{title}</b>: <a href='https://github.com/{org_name}/{app_name}/releases/tag/v{available_version}'>v{available_version}</a><br>".format(
                    available_version=app.available_version,
                    org_name=app.org_name,
                    app_name=app.app_name,
                    title=app.title,
                )
            if release_links:
                message = _(
                    "New {} releases for the following apps are available"
                ).format(_(update_type))
                update_message += "<div class='new-version-log'>{0}<div class='new-version-links'>{1}</div></div>".format(
                    message, release_links
                )

    if update_message:
        frappe.msgprint(
            update_message, title=_("New updates are available"), indicator="green"
        )
        cache.srem("update-user-set", user)



import stripe
import frappe
import datetime
# price IDS
price_ids ={
    "ONEHASH_PRO_YEAR":"price_1NRWD6EwPMdYWOILkemBhQHu"
}
subscription_key = {
    "MAIN":"MAIN",
    "ADDITIONAL_STORAGE":"ADDITIONAL_STORAGE",
}
class StripeSubscriptionManager():
    def __init__(self,country=""):
        stripe.api_key = frappe.conf.STRIPE_SECRET_KEY
        self.endpoint_secret = frappe.conf.STRIPE_ENDPOINT_SECRET
        if country:
            self.region = country
        else:
            self.region = frappe.conf.country or "US"
        if(self.region == "IN"):
            stripe.api_key = frappe.conf.STRIPE_SECRET_KEY_IN
            self.endpoint_secret = frappe.conf.STRIPE_ENDPOINT_SECRET_IN
        self.plan_to_product_id = {
            "25GB":"prod_OE6JgL1X5whRBm",
            "ONEHASH_PRO":"prod_ODy9z0LH7AwXD6",
            "ONEHASH_PLUS":"prod_OE6JgL1X5whRBm",
            "ONEHASH_STARTER":"prod_OF3nxhfb3JpKeR"
        }
        self.onehas_subscription_product_ids = ["prod_OE6JgL1X5whRBm","prod_ODy9z0LH7AwXD6","prod_OF3nxhfb3JpKeR"]
        self.trial_price_id = "price_1NTKzREwPMdYWOILklDKorqG"
        self.trial_product = "ONEHASH_PRO"
    
        if(self.region == "IN"):
            self.plan_to_product_id = {
            "25GB":"prod_OE6JgL1X5whRBm",
            "ONEHASH_PRO":"prod_OFowmBYUz738j9",
            "ONEHASH_PLUS":"prod_OFovQrq6UPfouo",
            "ONEHASH_STARTER":"prod_OFotftDB5owt2r"
            }
            self.trial_price_id = "price_1NTJIZCwmuPVDwVyGNdlnJsl"
            self.onehas_subscription_product_ids = ["prod_OFovQrq6UPfouo","prod_OFowmBYUz738j9","prod_OFotftDB5owt2r"]
        
    def getSession(self,session_id,expand=[]):
        return stripe.checkout.Session.retrieve(session_id,expand=expand)
    def create_customer(self, site_name,email,fname,lname,phone):
        return stripe.Customer.create(email=email,metadata={"full name": fname + " " + lname},name = site_name,phone = phone)
    def get_current_onehash_price(self,customer_id):
        subscription = self.get_onehash_subscription(frappe.conf.customer_id)
        print(subscription)
        return subscription["plan"]["id"]
    def end_trial(self,customer_id):
        # cancel the subcription of customer which is on trial
        subscriptions = stripe.Subscription.list(customer=customer_id)
        for subscription in subscriptions:
            if subscription["status"] == "trialing":
                stripe.Subscription.delete(subscription["id"])
    def start_free_trial_of_site(self,customer_id):
        return stripe.Subscription.create(customer=customer_id,items=[{"price": self.trial_price_id}],payment_settings={"save_default_payment_method": "on_subscription"},trial_settings={"end_behavior": {"missing_payment_method": "pause"}},metadata={"plan":"ONEHASH_PRO"},trial_period_days=14)
    def has_valid_site_subscription(self,cus_id):

        return self.get_onehash_subscription(cus_id) != "NONE"
    def create_new_purchase_session(self,customer_id,price_id,subdomain):
        success_url = "http://" + subdomain + "."+(frappe.conf.domain if frappe.conf.domain !="localhost" else frappe.conf.domain+":8000") +"/pricing?payment_success=True"
        session = stripe.checkout.Session.create(
            success_url=success_url,
            mode="subscription",
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                    
                }],
            client_reference_id = subdomain,
            customer = customer_id,
            metadata={"del_trial":True},
        )
        return session.url

    
   # def create_checkout_session(self,customer_id,plan,success_url,cancel_url):
    def get_customer_details(self,customer_id):
        customer = stripe.Customer.retrieve(customer_id,expand=["subscriptions"])
        return customer
    def get_current_onehash_product_id(self,customer_id):
        customer = self.get_customer_details(customer_id)
        product_id = None
        for subscription in customer["subscriptions"]["data"]:
            if subscription["status"] in ["active","trialing"] and subscription["plan"]["product"] and subscription["plan"]["product"] in self.onehas_subscription_product_ids:
                product_id = subscription["plan"]["product"]
                break
        return product_id
    def get_current_onehash_product(self,customer_id):
        subscriptions = stripe.Subscription.list(customer=customer_id)
        product = None
        for subscription in subscriptions["data"]:
            if subscription["status"] in ["active","trialing"] and subscription["plan"]["product"] and subscription["plan"]["product"] in self.onehas_subscription_product_ids:
                product = subscription["plan"]["product"]
                break
        return stripe.Product.retrieve(product)
        
    def has_valid_subscription_v2(self,customer_id,plan):
        # if plan == "ONEHASH" 
        # check if the customer has any product in subscription which product id starts with ONEHASH
        # if yes then return true else false
        customer = self.get_customer_details(customer_id)
        if "subscriptions" not in customer:
            return False
        if plan == "ONEHASH":
            for subscription in customer["subscriptions"]["data"]:
                if subscription["status"] in ["active","trialing"] and subscription["plan"]["product"] and subscription["plan"]["product"] in self.onehas_subscription_product_ids:
                    return True
            return False
        else :
            for subscription in customer["subscriptions"]["data"]:
                if subscription["status"] in ["active","trialing"] and subscription["plan"]["product"] and subscription["plan"]["product"] == self.plan_to_product_id[plan]:
                    return True
            return False
    def get_onehash_subscription(self,customer_id):
        subscriptions = stripe.Subscription.list(customer=customer_id)
        for subscription in subscriptions["data"]:
            if subscription["status"] in ["active","trialing"] and subscription["plan"]["product"] and subscription["plan"]["product"] in self.onehas_subscription_product_ids:
                return subscription
        return "NONE"
    def cancel_onehash_subscription(self,customer_id):
        current_sub = self.get_onehash_subscription(customer_id)
        if current_sub != "NONE":
            stripe.Subscription.delete(current_sub["id"])
        
    def upgrade_subscription(self,customer_id,new_price_id,subdomain):
        # this will upgrade the subscription to new price id and try to charge the customer immediately
        subscription = self.get_onehash_subscription(customer_id)
        # check is customer has any pending invoice if yes then return "PENDING_INVOICE"
        # check is customer has any pending update if yes then return "PENDING_UPDATE"
        # check is customer has any unpaid invoice if yes then return "UNPAID_INVOICE"
        # check is customer has no payment method if yes then return "NO_PAYMENT_METHOD"
        customer = self.get_customer_details(customer_id)
        invoices = stripe.Invoice.list(customer=customer_id)
        for invoice in invoices['data']:
            if invoice["status"] != "paid" and invoice["status"] != "void":
                return "PENDING_INVOICE"
        customer_payment_methods = stripe.PaymentMethod.list(customer=customer_id,type="card")
        
        if  len(customer_payment_methods["data"]) == 0 :
            return "NO_PAYMENT_METHOD"
        # remove any pending update
        if  customer["subscriptions"]["data"][0]["pending_update"] :
            return "PENDING_UPDATE"
       
        try:
            print("updating subscription..")
            response = stripe.Subscription.modify(
                    subscription.id,
                    payment_behavior='pending_if_incomplete',
                    proration_behavior='always_invoice',
                    items=[{
                        'id': subscription['items']['data'][0].id,
                        'price': new_price_id,
                    }],
                   
                    )
            
        except Exception as e:
            print(e)
            return "TECHNICAL_ERROR"
       # print("response",response)
        if("pending_update" in response and response["pending_update"] ):
            # error in payment
            print("there are updates pending,might require payment action")
            return "PENDING_UPDATE"
           
        else :
            # success
            return "SUCCESS"
    def handle_payment_intent_failed(self,event):
        customer_id = event["data"]["object"]["customer"]
        print("hi")
        frappe.publish_realtime("payment_failed",room=get_room(customer_id))
    def handle_payment_intent_action_required(self,event):
        payment_intent_id = event["data"]["object"]["payment_intent"]
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        client_secret = payment_intent["client_secret"]
        frappe.publish_realtime("requires_payment_action",message={"client_secret":client_secret},room=get_room(event["data"]["object"]["customer"]))
            # after 3 minute check if payment is done , if not dome then void this transaction
        from threading import Timer
        invoice_id = event["data"]["object"]["id"]
        def void_payment(invoice_id):
            print("voidng invoice")
            payment_intent = stripe.PaymentIntent.retrieve(invoice_id)
            if payment_intent["status"] == "requires_payment_action":
                stripe.Invoice.void_invoice(invoice_id)
        t = Timer(30*60, void_payment,(invoice_id))
        t.start()    
        
    def handle_checkout_session_completed(self,event):
        customer_id = event["data"]["object"]["customer"]
        session_metadata = event["data"]["object"]["metadata"]
        customer_id  = event["data"]["object"]["customer"]
        print(session_metadata)
        if "del_trial" in session_metadata and session_metadata["del_trial"] == "True":
            print("ending trial")
            self.end_trial(customer_id)
    
    def handle_invoice_paid(self,event):
        customer_id = event["data"]["object"]["customer"]
        sub_id = event["data"]["object"]["subscription"]
        subscription = stripe.Subscription.retrieve(sub_id,expand=["latest_invoice"])
        product_id = subscription["items"]["data"][0]["price"]["product"]
        price_id = subscription["items"]["data"][0]["price"]["id"]
        # invoice paid
        print("INVOICE PAID>>>>>>")
        if product_id in self.onehas_subscription_product_ids :
            if price_id != frappe.conf.price_id :
                # end tria
                # fetch the site_name from the database - saved payment intent id
                site_name = frappe.get_list("SaaS sites",filters={"cus_id":customer_id},fields=["site_name"],ignore_permissions=True)[0]["site_name"]
                print("updating onehash subscription for site",site_name)
                fulfilOneHashUpdate(self.onehas_subscription_product_ids,product_id,price_id,site_name)
                # call payment success on that site
                frappe.publish_realtime("payment_success",room=get_room(customer_id))
    
        


    
    
def fulfilOneHashUpdate(pids,product_id,price_id,site_name):
    # pass the checkout session 
    if product_id in pids:
            # handle onehash subscription
        product = stripe.Product.retrieve(product_id)
        user_limit = 10
        plan_name = ""
        if product.name == "OneHash Pro":
                user_limit = 100000
                plan_name = "ONEHASH_PRO"   
        elif product.name == "OneHash Starter":
                user_limit = 10
                plan_name = "ONEHASH_STARTER"
        else :
                user_limit = 30
                plan_name = "ONEHASH_PLUS"
        command_to_set_limit = "bench --site {site_name} set-config  max_users {user_limit}".format(site_name=site_name,user_limit=user_limit)
        command_to_set_plan = "bench --site {site_name} set-config  plan {plan}".format(site_name=site_name,plan=plan_name)
        command_to_set_price_id = "bench --site {site_name} set-config  price_id {price_id}".format(site_name=site_name,price_id=price_id)
        frappe.utils.execute_in_shell(command_to_set_limit)
        frappe.utils.execute_in_shell(command_to_set_plan)
        frappe.utils.execute_in_shell(command_to_set_price_id)
        
def test_onehash_price():
    stripe_manager = StripeSubscriptionManager()
    print(stripe_manager.get_current_onehash_price(frappe.conf.customer_id))
    