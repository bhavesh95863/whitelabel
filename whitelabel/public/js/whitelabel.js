$(window).on('load', function() {
    frappe.after_ajax(function () {
        if (frappe.boot.app_logo_details.logo_width) {
            $('.app-logo').css('width',frappe.boot.app_logo_details.logo_width+'px');
        }
        if (frappe.boot.app_logo_details.logo_width) {
            $('.app-logo').css('width',frappe.boot.app_logo_details.logo_width+'px');
        }
        $('.navbar').css('background-color',frappe.boot.app_logo_details.navbar_background_color)
    })
})