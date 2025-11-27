# -*- coding: utf-8 -*-

import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ServicesController(http.Controller):

    @http.route(['/our-services', '/services'], type='http', auth="public", website=True, sitemap=True)
    def services_page(self, **kw):
        """Page personnalisée des services NexPrint Studio - Remplace la page par défaut"""
        return request.render('NXPSTudion.services_page_template', {})
    
    @http.route('/nos-services', type='http', auth="public", website=True, sitemap=True)
    def services_page_alt(self, **kw):
        """Page personnalisée des services NexPrint Studio - Route alternative"""
        return request.render('NXPSTudion.services_page_template', {})
    
    @http.route(['/about-us', '/aboutus', '/about'], type='http', auth="public", website=True, sitemap=True)
    def about_us_page(self, **kw):
        """Page personnalisée À propos de NexPrint Studio - Remplace la page par défaut"""
        return request.render('NXPSTudion.about_us_page_template', {})
    
    @http.route(['/contactus', '/contact-us', '/contact'], type='http', auth="public", website=True, sitemap=True)
    def contact_page(self, **kw):
        """Page personnalisée Contact NexPrint Studio - Remplace la page par défaut"""
        return request.render('NXPSTudion.contact_page_template', {})
    
    @http.route(['/news', '/blog', '/pricing', '/price', '/blog/<path:path>'], type='http', auth="public", website=True)
    def remove_pages(self, path=None, **kw):
        """Redirige les pages News et Pricing vers la page d'accueil (pages supprimées)"""
        return request.redirect('/')
    
    @http.route('/shop/update-menus', type='http', auth="user", website=True)
    def update_menus_route(self, **kw):
        """Route pour forcer la mise à jour des menus Shop"""
        try:
            from odoo.addons.NXPSTudion.hooks import create_shop_menu
            create_shop_menu(request.env)
            
            # Afficher les menus pour vérification
            website = request.env['website'].get_current_website()
            root_menu = website.menu_id
            shop_menu = request.env['website.menu'].search([
                ('name', '=', 'Shop'),
                ('parent_id', '=', root_menu.id if root_menu else False),
            ], limit=1)
            
            menu_info = []
            if shop_menu:
                for child in shop_menu.child_id:
                    menu_info.append(f"{child.name}: {child.url}")
            
            return f"""
            <html>
            <body>
                <h1>Menus mis à jour avec succès!</h1>
                <h2>Menus Shop:</h2>
                <ul>
                    {'<br>'.join([f'<li>{m}</li>' for m in menu_info]) if menu_info else '<li>Aucun sous-menu</li>'}
                </ul>
                <p><a href="/shop">Retour au shop</a></p>
            </body>
            </html>
            """
        except Exception as e:
            _logger.error(f"Erreur mise à jour menus: {e}", exc_info=True)
            return f"<html><body><h1>Erreur: {str(e)}</h1></body></html>"
    
    @http.route('/shop/create-products', type='http', auth="user", website=True)
    def create_products_route(self, **kw):
        """Route pour forcer la création des produits (admin seulement)"""
        try:
            from odoo.addons.NXPSTudion.hooks import create_catalogue_products
            create_catalogue_products(request.env)
            return request.render('website.page_404', {
                'message': 'Produits créés avec succès!'
            })
        except Exception as e:
            return request.render('website.page_404', {
                'message': f'Erreur: {str(e)}'
            })
    
    @http.route(['/shop', '/boutique'], type='http', auth="public", website=True, sitemap=True)
    def shop_page(self, **kw):
        """Page catalogue Shop NexPrint Studio - Remplace la page par défaut"""
        # Mettre à jour automatiquement les menus Shop (vérification intelligente)
        try:
            from odoo.addons.NXPSTudion.hooks import create_shop_menu
            website = request.env['website'].get_current_website()
            root_menu = website.menu_id
            
            # Vérifier rapidement si une mise à jour est nécessaire
            shop_menu = request.env['website.menu'].search([
                ('name', '=', 'Shop'),
                ('parent_id', '=', root_menu.id if root_menu else False),
            ], limit=1)
            
            needs_update = False
            if shop_menu:
                # Vérifier si des menus utilisent encore des hashs (#) au lieu de paramètres (?)
                for child in shop_menu.child_id:
                    if child.url and child.url.startswith('/shop#'):
                        needs_update = True
                        break
                    # Vérifier aussi si le nombre de catégories correspond
                    catalogue_data_model = request.env['nexprint.catalogue.data']
                    categories_info = catalogue_data_model.get_categories_info()
                    if len(shop_menu.child_id) != len(categories_info):
                        needs_update = True
                        break
            else:
                needs_update = True
            
            # Mettre à jour seulement si nécessaire
            if needs_update:
                create_shop_menu(request.env)
        except Exception as e:
            _logger.warning(f"Erreur mise à jour automatique menu Shop: {e}")
        
        # Vérifier et créer/mettre à jour les produits automatiquement
        total_products = request.env['product.template'].search_count([
            ('website_published', '=', True),
            ('sale_ok', '=', True),
        ])
        
        try:
            from odoo.addons.NXPSTudion.hooks import create_catalogue_products
            catalogue_data_model = request.env['nexprint.catalogue.data']
            products_with_variants = catalogue_data_model.get_products_with_variants()
            
            # Vérifier s'il y a des doublons dans les catégories
            has_duplicates = False
            categories_info = catalogue_data_model.get_categories_info()
            for cat_key, cat_info in categories_info.items():
                category = request.env['product.category'].search([
                    ('name', '=', cat_info['name'])
                ], limit=1)
                if category:
                    # Compter les produits par référence
                    products = request.env['product.template'].search([
                        ('categ_id', '=', category.id),
                    ])
                    refs = {}
                    for product in products:
                        ref = product.default_code or 'NO_REF'
                        refs[ref] = refs.get(ref, 0) + 1
                        if refs[ref] > 1:
                            has_duplicates = True
                            break
                if has_duplicates:
                    break
            
            # Vérifier si des anciens produits avec variantes existent encore (à convertir)
            needs_update = False
            for base_name, variants in products_with_variants.items():
                for variant_data in variants:
                    old_product = request.env['product.template'].search([
                        ('default_code', '=', variant_data['ref']),
                        ('name', 'ilike', variant_data['desc']),
                    ], limit=1)
                    if old_product:
                        needs_update = True
                        break
                if needs_update:
                    break
            
            # Vérifier aussi si le produit template avec variantes n'existe pas
            if not needs_update:
                for base_name, variants in products_with_variants.items():
                    first_variant = variants[0]
                    # Trouver la catégorie
                    cat_key = None
                    catalogue_data = catalogue_data_model.get_catalogue_data()
                    for ck, products in catalogue_data.items():
                        for p in products:
                            if p['ref'] == first_variant['ref']:
                                cat_key = ck
                                break
                        if cat_key:
                            break
                    
                    if cat_key:
                        category = request.env['product.category'].search([
                            ('name', '=', catalogue_data_model.get_categories_info()[cat_key]['name'])
                        ], limit=1)
                        if category:
                            product_template = request.env['product.template'].search([
                                ('name', '=', base_name),
                                ('categ_id', '=', category.id),
                            ], limit=1)
                            if not product_template:
                                needs_update = True
                                break
            
            # Si nécessaire, mettre à jour les produits
            if needs_update or has_duplicates:
                if has_duplicates:
                    _logger.info("🔄 Nettoyage automatique des doublons...")
                if needs_update:
                    _logger.info("🔄 Mise à jour automatique des produits avec variantes...")
                create_catalogue_products(request.env, force_recreate=False)
                total_products = request.env['product.template'].search_count([
                    ('website_published', '=', True),
                    ('sale_ok', '=', True),
                ])
            elif total_products == 0:
                create_catalogue_products(request.env)
                total_products = request.env['product.template'].search_count([
                    ('website_published', '=', True),
                    ('sale_ok', '=', True),
                ])
        except Exception as e:
            _logger.error(f"Erreur création/mise à jour produits: {e}")
        
        # Récupérer les produits depuis Odoo
        products_by_category = {}
        categories_info = request.env['nexprint.catalogue.data'].get_categories_info()
        
        # Utiliser les noms de catégories depuis categories_info
        category_mapping = {}
        for cat_key, cat_info in categories_info.items():
            category_mapping[cat_key] = cat_info['name']
        
        # Vérifier d'abord si des produits manquent (par catégorie)
        missing_products = False
        expected_counts = {}
        for cat_key, cat_info in categories_info.items():
            expected_counts[cat_key] = cat_info.get('count', 0)
        
        for cat_key, cat_name in category_mapping.items():
            category = request.env['product.category'].search([
                ('name', '=', cat_name)
            ], limit=1)
            
            if category:
                products_count = request.env['product.template'].search_count([
                    ('categ_id', '=', category.id),
                    ('website_published', '=', True),
                    ('sale_ok', '=', True),
                ])
                expected_count = expected_counts.get(cat_key, 0)
                # Si le nombre de produits est inférieur au nombre attendu, créer les produits manquants
                if products_count < expected_count:
                    missing_products = True
                    _logger.info(f"Catégorie {cat_name}: {products_count}/{expected_count} produits - Création automatique des produits manquants")
                    break
            else:
                # Si la catégorie n'existe pas, il faut créer les produits
                missing_products = True
                break
        
        # Si des produits manquent, forcer la création de tous les produits
        if missing_products:
            try:
                _logger.info("Détection de produits manquants - Création automatique en cours...")
                from odoo.addons.NXPSTudion.hooks import create_catalogue_products
                create_catalogue_products(request.env)
                request.env.registry.clear_cache()
                _logger.info("Création automatique des produits terminée")
            except Exception as e:
                _logger.error(f"Erreur création produits: {e}", exc_info=True)
        
        # Récupérer les produits par catégorie
        for cat_key, cat_name in category_mapping.items():
            category = request.env['product.category'].search([
                ('name', '=', cat_name)
            ], limit=1)
            
            if category:
                products = request.env['product.template'].search([
                    ('categ_id', '=', category.id),
                    ('website_published', '=', True),
                    ('sale_ok', '=', True),
                ], order='default_code')
                products_by_category[cat_key] = products
            else:
                products_by_category[cat_key] = request.env['product.template']
        
        # Préparer les catégories avec les counts de produits calculés dans le contrôleur
        categories_list = []
        all_products = []  # Liste de tous les produits pour l'affichage en grille
        
        for cat_key, cat_info in categories_info.items():
            cat_products = products_by_category.get(cat_key, [])
            # Calculer le count ici en Python pour éviter les problèmes avec len() dans QWeb
            try:
                if cat_products:
                    products_count = len(cat_products)
                    # Ajouter les produits à la liste globale avec leur catégorie
                    for product in cat_products:
                        all_products.append({
                            'product': product,
                            'category_key': cat_key,
                            'category_name': cat_info['name'],
                            'category_icon': cat_info.get('icon', 'fa-cube'),
                        })
                else:
                    products_count = 0
            except:
                products_count = 0
            
            # Créer un nouveau dict avec les infos de catégorie + le count
            cat_info_with_count = dict(cat_info)
            cat_info_with_count['products_count'] = products_count
            categories_list.append((cat_key, cat_info_with_count))
        
        # Calculer le total de produits
        total_products = len(all_products)
        
        # Récupérer le paramètre de catégorie depuis l'URL
        selected_category = ''
        if hasattr(request, 'httprequest') and hasattr(request.httprequest, 'args'):
            selected_category = request.httprequest.args.get('category', '') or ''
        if not selected_category and 'category' in kw:
            selected_category = kw.get('category', '') or ''
        if not selected_category and hasattr(request, 'params'):
            selected_category = request.params.get('category', '') or ''
        if selected_category:
            selected_category = str(selected_category).strip()
        
        # Filtrer les produits si une catégorie est sélectionnée
        filtered_products = all_products
        if selected_category and selected_category in categories_info:
            filtered_products = [p for p in all_products if p.get('category_key') == selected_category]
            total_products = len(filtered_products)
        
        return request.render('NXPSTudion.shop_catalogue_template', {
            'products_by_category': products_by_category,
            'categories_info': categories_info,
            'categories_list': categories_list,
            'all_products': all_products,  # Tous les produits pour l'affichage en grille
            'filtered_products': filtered_products,  # Produits filtrés selon la catégorie
            'total_products': total_products,
            'selected_category': selected_category,  # Catégorie actuellement sélectionnée
        })

