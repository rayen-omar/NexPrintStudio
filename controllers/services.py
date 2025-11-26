# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


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
        # S'assurer que le menu Shop existe
        try:
            from odoo.addons.NXPSTudion.hooks import create_shop_menu
            website = request.env['website'].get_current_website()
            root_menu = website.menu_id
            
            # Vérifier si le menu Shop existe
            shop_menu = request.env['website.menu'].search([
                ('name', '=', 'Shop'),
                ('parent_id', '=', root_menu.id if root_menu else False),
                '|',
                ('website_id', '=', False),
                ('website_id', '=', website.id),
            ], limit=1)
            
            # Si le menu n'existe pas, le créer
            if not shop_menu:
                create_shop_menu(request.env)
        except Exception as e:
            import logging
            _logger = logging.getLogger(__name__)
            _logger.warning(f"Erreur vérification menu Shop: {e}")
        
        # Forcer la création des produits si nécessaire (seulement si pas de produits)
        total_products = request.env['product.template'].search_count([
            ('website_published', '=', True),
            ('sale_ok', '=', True),
        ])
        
        if total_products == 0:
            try:
                from odoo.addons.NXPSTudion.hooks import create_catalogue_products
                create_catalogue_products(request.env)
            except Exception as e:
                import logging
                _logger = logging.getLogger(__name__)
                _logger.error(f"Erreur création produits: {e}")
        
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
                    import logging
                    _logger = logging.getLogger(__name__)
                    _logger.info(f"Catégorie {cat_name}: {products_count}/{expected_count} produits - Création automatique des produits manquants")
                    break
            else:
                # Si la catégorie n'existe pas, il faut créer les produits
                missing_products = True
                break
        
        # Si des produits manquent, forcer la création de tous les produits
        if missing_products:
            try:
                import logging
                _logger = logging.getLogger(__name__)
                _logger.info("Détection de produits manquants - Création automatique en cours...")
                from odoo.addons.NXPSTudion.hooks import create_catalogue_products
                create_catalogue_products(request.env)
                # Invalider le cache des vues pour forcer le rechargement
                request.env.registry.clear_cache()
                _logger.info("Création automatique des produits terminée")
            except Exception as e:
                import logging
                _logger = logging.getLogger(__name__)
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
        
        return request.render('NXPSTudion.shop_catalogue_template', {
            'products_by_category': products_by_category,
            'categories_info': categories_info,
            'categories_list': categories_list,
            'all_products': all_products,  # Tous les produits pour l'affichage en grille
            'total_products': total_products,
        })

