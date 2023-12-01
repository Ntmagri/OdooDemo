from odoo import api, fields, models
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc" #This will make the properties appear as the date they were created
    #=====================================================
    # SQL CONSTRAINTS
    #=====================================================
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The offer price must be positive"),
    ]
    
    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Post Code")
    date_availability = fields.Datetime("Property Availability", copy=False, default=date.today() + relativedelta(months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
        ('west', 'West')],
        help="Type is used to separate North, South, East and West",
    )
    is_active = fields.Boolean(string="Active", default=True) 
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True, copy=False, default='new'
    )

   
   
    #=====================================================
    # RELATION BETWEEN OTHER MODELS
    #=====================================================

    property_type_id = fields.Many2one('estate.property.type', string="Property Type") #This is how I relate the other model to this one.
    salesman_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user) #whenever is a person, like contact, we declares as a res.partner, not the model name as property_type_id.
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    property_tag_ids = fields.Many2many('estate.property.tag', string="Property Tag") #Don't forget to use ids on Many2many fields.
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Property Offer")

    #=====================================================
    #COMPUTING
    #=====================================================
    #The _ before the compute and onchange, meaning that it's a private method, when there is not it's a public where the user can call it. 

        #Here it's computing the total area between living area and garden area
    total_area = fields.Integer("Total Area", compute="_compute_total_area") 
    #to be able to use Computed fields we need to import api.
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area
    
        #Here Computing the best price (Offer)
    best_price = fields.Integer("Best Offer", compute="_compute_best_price")
    @api.depends('offer_ids.price') #Here is relating to the offer_ids relational field and price is the field created in that model.
    def _compute_best_price(self):
        for line in self:
            line.best_price = max(line.offer_ids.mapped("price")) if line.offer_ids else 0

        #Onchange is like, whenever you activate something an information from another field changes as well. 
        #So like, if I activate the car field, it fill out the gas price for example.
        #DO NOT USE ONECHANGE FOR LOGIC
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden: #Here if garden is activated then garden area = 10 and garden orientation = north.
            self.garden_area = 10
            self.garden_orientation = "north"
            return {'warning': {'title': "Warning", 'message': "You have activated Garden field.", 'type': 'notification'},}
        else:
            self.garden_area = 0
            self.garden_orientation = False

    
    #=====================================================
    # BUTTONS
    #=====================================================
    #     #For this part of buttons we need to import from odoo.exceptions import UserError, ValidationError
    def action_sold_offer(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Cancelled offer and It can not be sold.")
        return self.write({"state": "sold"}) #This will change the state for sold or canceled.

    def action_cancel_offer(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold property and It can not be cancelled.")
        return self.write({"state": "canceled"})


    #====================================================================
    # PYTHON CONSTRAINTS, need to import ValidationError, and Odoo Tools
    #====================================================================
    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for line in self:
            if (
                not float_is_zero(line.selling_price, precision_rounding=0.01) #Checking if selling price is zero or not.
                and float_compare(line.selling_price, line.expected_price * 90 / 100, precision_rounding=0.01) < 0 #Here is comparing the selling with the expected using the math.
            ):
                raise ValidationError(
                    "The selling price must be 90% or greater of the expected price. " +
                    "Therefore, he must increase his offer or you must reduce the expected price."
                )


    #========================================================================================================
    #CRUD METHOD
            # Always call super(), Ex: return super().create(vals)
            # Always return data consistent with the parent method. 
    #========================================================================================================
    # Here will be the unlink model. Where will prevent deletion of a property if its state is not new or canceled.
    def unlink(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise UserError("Can not be deleted, only new and canceled can be.")
        return super().unlink()

