# -*- coding: utf-8 -*-

def post_init_hook(cr, registry):
    """Hook appelé après l'installation du module pour forcer la mise à jour de la page Services"""
    from odoo import api, SUPERUSER_ID
    
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # 1. SUPPRIMER toutes les vues website.services existantes (créées dynamiquement)
    views = env['ir.ui.view'].search([
        ('key', '=', 'website.services'),
        ('type', '=', 'qweb')
    ])
    
    if views:
        views.unlink()
        cr.commit()
    
    # 2. SUPPRIMER la page website.page avec URL /our-services ou /services
    pages = env['website.page'].search([
        '|',
        ('url', '=', '/our-services'),
        ('url', '=', '/services')
    ])
    
    if pages:
        pages.unlink()
        cr.commit()
    
    # 3. SUPPRIMER aussi les vues liées à our_services
    our_services_views = env['ir.ui.view'].search([
        ('key', '=', 'website.our_services'),
        ('type', '=', 'qweb')
    ])
    
    if our_services_views:
        our_services_views.unlink()
        cr.commit()
    
    # 4. SUPPRIMER la page About Us si elle existe (toutes les variantes possibles)
    about_pages = env['website.page'].search([
        '|', '|', '|', '|',
        ('url', '=', '/about-us'),
        ('url', '=', '/aboutus'),
        ('url', '=', '/about'),
        ('url', '=', '/about-us/'),
        ('url', 'ilike', '%about%')
    ])
    
    if about_pages:
        about_pages.unlink()
        cr.commit()
    
    # 5. SUPPRIMER aussi les vues liées à about us
    about_views = env['ir.ui.view'].search([
        '|',
        ('key', 'ilike', '%about%'),
        ('name', 'ilike', '%about%')
    ])
    
    # Filtrer pour ne garder que celles liées à website
    about_views = about_views.filtered(lambda v: 'website' in (v.key or '') or 'website' in (v.name or ''))
    
    if about_views:
        about_views.unlink()
        cr.commit()
    
    # 6. SUPPRIMER la page Contact si elle existe
    contact_pages = env['website.page'].search([
        '|', '|', '|',
        ('url', '=', '/contactus'),
        ('url', '=', '/contact-us'),
        ('url', '=', '/contact'),
        ('url', 'ilike', '%contact%')
    ])
    
    if contact_pages:
        contact_pages.unlink()
        cr.commit()
    
    # 7. SUPPRIMER les pages News et Pricing (recherche plus large)
    # Rechercher toutes les pages avec "news" ou "blog" dans l'URL ou le nom
    news_pages = env['website.page'].search([
        '|', '|', '|', '|', '|',
        ('url', '=', '/news'),
        ('url', '=', '/blog'),
        ('url', 'ilike', '%news%'),
        ('url', 'ilike', '%blog%'),
        ('name', 'ilike', '%news%'),
        ('name', 'ilike', '%blog%')
    ])
    
    if news_pages:
        news_pages.unlink()
        cr.commit()
    
    # Rechercher aussi dans les blogs (si le module website_blog est installé)
    try:
        blog_posts = env['blog.post'].search([])
        if blog_posts:
            # Ne pas supprimer les posts, mais on peut les archiver
            pass
    except:
        pass
    
    pricing_pages = env['website.page'].search([
        '|', '|', '|', '|',
        ('url', '=', '/pricing'),
        ('url', '=', '/price'),
        ('url', 'ilike', '%pricing%'),
        ('name', 'ilike', '%pricing%')
    ])
    
    if pricing_pages:
        pricing_pages.unlink()
        cr.commit()
    
    # 8. SUPPRIMER les menus News et Pricing du menu principal (recherche plus large)
    # Rechercher tous les menus avec "news", "blog", "pricing" ou "price"
    all_menus = env['website.menu'].search([])
    
    # Filtrer les menus News/Blog
    news_menus = all_menus.filtered(lambda m: 
        m.name and (
            'news' in m.name.lower() or 
            'blog' in m.name.lower() or
            'actualité' in m.name.lower() or
            'actualites' in m.name.lower()
        ) or (
            m.url and (
                'news' in m.url.lower() or 
                'blog' in m.url.lower()
            )
        )
    )
    
    if news_menus:
        news_menus.unlink()
        cr.commit()
    
    # Filtrer les menus Pricing
    pricing_menus = all_menus.filtered(lambda m: 
        m.name and (
            'pricing' in m.name.lower() or 
            'price' in m.name.lower() or
            'prix' in m.name.lower() or
            'tarif' in m.name.lower()
        ) or (
            m.url and (
                'pricing' in m.url.lower() or 
                'price' in m.url.lower()
            )
        )
    )
    
    if pricing_menus:
        pricing_menus.unlink()
        cr.commit()
    
    # 9. CRÉER les produits du catalogue dans Odoo
    create_catalogue_products(env)
    
    # 10. CRÉER le menu Shop dans la navigation
    create_shop_menu(env)
    
    # Invalider le cache pour forcer le rechargement
    env.registry.clear_cache()


