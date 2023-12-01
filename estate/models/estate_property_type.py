from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique."),
    ]


    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence", default=10) #This will allow the user to drag the options property type to any position he wants, so 1 item we wants home...
    #=====================================================
    # RELATION BETWEEN OTHER MODELS
    #=====================================================
        # 1) We are connecting this and estate.property model.
        # 2) We are connecting as well with the property_type_id field, which it's that connect with this one.
        # 3) With that, whenever we add the fields in the XML file form, we will be able to have the whole form of estate.property in property type form.
        # 4) Then, we will create a new property and the informations that we put in the view to be extract from will pop up in the notebook tree property_type.
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")

    offer_count = fields.Integer(string="Offers Count")
    offer_ids = fields.Many2many('estate.property.offer', string="Offers")
    
    
    #=====================================================
    # ACTION METHOD
    #=====================================================
        #It needs a action to make the button works.
    def action_view_offers(self):
        res = self.env.ref("estate.test_property_offer").read()[0] #test_property_offer is the ID of the estate_property_offer_views.xml, if we do not include it, it will not work
        res["domain"] = [("id", "in", self.offer_ids.id)]
        return res



