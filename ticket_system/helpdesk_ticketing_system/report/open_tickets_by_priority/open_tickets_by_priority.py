# Copyright (c) 2025, DharanidharanS and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    # Base condition
    conditions = "WHERE docstatus < 2"

    if filters.get("status"):
        conditions += " AND status = %(status)s"
    else:
        # Default to 'Open' if no status selected
        conditions += " AND status = 'Open'"

    if filters.get("priority"):
        conditions += " AND priority = %(priority)s"
    if filters.get("from_date"):
        conditions += " AND creation >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND creation <= %(to_date)s"

    columns = [
        {"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Ticket Count", "fieldname": "count", "fieldtype": "Int", "width": 100}
    ]

    data = frappe.db.sql(f"""
        SELECT priority, status, COUNT(*) AS count
        FROM `tabTicket`
        {conditions}
        GROUP BY priority, status
    """, filters, as_dict=True)

    return columns, data
