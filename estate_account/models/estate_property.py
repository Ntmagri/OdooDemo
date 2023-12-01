from odoo import models

class InheritedModel(models.Model):
    _inherit = "estate.property"


# TO CREATE AN INVOICE
    # WE NEED 
        # partner_id: the customer
        # move_type: it has several possible values, fields.Selection
        # journal_id: the accounting journal

    def action_sold_offer(self): #This will override the action_sold_offer from the other module. This one below in the code. 
        res = super().action_sold_offer()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit = 1)

        for line in self:
            self.env["account.move"].create( # Account.movie is the override(substitution) of the action_sold_offer method.
                {
                    "partner_id": line.buyer_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    
                }
            )

        return res


# TO CREATE AN INVOICE LINE, we need to link it to an invoce as well.
    # WE NEED
        # name: a description of the line
        # quantity
        # price_unit



# def action_sold_offer(self):
#         if "canceled" in self.mapped("state"):
#             raise UserError("Cancelled offer and It can not be sold.")
#         return self.write({"state": "sold"}) 