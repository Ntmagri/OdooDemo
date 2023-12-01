from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be positive"),
    ]

    price = fields.Float("Price")
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    validity = fields.Integer("Validity", default=7)

    #=====================================================
    #RELATION BETWEEN MODELS
    #=====================================================
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property Offer", required=True)
    #This relation is for the start button
    property_type_id = fields.Many2one('property_id.property_type_id', string="Property Type", store=True) #Here an offer will be linked to a property type when it’s created.

    #=====================================================
    # COMPUTING
    #=====================================================
        #Here we are computing the validity date for offers, inverse.
    date_deadline = fields.Date(string="Deadline Date", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    @api.depends('create_date', 'validity') #create_date is where "allows" the user to enter the date and from that will make the calculation of the date.
    def _compute_date_deadline(self):
        for line in self:
            date = line.create_date.date() if line.create_date else fields.Date.today()
            line.date_deadline = date + relativedelta(days=line.validity)
    
    def _inverse_date_deadline(self):
        for line in self:
            date = line.create_date.date() if line.create_date else fields.Date.today()
            line.validity = (line.date_deadline - date).days #here is where we make the inverse. 
            # Here is where we make the validation, if the validity date is different from the deadline date and the date today, it will fix for the right validity day.

    #This is just practicing onchange api.
    # @api.onchange('partner_id')
    # def _onchange_status(self):
    #     if self.partner_id:
    #         self.status = "accepted"
    #     else:
    #         self.status = False

    #=====================================================
    # BUTTONS
    #=====================================================
    def action_accept_offer(self): #here is calling the button in the view
        if "offer_accepted" in self.mapped("property_id.offer_ids.status"):
            raise UserError("Another offer already accepted.")
        self.write({"status": "accepted"}) #here is where will add accepted in the status view.
        return self.mapped("property_id").write(
            {
                "state":"offer_accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id
            }
        )
    
    def action_refuse_offer(self):
        return self.write({"status": "refused"})

    #============================================================
    # CRUD METHOD
    #============================================================
    # Here will a create model, where it will raisean error if the user tries to create an offer with a lower amount than an existing offer.
    @api.model
    def create(self, vals):
        if vals.get("property_id") and vals.get("price"):
            line = self.env["estate.property"].browse(vals["property_id"]) #This property_id is declared inside of the offer_ids field in the estate_property.py
            # here if the offeris higher than existing one.
            if line.offer_ids:
                max_offer = max(line.mapped("offer_ids.price"))
                if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                    raise UserError("The offer needs to be higher than %.2f" % max_offer) #%.2f is a placeholder for floating point number.
            line.state = "offer_received"
        return super().create(vals)
        
