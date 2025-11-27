# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCatalogue(models.Model):
    """Modèle pour gérer le catalogue de produits NexPrint Studio"""
    _name = 'nexprint.catalogue'
    _description = 'Catalogue Produits NexPrint Studio'
    _order = 'categorie, reference'

    reference = fields.Char(string='Référence', required=True, index=True)
    categorie = fields.Selection([
        ('sublimation', 'Sublimation'),
        ('goodies', 'Goodies'),
        ('signaletique', 'Signalétique'),
        ('covering', 'Covering Véhicules'),
        ('impression', 'Impression'),
        ('gravure', 'Gravure & CNC'),
        ('decoration', 'Décoration & PLV'),
        ('textile', 'Textile & Broderie'),
        ('cadeaux', 'Cadeaux Personnalisés'),
        ('services', 'Services Graphiques & Installation'),
        ('consommables', 'Consommables Production'),
    ], string='Catégorie', required=True, index=True)
    designation = fields.Char(string='Désignation', required=True)
    prix_ht = fields.Float(string='Prix HT (TND)', required=True, digits=(16, 2))
    tva = fields.Float(string='TVA (%)', default=19.0, digits=(16, 2))
    prix_ttc = fields.Float(string='Prix TTC (TND)', compute='_compute_prix_ttc', store=True, digits=(16, 2))
    type_produit = fields.Selection([
        ('produit', 'Produit'),
        ('service', 'Service'),
    ], string='Type', required=True, default='produit')
    unite = fields.Char(string='Unité', required=True, default='Pièce')
    actif = fields.Boolean(string='Actif', default=True)

    @api.depends('prix_ht', 'tva')
    def _compute_prix_ttc(self):
        for record in self:
            record.prix_ttc = record.prix_ht * (1 + record.tva / 100)

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.reference} - {record.designation}"
            result.append((record.id, name))
        return result


