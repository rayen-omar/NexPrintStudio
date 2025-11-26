# -*- coding: utf-8 -*-
"""
Script pour créer manuellement les produits du catalogue
À exécuter dans la console Odoo ou via un cron
"""

def create_all_products(env):
    """Crée tous les produits du catalogue"""
    from odoo.addons.NXPSTudion.hooks import create_catalogue_products
    
    print("Début de la création des produits...")
    create_catalogue_products(env)
    print("Création terminée!")
    
    # Vérifier les produits créés
    total_products = env['product.template'].search_count([
        ('website_published', '=', True)
    ])
    print(f"Total produits publiés: {total_products}")
    
    # Vérifier par catégorie
    categories_info = env['nexprint.catalogue.data'].get_categories_info()
    for cat_key, cat_info in categories_info.items():
        category = env['product.category'].search([
            ('name', '=', cat_info['name'])
        ], limit=1)
        if category:
            count = env['product.template'].search_count([
                ('categ_id', '=', category.id),
                ('website_published', '=', True)
            ])
            print(f"{cat_info['name']}: {count} produits")


