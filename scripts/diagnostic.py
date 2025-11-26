# -*- coding: utf-8 -*-
"""
Script de diagnostic pour vérifier l'état des produits et catégories
À exécuter dans la console Odoo
"""

def diagnostic_products(env):
    """Diagnostic des produits et catégories"""
    print("=" * 60)
    print("DIAGNOSTIC PRODUITS NEXPRINT STUDIO")
    print("=" * 60)
    
    # Récupérer les informations du catalogue
    catalogue_data_model = env['nexprint.catalogue.data']
    catalogue_data = catalogue_data_model.get_catalogue_data()
    categories_info = catalogue_data_model.get_categories_info()
    
    print("\n1. VÉRIFICATION DES CATÉGORIES:")
    print("-" * 60)
    for cat_key, cat_info in categories_info.items():
        category = env['product.category'].search([
            ('name', '=', cat_info['name'])
        ], limit=1)
        
        if category:
            count = env['product.template'].search_count([
                ('categ_id', '=', category.id),
                ('website_published', '=', True),
                ('sale_ok', '=', True),
            ])
            print(f"✓ {cat_info['name']}: ID={category.id}, Produits={count}")
        else:
            print(f"✗ {cat_info['name']}: CATÉGORIE NON TROUVÉE!")
    
    print("\n2. VÉRIFICATION DES PRODUITS PAR CATÉGORIE:")
    print("-" * 60)
    for cat_key, products in catalogue_data.items():
        cat_info = categories_info.get(cat_key, {})
        category = env['product.category'].search([
            ('name', '=', cat_info.get('name', ''))
        ], limit=1)
        
        if category:
            products_in_db = env['product.template'].search([
                ('categ_id', '=', category.id),
                ('website_published', '=', True),
            ])
            
            print(f"\n{cat_info.get('name', cat_key)}:")
            print(f"  - Produits attendus: {len(products)}")
            print(f"  - Produits en base: {len(products_in_db)}")
            
            # Vérifier chaque produit
            missing_products = []
            for product_data in products:
                existing = env['product.template'].search([
                    ('default_code', '=', product_data['ref'])
                ], limit=1)
                if not existing:
                    missing_products.append(product_data['ref'])
            
            if missing_products:
                print(f"  - Produits manquants: {len(missing_products)}")
                print(f"    {', '.join(missing_products[:5])}{'...' if len(missing_products) > 5 else ''}")
    
    print("\n3. TOTAL PRODUITS PUBLIÉS:")
    print("-" * 60)
    total = env['product.template'].search_count([
        ('website_published', '=', True),
        ('sale_ok', '=', True),
    ])
    print(f"Total: {total} produits")
    
    print("\n" + "=" * 60)


