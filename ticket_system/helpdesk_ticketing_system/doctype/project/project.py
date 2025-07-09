# Copyright (c) 2025, DharanidharanS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Project(Document):
	pass


# @frappe.whitelist()
# def get_available_developers(doctype, txt, searchfield, start, page_len, filters):
#     txt = txt or ""
#     return frappe.db.sql("""
#         SELECT name, CONCAT(developer_name, ' - ', developer_email)
#         FROM `tabDeveloper`
#         WHERE developer_name LIKE %s
#         LIMIT 20
#     """, [f"%{txt}%"])
