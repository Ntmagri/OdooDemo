from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The tag name must be unique."),
    ]

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")