def create_shop_menu(env):
    """Crée le menu Shop dans la navigation principale"""
    import logging
    _logger = logging.getLogger(__name__)
    
    try:
        # Récupérer le website
        website = env['website'].search([], limit=1)
        if not website:
            _logger.warning("Aucun website trouvé")
            return
        
        # Récupérer le menu racine (website.menu_id)
        root_menu = website.menu_id
        if not root_menu:
            _logger.warning("Menu racine non trouvé, tentative de récupération...")
            # Essayer de trouver le menu principal
            main_menu = env.ref('website.main_menu', raise_if_not_found=False)
            if main_menu:
                root_menu = main_menu
            else:
                _logger.error("Impossible de trouver le menu racine")
                return
        
        # Chercher si le menu Shop existe déjà
        shop_menu = env['website.menu'].search([
            ('name', '=', 'Shop'),
            ('parent_id', '=', root_menu.id),
            '|',
            ('website_id', '=', False),
            ('website_id', '=', website.id),
        ], limit=1)
        
        if not shop_menu:
            # Créer le menu Shop
            shop_menu = env['website.menu'].create({
                'name': 'Shop',
                'url': '/shop',
                'parent_id': root_menu.id,
                'sequence': 20,  # Position dans le menu
                'website_id': website.id,
            })
            _logger.info(f"✅ Menu Shop créé (ID: {shop_menu.id})")
        else:
            # Mettre à jour si nécessaire
            if shop_menu.url != '/shop':
                shop_menu.write({'url': '/shop'})
            if shop_menu.parent_id.id != root_menu.id:
                shop_menu.write({'parent_id': root_menu.id})
            _logger.info(f"✅ Menu Shop existe déjà (ID: {shop_menu.id})")
        
        # Récupérer les catégories pour créer les sous-menus
        catalogue_data_model = env['nexprint.catalogue.data']
        categories_info = catalogue_data_model.get_categories_info()
        
        # Supprimer les anciens sous-menus
        old_children = shop_menu.child_id
        if old_children:
            old_children.unlink()
        
        # Créer les sous-menus pour chaque catégorie
        sequence = 10
        for cat_key, cat_info in categories_info.items():
            env['website.menu'].create({
                'name': cat_info['name'],
                'url': f'/shop#{cat_key}',
                'parent_id': shop_menu.id,
                'sequence': sequence,
                'website_id': website.id,
            })
            sequence += 10
        
        env.cr.commit()
        _logger.info(f"✅ Menu Shop avec {len(categories_info)} catégories créé avec succès")
        
    except Exception as e:
        _logger.error(f"❌ Erreur création menu Shop: {e}", exc_info=True)
        env.cr.rollback()


