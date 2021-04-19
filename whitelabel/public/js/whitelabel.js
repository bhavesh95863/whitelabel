$(window).on('load', function() {
    frappe.after_ajax(function () {
        if (frappe.boot.app_logo_details.logo_width) {
            $('.app-logo').css('width',frappe.boot.app_logo_details.logo_width+'px');
        }
        if (frappe.boot.app_logo_details.logo_width) {
            $('.app-logo').css('width',frappe.boot.app_logo_details.logo_width+'px');
        }
    })
})