# Copyright (c) 2025, DharanidharanS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Ticket(Document):
    
    def after_insert(self):
         self.set_deadline()
         self.send_confirmation_email()
        
    def before_save(self):
        self.sendmail()
        # self.deadline()
        
    def set_deadline(self):
        self.from_date = frappe.utils.nowdate()
        today = frappe.utils.nowdate()
        summ=0
        if self.priority == "High":
            self.dead_line = frappe.utils.add_days(today, 1)
        if self.priority == "Medium":
            self.dead_line = frappe.utils.add_days(today, 3)
        if self.priority == "Low":
            self.dead_line = frappe.utils.add_days(today, 5)
        self.save()
        
    def send_confirmation_email(self):

        developer_email = self.developer_email
        customer_email = self.client_email
        print("Developer Email:", developer_email)
        print("Customer Email:", customer_email)
        
        if customer_email:
            frappe.sendmail(
                recipients=[customer_email],

                subject=f"Ticket Confirmation - {self.name}",
                message=f"Dear {self.client},\n\nYour ticket has been submitted successfully.\n\nThanks,\nSupport Team"
            )

            frappe.sendmail(
                recipients=[developer_email],
                subject=f"Customer Raised an Ticket - {self.name}",
                message=f"Dear {self.developer},\n\nCustomer has submitted an Ticket.\n\nThanks,\nSupport Team"
            )

            frappe.log_error(frappe.get_traceback(), f"Ticket Sent successfully: {self.name}")
        
        else:
            frappe.log_error("No valid email found to send confirmation for Ticket: " + self.name)

    def sendmail(self):
        developer_email = self.developer_email
        customer_email = self.client_email
        manager = "dharanijeeva463@gmail.com"
        state=self.status
        if state == "In Progress":
            frappe.sendmail(
                recipients=[customer_email],
                subject=f"Ticket Confirmation - {self.name}",
                message=f"Dear {self.client},\n\nYour ticket has been In Progress.\n\nThanks,\nSupport Team"
            )

            frappe.sendmail(
                recipients=[manager],
                subject=f"Customer Raised a Ticket - {self.name}",
                message=f"Dear {manager},\n\n ticket has been In Progress.\n\nThanks,\nSupport Team"
            )
        elif state == "Closed":
            frappe.sendmail(
                recipients=[customer_email],
                subject=f"Ticket Closed - {self.name}",
                message=f"Dear {self.client},\n\nYour ticket has been Completed successfully.\n\nThanks,\nSupport Team"
            )

            frappe.sendmail(
                recipients=[manager],
                subject=f"Ticket Closed - {self.name}",
                message=f"Dear {manager},\n\nThe ticket has been Completed successfully.\n\nThanks,\nSupport Team"
            )
            
    
@frappe.whitelist()
def add_comment_and_notify(ticket, comment_text, role):
    manager = "dharanijeeva463@gmail.com"
    doc = frappe.get_doc("Ticket", ticket)
    if doc.status == "Closed":
        frappe.throw("You cannot comment on a closed ticket.")

    if role == "Client":
        client = doc.get("client_email")
        recipient_email = doc.get("developer_email")
        doc.status = "In Progress"
    else:
        client = doc.get("developer_email")
        recipient_email = doc.get("client_email")
        doc.status = "In Progress"

    timestamp = frappe.utils.now_datetime()
    doc.append("ticket_comments", {
        "comment_text": comment_text,
        "commented_by": client,
        "role": role,
        "timestamp": timestamp
    })

    doc.flags.ignore_validate_update_after_submit = True
    doc.flags.ignore_permissions = True
    doc.flags.ignore_version = True
    doc.save()

    if recipient_email:
        frappe.sendmail(
            recipients=[recipient_email],
            subject=f"New comment on Ticket {ticket}",
            message=comment_text,
            sender="support@yourcompany.com"  
        )

@frappe.whitelist()
def get_user_role_for_ticket():
    user = frappe.session.user

    developer = frappe.get_value("Developer", {"user_id": user}, "name")
    if developer:
        return "Developer"

    client = frappe.get_value("Client", {"user_id": user}, "name")
    if client:
        return "Client"
    
    return "Manager"

def deadline(self):
        frappe.log_error("Deadline Check", "Checking deadline for ticket")
        print("Checking deadline for ticket")
        manager="dharanijeeva463@gmail.com"
        from_date = self.get("from_date")
        deadline = self.get("deadline")

        if not from_date or not deadline:
            return

        if isinstance(from_date, str):
            from_date = frappe.utils.get_datetime(from_date)
        if isinstance(deadline, str):
            deadline = frappe.utils.get_datetime(deadline)

        if from_date > deadline:
            self.status = "Failed"
            frappe.sendmail(
                recipients=[manager],
                subject=f"Deadline Error for Ticket {self.name}",
                message=f"Dear Manager,<br><br>The From Date for Ticket {self.name} is after the Deadline.<br><br>Thanks,<br>Support Team"
            )
            frappe.sendmail(
                recipients=[self.client_email],
                subject=f"Deadline Error for Ticket {self.name}",
                message=f"Dear {self.client},<br><br>The From Date for your Ticket {self.name} is after the Deadline.<br><br>Thanks,<br>Support Team"
            )
        if self.docstatus == 1 and self.status == "Failed":
            self.cancel()
