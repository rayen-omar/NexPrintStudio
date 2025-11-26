# -*- coding: utf-8 -*-

from odoo import api, SUPERUSER_ID

def update_services_page(env):
    """Force la mise à jour de la page Services avec le nouveau template"""
    # Chercher la vue website.services
    view = env['ir.ui.view'].search([
        ('key', '=', 'website.services'),
        ('type', '=', 'qweb')
    ], limit=1)
    
    if view:
        # Récupérer le nouveau template depuis notre module
        new_template = env.ref('NXPSTudion.website_services_nexprint', raise_if_not_found=False)
        if new_template:
            # Mettre à jour le contenu de la vue avec le nouveau template
            view.arch_db = new_template.arch_db
            view._write({'arch_db': new_template.arch_db})
            env.cr.commit()
            # Invalider le cache
            env.registry.clear_cache()


