// Copyright (c) 2025, DharanidharanS and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Ticket", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Ticket", {
  refresh(frm) {
    frm.add_custom_button("Add Comment", () => {
      frappe.prompt([
        {
          label: "Comment",
          fieldname: "comment_text",
          fieldtype: "Text Editor",
          reqd: 1
        },
        {
          label: "Role",
          fieldname: "role",
          fieldtype: "Select",
          options: ["Client", "Developer"],
          reqd: 1
        }
      ], (values) => {
        frappe.call({
          method: "ticket_system.helpdesk_ticketing_system.doctype.ticket.ticket.add_comment_and_notify",
          args: {
            ticket: frm.doc.name,
            comment_text: values.comment_text,
            role: values.role
          },
          callback: () => {
            frappe.msgprint("Comment added and emailed.");
            frm.reload_doc();
          }
        });
      }, "Post a Comment");
    });
  }
});
frappe.ui.form.on("Ticket", {
  refresh: function(frm) {
    // Only show if status is not already Completed
    if (frm.doc.status !== "Closed") {
      frm.add_custom_button("Mark as Completed", function () {
        frappe.call({
          method: "frappe.client.set_value",
          args: {
            doctype: "Ticket",
            name: frm.doc.name,
            fieldname: "status",
            value: "Closed"
          },
          callback: function() {
            //frappe.msgprint("Ticket marked as Completed");
            frm.reload_doc();
          }
        });
      }, __("Actions"));
    }
  }
});