def create_catalogue_products(env, force_recreate=False):
    """Crée les produits du catalogue dans Odoo
    
    Args:
        env: Environnement Odoo
        force_recreate: Si True, recrée tous les produits même s'ils existent déjà
    """
    import logging
    _logger = logging.getLogger(__name__)
    
    try:
        catalogue_data_model = env['nexprint.catalogue.data']
        catalogue_data = catalogue_data_model.get_catalogue_data()
        categories_info = catalogue_data_model.get_categories_info()
        
        # Créer ou récupérer les catégories de produits
        product_categories = {}
        for cat_key, cat_info in categories_info.items():
            # Chercher la catégorie existante ou la créer
            category = env['product.category'].search([
                ('name', '=', cat_info['name'])
            ], limit=1)
            
            if not category:
                category = env['product.category'].create({
                    'name': cat_info['name'],
                })
                env.cr.commit()
                _logger.info(f"Catégorie créée: {cat_info['name']}")
            
            product_categories[cat_key] = category
            _logger.info(f"Catégorie {cat_key}: {cat_info['name']} -> ID: {category.id}")
        
        # Créer les produits
        products_created = 0
        products_updated = 0
        products_skipped = 0
        total_expected = sum(len(products) for products in catalogue_data.values())
        _logger.info(f"Début création produits - Total attendu: {total_expected} produits")
        
        # Compter les produits existants par catégorie pour diagnostic AVANT création
        _logger.info("=" * 60)
        _logger.info("DIAGNOSTIC AVANT CRÉATION:")
        for cat_key, cat_info in categories_info.items():
            category = product_categories.get(cat_key)
            if category:
                existing_count = env['product.template'].search_count([
                    ('categ_id', '=', category.id),
                    ('website_published', '=', True),
                ])
                # Compter aussi les produits par référence dans cette catégorie
                catalogue_data_for_cat = catalogue_data.get(cat_key, [])
                products_found_by_ref = 0
                for product_data in catalogue_data_for_cat:
                    existing = env['product.template'].search([
                        ('default_code', '=', product_data['ref']),
                        ('categ_id', '=', category.id),
                    ], limit=1)
                    if existing:
                        products_found_by_ref += 1
                
                status = "✅" if existing_count >= cat_info.get('count', 0) else "⚠️"
                _logger.info(f"{status} {cat_info['name']}: {existing_count}/{cat_info.get('count', 0)} produits (trouvés par ref: {products_found_by_ref}/{len(catalogue_data_for_cat)})")
        _logger.info("=" * 60)
        
        for cat_key, products in catalogue_data.items():
            category = product_categories.get(cat_key)
            if not category:
                _logger.warning(f"Catégorie non trouvée pour {cat_key}")
                continue
            
            cat_products_created = 0
            cat_products_updated = 0
            cat_products_errors = 0
            _logger.info(f"Traitement catégorie {cat_key} ({category.name}): {len(products)} produits à traiter")
            for product_data in products:
                # Vérifier si le produit existe déjà (recherche par référence)
                existing_product = env['product.template'].search([
                    ('default_code', '=', product_data['ref'])
                ], limit=1)
                
                # Si le produit existe mais n'est pas dans la bonne catégorie, le forcer à être mis à jour
                if existing_product and existing_product.categ_id.id != category.id:
                    _logger.warning(f"Produit {product_data['ref']} existe mais dans mauvaise catégorie: {existing_product.categ_id.name} (attendu: {category.name})")
                
                # Si force_recreate est True, traiter comme nouveau produit
                if force_recreate and existing_product:
                    # Supprimer l'ancien produit pour le recréer
                    try:
                        existing_product.unlink()
                        existing_product = env['product.template']
                        _logger.info(f"Produit {product_data['ref']} supprimé pour recréation")
                    except Exception as e:
                        _logger.error(f"Erreur suppression produit {product_data['ref']}: {e}")
                
                if not existing_product:
                    # Créer le produit
                    # Déterminer le type de produit (Odoo 17 utilise detailed_type)
                    # En Odoo 17, les valeurs acceptées sont: 'consu' (Consumable) et 'service' (Service)
                    if product_data.get('type') == 'service':
                        detailed_type = 'service'
                    else:
                        # Par défaut, utiliser 'consu' pour les produits consommables
                        detailed_type = 'consu'
                    
                    product_vals = {
                        'name': f"{product_data['ref']} - {product_data['desc']}",
                        'default_code': product_data['ref'],
                        'list_price': product_data['ttc'],  # Prix TTC pour l'ecommerce
                        'standard_price': product_data['ht'],  # Coût de revient (Prix HT)
                        'categ_id': category.id,
                        'detailed_type': detailed_type,  # Odoo 17 utilise detailed_type au lieu de type
                        'sale_ok': True,
                        'purchase_ok': False,
                        'website_published': True,
                        'description_sale': f"Prix HT: {product_data['ht']} TND\nPrix TTC: {product_data['ttc']} TND\nUnité: {product_data['unite']}",
                    }
                    
                    try:
                        new_product = env['product.template'].create(product_vals)
                        products_created += 1
                        cat_products_created += 1
                        _logger.info(f"✅ Produit créé: {product_data['ref']} - {product_vals['name']} (Catégorie: {category.name})")
                    except Exception as e:
                        cat_products_errors += 1
                        _logger.error(f"❌ Erreur création produit {product_data['ref']}: {e}", exc_info=True)
                else:
                    # Mettre à jour le produit existant si nécessaire
                    update_vals = {}
                    needs_update = False
                    
                    # Toujours vérifier et corriger la catégorie
                    if existing_product.categ_id.id != category.id:
                        update_vals['categ_id'] = category.id
                        needs_update = True
                        _logger.info(f"Produit {product_data['ref']}: catégorie incorrecte ({existing_product.categ_id.name} -> {category.name})")
                    
                    # Toujours s'assurer que le produit est publié et vendable
                    if not existing_product.website_published:
                        update_vals['website_published'] = True
                        needs_update = True
                    if not existing_product.sale_ok:
                        update_vals['sale_ok'] = True
                        needs_update = True
                    
                    # Mettre à jour les prix si différents
                    if abs(existing_product.list_price - product_data['ttc']) > 0.01:
                        update_vals['list_price'] = product_data['ttc']
                        needs_update = True
                    if abs(existing_product.standard_price - product_data['ht']) > 0.01:
                        update_vals['standard_price'] = product_data['ht']
                        needs_update = True
                    
                    # Mettre à jour le type si nécessaire (Odoo 17 utilise detailed_type)
                    # En Odoo 17, les valeurs acceptées sont: 'consu' (Consumable) et 'service' (Service)
                    expected_detailed_type = 'service' if product_data.get('type') == 'service' else 'consu'
                    if existing_product.detailed_type != expected_detailed_type:
                        update_vals['detailed_type'] = expected_detailed_type
                        needs_update = True
                    
                    if needs_update and update_vals:
                        existing_product.write(update_vals)
                        products_updated += 1
                        cat_products_updated += 1
                        _logger.info(f"Produit mis à jour: {product_data['ref']} - {update_vals}")
                    else:
                        products_skipped += 1
                        # Vérifier quand même si le produit est dans la bonne catégorie
                        if existing_product.categ_id.id != category.id:
                            _logger.warning(f"Produit {product_data['ref']} existe mais n'est pas dans la bonne catégorie (actuel: {existing_product.categ_id.name}, attendu: {category.name})")
            
            cat_info = categories_info.get(cat_key, {})
            _logger.info(f"Catégorie {cat_key} ({cat_info.get('name', cat_key)}): {cat_products_created} créés, {cat_products_updated} mis à jour, {cat_products_errors} erreurs")
            if cat_products_errors > 0:
                _logger.warning(f"⚠️ Catégorie {cat_info.get('name', cat_key)}: {cat_products_errors} erreurs lors de la création!")
            env.cr.commit()
        
        # Vérification finale par catégorie
        _logger.info("=" * 60)
        _logger.info("VÉRIFICATION FINALE PAR CATÉGORIE:")
        for cat_key, cat_info in categories_info.items():
            category = product_categories.get(cat_key)
            if category:
                final_count = env['product.template'].search_count([
                    ('categ_id', '=', category.id),
                    ('website_published', '=', True),
                    ('sale_ok', '=', True),
                ])
                expected = cat_info.get('count', 0)
                status = "✅" if final_count >= expected else "❌"
                _logger.info(f"{status} {cat_info['name']}: {final_count}/{expected} produits")
        
        _logger.info("=" * 60)
        _logger.info(f"Total: {products_created} produits créés, {products_updated} produits mis à jour, {products_skipped} produits déjà à jour")
        print(f"✅ Produits créés: {products_created}, Produits mis à jour: {products_updated}, Produits déjà à jour: {products_skipped}")
        
        # Afficher un résumé par catégorie
        print("\n📊 Résumé par catégorie:")
        for cat_key, cat_info in categories_info.items():
            category = product_categories.get(cat_key)
            if category:
                final_count = env['product.template'].search_count([
                    ('categ_id', '=', category.id),
                    ('website_published', '=', True),
                    ('sale_ok', '=', True),
                ])
                expected = cat_info.get('count', 0)
                status = "✅" if final_count >= expected else "⚠️"
                print(f"  {status} {cat_info['name']}: {final_count}/{expected} produits")
    except Exception as e:
        _logger.error(f"Erreur dans create_catalogue_products: {e}", exc_info=True)
        env.cr.rollback()

