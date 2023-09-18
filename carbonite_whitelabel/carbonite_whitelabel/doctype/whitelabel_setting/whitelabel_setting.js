// Copyright (c) 2021, Bhavesh Maheshwari and contributors
// For license information, please see license.txt

frappe.ui.form.on('carbonite_whitelabel Setting', {
	after_save: function(frm) {
		frappe.ui.toolbar.clear_cache();
	}
});
