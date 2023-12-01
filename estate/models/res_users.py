from odoo import fields, models

class ResUsers(models.Model):

    _inherit = "res.users"

    #===============================
    # Relation with other model
    #===============================
        #Here we are connecting with the estate_property, and with the salesman_id
        #The domain here is to show/list only the vailable properties.
        #With all these fields we will be able to display the list of properties linked to a salesperson directlyin the settings...
    property_ids = fields.One2many("estate.property", "salesman_id", string="Properties", domain=[("state", "in", ["new", "offer_received"])])