# -*- coding: utf-8 -*-
"""
Script pour supprimer manuellement les pages News et Pricing
À exécuter dans la console Odoo ou via un cron
"""

def remove_news_and_pricing(env):
    """Supprime les pages News et Pricing et leurs menus"""
    
    # 1. Supprimer les pages News/Blog
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
        print(f"Suppression de {len(news_pages)} page(s) News/Blog")
        news_pages.unlink()
    
    # 2. Supprimer les pages Pricing
    pricing_pages = env['website.page'].search([
        '|', '|', '|', '|',
        ('url', '=', '/pricing'),
        ('url', '=', '/price'),
        ('url', 'ilike', '%pricing%'),
        ('name', 'ilike', '%pricing%')
    ])
    
    if pricing_pages:
        print(f"Suppression de {len(pricing_pages)} page(s) Pricing")
        pricing_pages.unlink()
    
    # 3. Supprimer les menus News/Blog
    all_menus = env['website.menu'].search([])
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
        print(f"Suppression de {len(news_menus)} menu(s) News/Blog")
        for menu in news_menus:
            print(f"  - Suppression du menu: {menu.name} (URL: {menu.url})")
        news_menus.unlink()
    
    # 4. Supprimer les menus Pricing
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
        print(f"Suppression de {len(pricing_menus)} menu(s) Pricing")
        for menu in pricing_menus:
            print(f"  - Suppression du menu: {menu.name} (URL: {menu.url})")
        pricing_menus.unlink()
    
    env.cr.commit()
    env.registry.clear_cache()
    print("Suppression terminée avec succès!")


