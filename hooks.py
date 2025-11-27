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
        else:
            if shop_menu.url != '/shop':
                shop_menu.write({'url': '/shop'})
            if shop_menu.parent_id.id != root_menu.id:
                shop_menu.write({'parent_id': root_menu.id})
        
        # Récupérer les catégories pour créer les sous-menus
        catalogue_data_model = env['nexprint.catalogue.data']
        categories_info = catalogue_data_model.get_categories_info()
        
        existing_menus = {menu.name: menu for menu in shop_menu.child_id}
        menus_to_update = []
        menus_to_create = []
        sequence = 10
        for cat_key, cat_info in categories_info.items():
            menu_name = cat_info['name']
            menu_url = f'/shop?category={cat_key}'
            
            if menu_name in existing_menus:
                existing_menu = existing_menus[menu_name]
                if existing_menu.url != menu_url or existing_menu.url.startswith('/shop#'):
                    existing_menu.write({'url': menu_url, 'sequence': sequence})
                    menus_to_update.append(menu_name)
                else:
                    existing_menu.write({'sequence': sequence})
            else:
                menus_to_create.append((menu_name, menu_url))
            
            sequence += 10
        
        for menu_name, menu_url in menus_to_create:
            env['website.menu'].create({
                'name': menu_name,
                'url': menu_url,
                'parent_id': shop_menu.id,
                'sequence': sequence,
                'website_id': website.id,
            })
        
        category_names = {cat_info['name'] for cat_info in categories_info.values()}
        menus_to_delete = [menu for menu in shop_menu.child_id if menu.name not in category_names]
        if menus_to_delete:
            menus_to_delete.unlink()
        
        env.cr.commit()
        
    except Exception as e:
        _logger.error(f"Erreur création menu Shop: {e}", exc_info=True)
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
            
            product_categories[cat_key] = category
        
        # Nettoyer les doublons avant de commencer
        for cat_key, cat_info in categories_info.items():
            category = product_categories.get(cat_key)
            if category:
                all_products = env['product.template'].search([('categ_id', '=', category.id)])
                products_by_ref = {}
                for product in all_products:
                    ref = product.default_code or 'NO_REF'
                    if ref not in products_by_ref:
                        products_by_ref[ref] = []
                    products_by_ref[ref].append(product)
                
                duplicates_removed = 0
                for ref, product_list in products_by_ref.items():
                    if len(product_list) > 1:
                        for dup in product_list[1:]:
                            try:
                                dup.unlink()
                                duplicates_removed += 1
                            except Exception as e:
                                _logger.error(f"Erreur suppression doublon {dup.id}: {e}")
                
                if duplicates_removed > 0:
                    env.cr.commit()
                    _logger.info(f"{duplicates_removed} doublons supprimés dans {cat_info['name']}")
        
        # Créer les produits
        products_created = 0
        products_updated = 0
        products_skipped = 0
        
        # Traiter d'abord les produits avec variantes
        products_with_variants = catalogue_data_model.get_products_with_variants()
        variant_refs = set()  # Références des produits qui sont des variantes
        
        for base_name, variants in products_with_variants.items():
            # Trouver la catégorie pour ces variantes (elles sont toutes dans la même catégorie)
            first_variant = variants[0]
            cat_key_for_variant = None
            for cat_key, products in catalogue_data.items():
                for p in products:
                    if p['ref'] == first_variant['ref']:
                        cat_key_for_variant = cat_key
                        break
                if cat_key_for_variant:
                    break
            
            if not cat_key_for_variant:
                continue
            
            category = product_categories.get(cat_key_for_variant)
            if not category:
                continue
            
            # SUPPRIMER AUTOMATIQUEMENT les anciens produits qui sont maintenant des variantes
            for variant_data in variants:
                variant_refs.add(variant_data['ref'])
                # Chercher et supprimer les anciens produits avec ces références
                old_products = env['product.template'].search([
                    ('default_code', '=', variant_data['ref'])
                ])
                if old_products:
                    for old_product in old_products:
                        try:
                            old_product.unlink()
                        except Exception as e:
                            _logger.error(f"Erreur suppression {variant_data['ref']}: {e}")
                    env.cr.commit()
            
            # Créer ou récupérer l'attribut "Format"
            attribute = env['product.attribute'].search([('name', '=', 'Format')], limit=1)
            if not attribute:
                attribute = env['product.attribute'].create({
                    'name': 'Format',
                    'create_variant': 'always',
                    'display_type': 'radio',
                })
            
            # Créer les valeurs d'attribut pour chaque variante
            attribute_values = {}
            for variant_data in variants:
                variant_refs.add(variant_data['ref'])
                variant_value = variant_data.get('variant', variant_data['desc'].split()[-1])  # Ex: "A2" ou "A1"
                attr_value = env['product.attribute.value'].search([
                    ('attribute_id', '=', attribute.id),
                    ('name', '=', variant_value)
                ], limit=1)
                if not attr_value:
                    attr_value = env['product.attribute.value'].create({
                        'name': variant_value,
                        'attribute_id': attribute.id,
                    })
                attribute_values[variant_value] = {
                    'attr_value': attr_value,
                    'data': variant_data,
                }
            
            # Créer ou récupérer le produit template
            product_name = base_name
            product_template = env['product.template'].search([
                ('name', '=', product_name),
                ('categ_id', '=', category.id),
            ], limit=1)
            
            # Déterminer le type de produit
            detailed_type = 'service' if variants[0].get('type') == 'service' else 'consu'
            
            if not product_template:
                # Créer le produit template
                product_template = env['product.template'].create({
                    'name': product_name,
                    'default_code': variants[0]['ref'].split('-')[0] + '-BASE',  # Ex: "IMP-AFF-BASE"
                    'categ_id': category.id,
                    'detailed_type': detailed_type,
                    'sale_ok': True,
                    'purchase_ok': False,
                    'website_published': True,
                    'description_sale': f"Produit avec variantes de format",
                })
                
                # Ajouter l'attribut au produit
                env['product.template.attribute.line'].create({
                    'product_tmpl_id': product_template.id,
                    'attribute_id': attribute.id,
                    'value_ids': [(6, 0, [av['attr_value'].id for av in attribute_values.values()])],
                })
            else:
                # Vérifier si l'attribut Format existe déjà
                has_format_attribute = False
                for attr_line in product_template.attribute_line_ids:
                    if attr_line.attribute_id.id == attribute.id:
                        has_format_attribute = True
                        # Vérifier si toutes les valeurs sont présentes
                        existing_values = set(attr_line.value_ids.mapped('name'))
                        needed_values = set(attribute_values.keys())
                        if existing_values != needed_values:
                            attr_line.write({
                                'value_ids': [(6, 0, [av['attr_value'].id for av in attribute_values.values()])],
                            })
                        break
                
                if not has_format_attribute:
                    env['product.template.attribute.line'].create({
                        'product_tmpl_id': product_template.id,
                        'attribute_id': attribute.id,
                        'value_ids': [(6, 0, [av['attr_value'].id for av in attribute_values.values()])],
                    })
                
                update_vals = {}
                if product_template.detailed_type != detailed_type:
                    update_vals['detailed_type'] = detailed_type
                if not product_template.website_published:
                    update_vals['website_published'] = True
                if not product_template.sale_ok:
                    update_vals['sale_ok'] = True
                if update_vals:
                    product_template.write(update_vals)
            
            # Forcer la création des variantes en accédant à product_variant_ids
            # Odoo crée automatiquement toutes les variantes possibles
            env.cr.commit()
            product_template.invalidate_recordset(['product_variant_ids'])
            
            # Créer ou mettre à jour les variantes
            for variant_value, variant_info in attribute_values.items():
                variant_data = variant_info['data']
                attr_value = variant_info['attr_value']
                
                # Trouver la variante correspondante en utilisant product_template_attribute_value_ids
                variant = None
                for v in product_template.product_variant_ids:
                    # Vérifier si cette variante a la bonne valeur d'attribut
                    for ptav in v.product_template_attribute_value_ids:
                        if ptav.product_attribute_value_id.id == attr_value.id:
                            variant = v
                            break
                    if variant:
                        break
                
                if variant:
                    # Mettre à jour la variante
                    variant.write({
                        'default_code': variant_data['ref'],
                        'list_price': variant_data['ttc'],
                        'standard_price': variant_data['ht'],
                        'website_published': True,
                        'sale_ok': True,
                    })
        
        # Traiter les produits normaux (sans variantes)
        for cat_key, products in catalogue_data.items():
            category = product_categories.get(cat_key)
            if not category:
                _logger.warning(f"Catégorie non trouvée pour {cat_key}")
                continue
            
            cat_products_created = 0
            cat_products_updated = 0
            cat_products_errors = 0
            for product_data in products:
                # Ignorer les produits qui sont des variantes
                if product_data['ref'] in variant_refs:
                    continue
                
                # Vérifier s'il y a des doublons existants pour cette référence
                duplicate_products = env['product.template'].search([
                    ('default_code', '=', product_data['ref'])
                ])
                
                if len(duplicate_products) > 1:
                    for dup in duplicate_products[1:]:
                        try:
                            dup.unlink()
                        except Exception as e:
                            _logger.error(f"Erreur suppression doublon {dup.id}: {e}")
                    env.cr.commit()
                    existing_product = duplicate_products[0]
                elif len(duplicate_products) == 1:
                    existing_product = duplicate_products[0]
                else:
                    existing_product = env['product.template']
                
                if not existing_product:
                    product_name = f"{product_data['ref']} - {product_data['desc']}"
                    existing_by_name = env['product.template'].search([
                        ('name', '=', product_name),
                        ('categ_id', '=', category.id),
                    ], limit=1)
                    if existing_by_name:
                        existing_product = existing_by_name
                
                if existing_product and existing_product.categ_id.id != category.id:
                    _logger.warning(f"Produit {product_data['ref']} dans mauvaise catégorie: {existing_product.categ_id.name} -> {category.name}")
                
                if force_recreate and existing_product:
                    try:
                        existing_product.unlink()
                        existing_product = env['product.template']
                    except Exception as e:
                        _logger.error(f"Erreur suppression produit {product_data['ref']}: {e}")
                
                if not existing_product:
                    detailed_type = 'service' if product_data.get('type') == 'service' else 'consu'
                    product_vals = {
                        'name': f"{product_data['ref']} - {product_data['desc']}",
                        'default_code': product_data['ref'],
                        'list_price': product_data['ttc'],
                        'standard_price': product_data['ht'],
                        'categ_id': category.id,
                        'detailed_type': detailed_type,
                        'sale_ok': True,
                        'purchase_ok': False,
                        'website_published': True,
                        'description_sale': f"Prix HT: {product_data['ht']} TND\nPrix TTC: {product_data['ttc']} TND\nUnité: {product_data['unite']}",
                    }
                    
                    try:
                        env['product.template'].create(product_vals)
                        products_created += 1
                        cat_products_created += 1
                    except Exception as e:
                        cat_products_errors += 1
                        _logger.error(f"Erreur création produit {product_data['ref']}: {e}", exc_info=True)
                else:
                    update_vals = {}
                    needs_update = False
                    
                    if existing_product.categ_id.id != category.id:
                        update_vals['categ_id'] = category.id
                        needs_update = True
                    if not existing_product.website_published:
                        update_vals['website_published'] = True
                        needs_update = True
                    if not existing_product.sale_ok:
                        update_vals['sale_ok'] = True
                        needs_update = True
                    if abs(existing_product.list_price - product_data['ttc']) > 0.01:
                        update_vals['list_price'] = product_data['ttc']
                        needs_update = True
                    if abs(existing_product.standard_price - product_data['ht']) > 0.01:
                        update_vals['standard_price'] = product_data['ht']
                        needs_update = True
                    
                    expected_detailed_type = 'service' if product_data.get('type') == 'service' else 'consu'
                    if existing_product.detailed_type != expected_detailed_type:
                        update_vals['detailed_type'] = expected_detailed_type
                        needs_update = True
                    
                    if needs_update and update_vals:
                        existing_product.write(update_vals)
                        products_updated += 1
                        cat_products_updated += 1
                    else:
                        products_skipped += 1
            
            if cat_products_errors > 0:
                _logger.warning(f"Catégorie {categories_info.get(cat_key, {}).get('name', cat_key)}: {cat_products_errors} erreurs")
            env.cr.commit()
    except Exception as e:
        _logger.error(f"Erreur dans create_catalogue_products: {e}", exc_info=True)
        env.cr.rollback()