class CatalogueData(models.AbstractModel):
    """Données du catalogue - Classe utilitaire pour charger les données"""
    _name = 'nexprint.catalogue.data'
    _description = 'Données du catalogue NexPrint Studio'

    def get_catalogue_data(self):
        """Retourne toutes les données du catalogue"""
        return {
            'sublimation': [
                {'ref': 'SUB-T01', 'desc': 'T-shirt blanc polyester 180 g', 'ht': 12, 'ttc': 14.28, 'unite': 'Pièce'},
                {'ref': 'SUB-T02', 'desc': 'T-shirt technique sport 150 g', 'ht': 15, 'ttc': 17.85, 'unite': 'Pièce'},
                {'ref': 'SUB-T03', 'desc': 'T-shirt enfant polyester', 'ht': 10, 'ttc': 11.9, 'unite': 'Pièce'},
                {'ref': 'SUB-POL01', 'desc': 'Polo polyester sublimable', 'ht': 22, 'ttc': 26.18, 'unite': 'Pièce'},
                {'ref': 'SUB-SWE01', 'desc': 'Sweat capuche sublimable', 'ht': 48, 'ttc': 57.12, 'unite': 'Pièce'},
                {'ref': 'SUB-CAS01', 'desc': 'Casquette blanche sublimable', 'ht': 9, 'ttc': 10.71, 'unite': 'Pièce'},
                {'ref': 'SUB-MUG01', 'desc': 'Mug blanc 330 ml', 'ht': 7, 'ttc': 8.33, 'unite': 'Pièce'},
                {'ref': 'SUB-MUG02', 'desc': 'Mug magique noir 330 ml', 'ht': 9.5, 'ttc': 11.3, 'unite': 'Pièce'},
                {'ref': 'SUB-MUG03', 'desc': 'Mug intérieur coloré 330 ml', 'ht': 8.5, 'ttc': 10.12, 'unite': 'Pièce'},
                {'ref': 'SUB-GOU01', 'desc': 'Gourde alu 600 ml', 'ht': 16, 'ttc': 19.04, 'unite': 'Pièce'},
                {'ref': 'SUB-THER01', 'desc': 'Bouteille isotherme 500 ml', 'ht': 28, 'ttc': 33.32, 'unite': 'Pièce'},
                {'ref': 'SUB-CUS01', 'desc': 'Coussin 40x40 cm + housse', 'ht': 18, 'ttc': 21.42, 'unite': 'Pièce'},
                {'ref': 'SUB-MAT01', 'desc': 'Tapis de souris 22x18 cm', 'ht': 5.5, 'ttc': 6.54, 'unite': 'Pièce'},
                {'ref': 'SUB-PK01', 'desc': 'Porte-clés métal sublimable', 'ht': 4.2, 'ttc': 5, 'unite': 'Pièce'},
                {'ref': 'SUB-PLAALU01', 'desc': 'Plaque aluminium 20x30 cm', 'ht': 19, 'ttc': 22.61, 'unite': 'Pièce'},
                {'ref': 'SUB-PUZ01', 'desc': 'Puzzle A4 80 pièces', 'ht': 11, 'ttc': 13.09, 'unite': 'Pièce'},
                {'ref': 'SUB-COQ01', 'desc': 'Coque téléphone (modèles courants)', 'ht': 12, 'ttc': 14.28, 'unite': 'Pièce'},
                {'ref': 'SUB-TAB01', 'desc': 'Tablier cuisine polyester', 'ht': 14, 'ttc': 16.66, 'unite': 'Pièce'},
                {'ref': 'SUB-TOTE01', 'desc': 'Tote bag polyester sublimable', 'ht': 9, 'ttc': 10.71, 'unite': 'Pièce'},
                {'ref': 'SUB-HOR01', 'desc': 'Horloge murale sublimable', 'ht': 22, 'ttc': 26.18, 'unite': 'Pièce'},
            ],
            'goodies': [
                {'ref': 'GOO-PEN01', 'desc': 'Stylo publicitaire plastique', 'ht': 0.85, 'ttc': 1.01, 'unite': 'Pièce'},
                {'ref': 'GOO-PEN02', 'desc': 'Stylo métal gravé laser', 'ht': 3.2, 'ttc': 3.81, 'unite': 'Pièce'},
                {'ref': 'GOO-NOTE01', 'desc': 'Bloc-notes A5 80 pages', 'ht': 4.8, 'ttc': 5.71, 'unite': 'Pièce'},
                {'ref': 'GOO-USB16', 'desc': 'Clé USB 16 Go personnalisée', 'ht': 18, 'ttc': 21.42, 'unite': 'Pièce'},
                {'ref': 'GOO-USB32', 'desc': 'Clé USB 32 Go personnalisée', 'ht': 24, 'ttc': 28.56, 'unite': 'Pièce'},
                {'ref': 'GOO-LANY01', 'desc': 'Lanière badge imprimée', 'ht': 2.9, 'ttc': 3.45, 'unite': 'Pièce'},
                {'ref': 'GOO-BADG01', 'desc': 'Badge rond 58 mm', 'ht': 2.5, 'ttc': 2.97, 'unite': 'Pièce'},
                {'ref': 'GOO-POW01', 'desc': 'Powerbank 5000 mAh personnalisée', 'ht': 39, 'ttc': 46.41, 'unite': 'Pièce'},
                {'ref': 'GOO-UMBR01', 'desc': 'Parapluie publicitaire auto', 'ht': 22, 'ttc': 26.18, 'unite': 'Pièce'},
                {'ref': 'GOO-BOTT01', 'desc': 'Gobelet réutilisable 30 cl', 'ht': 2.2, 'ttc': 2.62, 'unite': 'Pièce'},
                {'ref': 'GOO-CAP01', 'desc': 'Casquette promo 5 panneaux', 'ht': 6.5, 'ttc': 7.73, 'unite': 'Pièce'},
                {'ref': 'GOO-BAG01', 'desc': 'Sac shopping non tissé', 'ht': 3.8, 'ttc': 4.52, 'unite': 'Pièce'},
                {'ref': 'GOO-MAG01', 'desc': 'Magnet 7x7 cm', 'ht': 1.6, 'ttc': 1.9, 'unite': 'Pièce'},
                {'ref': 'GOO-LIGH01', 'desc': 'Briquet imprimé', 'ht': 1.2, 'ttc': 1.43, 'unite': 'Pièce'},
            ],
            'signaletique': [
                {'ref': 'SIG-ALU01', 'desc': 'Plaque Alucobond 100×50 cm', 'ht': 70, 'ttc': 83.3, 'unite': 'm²'},
                {'ref': 'SIG-ALU02', 'desc': 'Panneau Dibond 3 mm impression', 'ht': 85, 'ttc': 101.15, 'unite': 'm²'},
                {'ref': 'SIG-PVC01', 'desc': 'Panneau PVC expansé 5 mm', 'ht': 45, 'ttc': 53.55, 'unite': 'm²'},
                {'ref': 'SIG-TOt01', 'desc': 'Totem extérieur 2 faces 200x60 cm', 'ht': 420, 'ttc': 499.8, 'unite': 'Pièce'},
                {'ref': 'SIG-LED01', 'desc': 'Enseigne lumineuse LED 100x40 cm', 'ht': 650, 'ttc': 773.5, 'unite': 'Pièce'},
                {'ref': 'SIG-NEON01', 'desc': 'Néon flex sur mesure (lettre)', 'ht': 38, 'ttc': 45.22, 'unite': 'Lettre'},
                {'ref': 'SIG-BAN01', 'desc': 'Bâche PVC 440g/m² impression', 'ht': 32, 'ttc': 38.08, 'unite': 'm²'},
                {'ref': 'SIG-MESH01', 'desc': 'Bâche micro-perforée (mesh)', 'ht': 36, 'ttc': 42.84, 'unite': 'm²'},
                {'ref': 'SIG-ADH01', 'desc': 'Adhésif vinyle polymère imprimé', 'ht': 28, 'ttc': 33.32, 'unite': 'm²'},
                {'ref': 'SIG-SABL01', 'desc': 'Vinyle dépoli (sablé)', 'ht': 35, 'ttc': 41.65, 'unite': 'm²'},
                {'ref': 'SIG-PLAQ01', 'desc': 'Plaque de porte pro 20x30 cm', 'ht': 29, 'ttc': 34.51, 'unite': 'Pièce'},
                {'ref': 'SIG-PLAQ02', 'desc': 'Plaque de bureau 10x20 cm', 'ht': 18, 'ttc': 21.42, 'unite': 'Pièce'},
                {'ref': 'SIG-DRAP01', 'desc': 'Beach flag 3,4 m voile', 'ht': 110, 'ttc': 130.9, 'unite': 'Pièce'},
                {'ref': 'SIG-ROLL01', 'desc': 'Roll-up 85x200 cm', 'ht': 80, 'ttc': 95.2, 'unite': 'Pièce'},
                {'ref': 'SIG-KAK01', 'desc': 'Kakemono 80x200 cm', 'ht': 85, 'ttc': 101.15, 'unite': 'Pièce'},
                {'ref': 'SIG-CHAN01', 'desc': 'Panneau de chantier 60x80 cm', 'ht': 65, 'ttc': 77.35, 'unite': 'Pièce'},
            ],
            'covering': [
                {'ref': 'COV-AUTO01', 'desc': 'Habillage flanc droit véhicule utilitaire', 'ht': 150, 'ttc': 178.5, 'unite': 'm²', 'type': 'service'},
                {'ref': 'COV-AUTO02', 'desc': 'Habillage flanc gauche véhicule utilitaire', 'ht': 150, 'ttc': 178.5, 'unite': 'm²', 'type': 'service'},
                {'ref': 'COV-REAR01', 'desc': 'Sticker arrière complet', 'ht': 95, 'ttc': 113.05, 'unite': 'Pièce', 'type': 'service'},
                {'ref': 'COV-LOGO01', 'desc': 'Lettrage logo + coordonnées (set)', 'ht': 85, 'ttc': 101.15, 'unite': 'Set', 'type': 'service'},
                {'ref': 'COV-FULL01', 'desc': 'Covering complet voiture moyenne', 'ht': 650, 'ttc': 773.5, 'unite': 'Véhicule', 'type': 'service'},
                {'ref': 'COV-ROOF01', 'desc': 'Wrap toit carbone', 'ht': 180, 'ttc': 214.2, 'unite': 'Pièce', 'type': 'service'},
                {'ref': 'COV-HOOD01', 'desc': 'Wrap capot', 'ht': 160, 'ttc': 190.4, 'unite': 'Pièce', 'type': 'service'},
            ],
            'impression': [
                {'ref': 'IMP-CV01', 'desc': 'Cartes de visite (500 ex)', 'ht': 55, 'ttc': 65.45, 'unite': 'Lot', 'type': 'service'},
                {'ref': 'IMP-CV02', 'desc': 'Cartes de visite (1000 ex)', 'ht': 85, 'ttc': 101.15, 'unite': 'Lot', 'type': 'service'},
                {'ref': 'IMP-FLY01', 'desc': 'Flyers A5 quadri recto-verso (500 ex)', 'ht': 120, 'ttc': 142.8, 'unite': 'Lot', 'type': 'service'},
                {'ref': 'IMP-FLY02', 'desc': 'Flyers A5 (1000 ex)', 'ht': 185, 'ttc': 220.15, 'unite': 'Lot', 'type': 'service'},
                {'ref': 'IMP-BRO01', 'desc': 'Brochure A4 16 pages (100 ex)', 'ht': 320, 'ttc': 380.8, 'unite': 'Lot', 'type': 'service'},
                {'ref': 'IMP-BRO02', 'desc': 'Brochure A4 32 pages (100 ex)', 'ht': 520, 'ttc': 618.8, 'unite': 'Lot', 'type': 'service'},
                # IMP-AFF01 et IMP-AFF02 sont des variantes du produit "Affiche" - gérées séparément
                {'ref': 'IMP-ETIQ01', 'desc': 'Étiquettes autocollantes (1000 pcs)', 'ht': 95, 'ttc': 113.05, 'unite': 'Lot', 'type': 'service'},
                {'ref': 'IMP-MENU01', 'desc': 'Menu restaurant plastifié A4', 'ht': 12, 'ttc': 14.28, 'unite': 'Pièce', 'type': 'service'},
                {'ref': 'IMP-NCR01', 'desc': 'Carnet autocopiant 50x3 feuillets', 'ht': 19, 'ttc': 22.61, 'unite': 'Pièce', 'type': 'service'},
                {'ref': 'IMP-BLOC01', 'desc': 'Bloc-notes A5 50 feuilles', 'ht': 7.5, 'ttc': 8.92, 'unite': 'Pièce', 'type': 'service'},
            ],
            'gravure': [
                {'ref': 'GRA-TRO01', 'desc': 'Tampon Trodat 4912 personnalisé', 'ht': 25, 'ttc': 29.75, 'unite': 'Pièce'},
                {'ref': 'GRA-TRO02', 'desc': 'Tampon Trodat 4926 grand', 'ht': 48, 'ttc': 57.12, 'unite': 'Pièce'},
                {'ref': 'GRA-TRO03', 'desc': 'Encreur Trodat noir', 'ht': 9, 'ttc': 10.71, 'unite': 'Pièce'},
                {'ref': 'GRA-PLA01', 'desc': 'Plaque gravée plexiglas 20x30 cm', 'ht': 35, 'ttc': 41.65, 'unite': 'Pièce'},
                {'ref': 'GRA-PLA02', 'desc': 'Plaque inox gravée 10x20 cm', 'ht': 42, 'ttc': 49.98, 'unite': 'Pièce'},
                {'ref': 'GRA-TROP01', 'desc': 'Trophée acrylique personnalisé', 'ht': 65, 'ttc': 77.35, 'unite': 'Pièce'},
                {'ref': 'GRA-MED01', 'desc': 'Médaille gravée métal', 'ht': 18, 'ttc': 21.42, 'unite': 'Pièce'},
                {'ref': 'GRA-ETIQ01', 'desc': 'Étiquettes industrielles gravées', 'ht': 2.8, 'ttc': 3.33, 'unite': 'Pièce'},
                {'ref': 'GRA-LETT3D01', 'desc': 'Lettres 3D PVC 10 mm (par lettre)', 'ht': 7.5, 'ttc': 8.92, 'unite': 'Lettre'},
            ],
            'decoration': [
                {'ref': 'DEC-TOT01', 'desc': 'Totem intérieur 2 m', 'ht': 95, 'ttc': 113.05, 'unite': 'Pièce'},
                {'ref': 'DEC-CPT01', 'desc': 'Comptoir promo pliable', 'ht': 185, 'ttc': 220.15, 'unite': 'Pièce'},
                {'ref': 'DEC-PRES01', 'desc': 'Présentoir plexi A4', 'ht': 22, 'ttc': 26.18, 'unite': 'Pièce'},
                {'ref': 'DEC-STAND01', 'desc': 'Stand d\'exposition 3x3 avec visuel', 'ht': 850, 'ttc': 1011.5, 'unite': 'Pièce'},
                {'ref': 'DEC-ADH01', 'desc': 'Adhésifs muraux décoratifs (m²)', 'ht': 26, 'ttc': 30.94, 'unite': 'm²'},
                {'ref': 'DEC-LETTLUM01', 'desc': 'Lettres lumineuses (par caractère)', 'ht': 70, 'ttc': 83.3, 'unite': 'Pièce'},
            ],
            'textile': [
                {'ref': 'TEX-TEE01', 'desc': 'T-shirt coton 150 g impression DTG', 'ht': 22, 'ttc': 26.18, 'unite': 'Pièce'},
                {'ref': 'TEX-TEE02', 'desc': 'T-shirt coton 180 g impression DTG', 'ht': 26, 'ttc': 30.94, 'unite': 'Pièce'},
                {'ref': 'TEX-POLO01', 'desc': 'Polo brodé logo', 'ht': 35, 'ttc': 41.65, 'unite': 'Pièce'},
                {'ref': 'TEX-SWE01', 'desc': 'Sweat capuche impression', 'ht': 49, 'ttc': 58.31, 'unite': 'Pièce'},
                {'ref': 'TEX-CAPB01', 'desc': 'Casquette brodée', 'ht': 18, 'ttc': 21.42, 'unite': 'Pièce'},
                {'ref': 'TEX-TABL01', 'desc': 'Tablier personnalisé', 'ht': 22, 'ttc': 26.18, 'unite': 'Pièce'},
                {'ref': 'TEX-VEST01', 'desc': 'Veste softshell personnalisée', 'ht': 95, 'ttc': 113.05, 'unite': 'Pièce'},
            ],
            'cadeaux': [
                {'ref': 'CAD-CAD01', 'desc': 'Cadre photo A4 bois personnalisé', 'ht': 28, 'ttc': 33.32, 'unite': 'Pièce'},
                {'ref': 'CAD-TOI01', 'desc': 'Tableau toile 50x70 cm', 'ht': 75, 'ttc': 89.25, 'unite': 'Pièce'},
                {'ref': 'CAD-PLX01', 'desc': 'Tableau plexiglas 40x60 cm', 'ht': 95, 'ttc': 113.05, 'unite': 'Pièce'},
                {'ref': 'CAD-ALB01', 'desc': 'Album photo 20 pages', 'ht': 65, 'ttc': 77.35, 'unite': 'Pièce'},
                {'ref': 'CAD-BOX01', 'desc': 'Boîte cadeau personnalisée', 'ht': 15, 'ttc': 17.85, 'unite': 'Pièce'},
                {'ref': 'CAD-CARV01', 'desc': 'Carte de vœux premium', 'ht': 4.5, 'ttc': 5.35, 'unite': 'Pièce'},
            ],
            'services': [
                {'ref': 'SER-DES01', 'desc': 'Création visuel + maquette produit', 'ht': 40, 'ttc': 47.6, 'unite': 'Prestation', 'type': 'service'},
                {'ref': 'SER-LOGO01', 'desc': 'Création de logo professionnel', 'ht': 120, 'ttc': 142.8, 'unite': 'Prestation', 'type': 'service'},
                {'ref': 'SER-BRND01', 'desc': 'Mini charte graphique (logo/couleurs/typo)', 'ht': 240, 'ttc': 285.6, 'unite': 'Prestation', 'type': 'service'},
                {'ref': 'SER-MAQU01', 'desc': 'Maquette enseigne / covering (3 vues)', 'ht': 95, 'ttc': 113.05, 'unite': 'Prestation', 'type': 'service'},
                {'ref': 'SER-RET01', 'desc': 'Retouche photo avancée (pack 10)', 'ht': 60, 'ttc': 71.4, 'unite': 'Prestation', 'type': 'service'},
                {'ref': 'SER-POSE01', 'desc': 'Pose d\'enseigne (équipe 2 pers / h)', 'ht': 65, 'ttc': 77.35, 'unite': 'Heure', 'type': 'service'},
                {'ref': 'SER-POSE02', 'desc': 'Pose adhésifs/vitrophanie (m²)', 'ht': 18, 'ttc': 21.42, 'unite': 'm²', 'type': 'service'},
                {'ref': 'SER-LIV01', 'desc': 'Livraison Grand Tunis', 'ht': 15, 'ttc': 17.85, 'unite': 'Prestation', 'type': 'service'},
                {'ref': 'SER-DEV01', 'desc': 'Déplacement &amp; métrage sur site', 'ht': 25, 'ttc': 29.75, 'unite': 'Prestation', 'type': 'service'},
            ],
            'consommables': [
                {'ref': 'CON-VINPOL-137', 'desc': 'Vinyle polymère 137 cm (rouleau 50 m)', 'ht': 260, 'ttc': 309.4, 'unite': 'Rouleau'},
                {'ref': 'CON-VINMON-100', 'desc': 'Vinyle monomère 100 cm (rouleau 50 m)', 'ht': 150, 'ttc': 178.5, 'unite': 'Rouleau'},
                {'ref': 'CON-LAMG-137', 'desc': 'Laminat brillant 137 cm (50 m)', 'ht': 210, 'ttc': 249.9, 'unite': 'Rouleau'},
                {'ref': 'CON-LAMM-137', 'desc': 'Laminat mat 137 cm (50 m)', 'ht': 210, 'ttc': 249.9, 'unite': 'Rouleau'},
                {'ref': 'CON-ALU-3MM', 'desc': 'Plaque Dibond 3 mm 300x150 cm', 'ht': 185, 'ttc': 220.15, 'unite': 'Plaque'},
                {'ref': 'CON-PVC-5MM', 'desc': 'PVC expansé 5 mm 300x200 cm', 'ht': 95, 'ttc': 113.05, 'unite': 'Plaque'},
                {'ref': 'CON-ACR-3MM', 'desc': 'Plexiglas transparent 3 mm 200x300 cm', 'ht': 220, 'ttc': 261.8, 'unite': 'Plaque'},
                {'ref': 'CON-INK-CMYK', 'desc': 'Encre CMYK éco-solvant (1 L)', 'ht': 75, 'ttc': 89.25, 'unite': 'Litre'},
                {'ref': 'CON-INK-WH', 'desc': 'Encre blanche UV (1 L)', 'ht': 180, 'ttc': 214.2, 'unite': 'Litre'},
                {'ref': 'CON-TSH-180', 'desc': 'T-shirt blanc polyester 180 g (vierge)', 'ht': 6.5, 'ttc': 7.73, 'unite': 'Pièce'},
                {'ref': 'CON-MUG-BL', 'desc': 'Mug blanc 330 ml (vierge)', 'ht': 3.2, 'ttc': 3.81, 'unite': 'Pièce'},
                {'ref': 'CON-GOURDE-ALU', 'desc': 'Gourde alu 600 ml (vierge)', 'ht': 9.5, 'ttc': 11.3, 'unite': 'Pièce'},
                {'ref': 'CON-PAPER-PP', 'desc': 'Papier photo 200 g (rouleau 610 mm)', 'ht': 55, 'ttc': 65.45, 'unite': 'Rouleau'},
                {'ref': 'CON-TRANS-HTV', 'desc': 'Flex textile (HTV) 50 cm x 25 m', 'ht': 120, 'ttc': 142.8, 'unite': 'Rouleau'},
                {'ref': 'CON-THERM-TAPE', 'desc': 'Ruban thermique sublimation', 'ht': 9, 'ttc': 10.71, 'unite': 'Rouleau'},
                {'ref': 'CON-PLA-LAS', 'desc': 'Plaque acrylique laser 3 mm 60x90 cm', 'ht': 18, 'ttc': 21.42, 'unite': 'Plaque'},
                {'ref': 'CON-BOIS-MDF', 'desc': 'Plaque MDF 3 mm 60x90 cm', 'ht': 11, 'ttc': 13.09, 'unite': 'Plaque'},
                {'ref': 'CON-TAMP-PLA', 'desc': 'Monture Trodat 4912 vide', 'ht': 12.5, 'ttc': 14.88, 'unite': 'Pièce'},
                {'ref': 'CON-ADH-DEP', 'desc': 'Vinyle dépoli (sablé) 122 cm (50 m)', 'ht': 210, 'ttc': 249.9, 'unite': 'Rouleau'},
                {'ref': 'CON-ACC-RACLE', 'desc': 'Raclette pose + feutrine', 'ht': 5.5, 'ttc': 6.54, 'unite': 'Pièce'},
            ],
        }

    def get_categories_info(self):
        """Retourne les informations sur les catégories"""
        return {
            'sublimation': {'name': 'Sublimation', 'icon': 'fa-magic', 'count': 20},
            'goodies': {'name': 'Goodies', 'icon': 'fa-gift', 'count': 14},
            'signaletique': {'name': 'Signalétique', 'icon': 'fa-map-signs', 'count': 16},
            'covering': {'name': 'Covering Véhicules', 'icon': 'fa-car', 'count': 7},
            'impression': {'name': 'Impression', 'icon': 'fa-print', 'count': 11},  # 12 - 1 (Affiche A1/A2 devient 1 produit avec variantes)
            'gravure': {'name': 'Gravure & CNC', 'icon': 'fa-bolt', 'count': 9},
            'decoration': {'name': 'Décoration & PLV', 'icon': 'fa-paint-brush', 'count': 6},
            'textile': {'name': 'Textile & Broderie', 'icon': 'fa-tshirt', 'count': 7},
            'cadeaux': {'name': 'Cadeaux Personnalisés', 'icon': 'fa-heart', 'count': 6},
            'services': {'name': 'Services Graphiques & Installation', 'icon': 'fa-cogs', 'count': 9},
            'consommables': {'name': 'Consommables Production', 'icon': 'fa-cube', 'count': 20},
        }
    
    def get_products_with_variants(self):
        """Retourne un dictionnaire des produits qui doivent avoir des variantes
        Format: {base_name: [list of variant data]}
        """
        return {
            'Affiche': [
                {'ref': 'IMP-AFF01', 'desc': 'Affiche A2', 'ht': 8.5, 'ttc': 10.12, 'unite': 'Pièce', 'type': 'service', 'variant': 'A2'},
                {'ref': 'IMP-AFF02', 'desc': 'Affiche A1', 'ht': 14, 'ttc': 16.66, 'unite': 'Pièce', 'type': 'service', 'variant': 'A1'},
            ],
            # Ajouter d'autres produits avec variantes ici si nécessaire
        }

