# -*- coding: utf-8 -*-
{
    'name': 'NXPSTudion',
    'version': '17.0.1.0.0',
    'category': 'Website',
    'summary': 'Nexprint Studio - Personnalisation de la page d\'accueil ecommerce',
    'description': """
        Module personnalisé pour Nexprint Studio
        =========================================
        
        Ce module hérite de la page d'accueil du module ecommerce et la personnalise
        selon les besoins de Nexprint Studio, spécialisée dans la communication visuelle,
        l'impression et la gravure publicitaire.
    """,
    'depends': ['website', 'website_sale'],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'NXPSTudion/static/src/css/nexprint_identity.css',
        ],
    },
    'post_init_hook': 'hooks.post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
