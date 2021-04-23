$(window).on('load', function() {
    frappe.after_ajax(function () {
        if (frappe.boot.app_logo_details.logo_width) {
            $('.app-logo').css('width',frappe.boot.app_logo_details.logo_width+'px');
        }
        if (frappe.boot.app_logo_details.logo_height) {
            $('.app-logo').css('height',frappe.boot.app_logo_details.logo_height+'px');
        }
        $('.navbar').css('background-color',frappe.boot.app_logo_details.navbar_background_color)
        $(`<span style=${frappe.boot.app_logo_details.custom_navbar_title_style.replace('\n','')} class="hidden-xs hidden-sm">${frappe.boot.app_logo_details.custom_navbar_title}</span>`).insertAfter("#navbar-breadcrumbs")
    })
})
