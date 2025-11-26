# -*- coding: utf-8 -*-
"""
Script pour générer le template XML du catalogue complet
"""

# Données du catalogue
catalogue = {
    "Sublimation": [
        ("SUB-T01", "T-shirt blanc polyester 180 g", 12, 14.28, "Pièce"),
        ("SUB-T02", "T-shirt technique sport 150 g", 15, 17.85, "Pièce"),
        ("SUB-T03", "T-shirt enfant polyester", 10, 11.9, "Pièce"),
        ("SUB-POL01", "Polo polyester sublimable", 22, 26.18, "Pièce"),
        ("SUB-SWE01", "Sweat capuche sublimable", 48, 57.12, "Pièce"),
        ("SUB-CAS01", "Casquette blanche sublimable", 9, 10.71, "Pièce"),
        ("SUB-MUG01", "Mug blanc 330 ml", 7, 8.33, "Pièce"),
        ("SUB-MUG02", "Mug magique noir 330 ml", 9.5, 11.3, "Pièce"),
        ("SUB-MUG03", "Mug intérieur coloré 330 ml", 8.5, 10.12, "Pièce"),
        ("SUB-GOU01", "Gourde alu 600 ml", 16, 19.04, "Pièce"),
        ("SUB-THER01", "Bouteille isotherme 500 ml", 28, 33.32, "Pièce"),
        ("SUB-CUS01", "Coussin 40x40 cm + housse", 18, 21.42, "Pièce"),
        ("SUB-MAT01", "Tapis de souris 22x18 cm", 5.5, 6.54, "Pièce"),
        ("SUB-PK01", "Porte-clés métal sublimable", 4.2, 5, "Pièce"),
        ("SUB-PLAALU01", "Plaque aluminium 20x30 cm", 19, 22.61, "Pièce"),
        ("SUB-PUZ01", "Puzzle A4 80 pièces", 11, 13.09, "Pièce"),
        ("SUB-COQ01", "Coque téléphone (modèles courants)", 12, 14.28, "Pièce"),
        ("SUB-TAB01", "Tablier cuisine polyester", 14, 16.66, "Pièce"),
        ("SUB-TOTE01", "Tote bag polyester sublimable", 9, 10.71, "Pièce"),
        ("SUB-HOR01", "Horloge murale sublimable", 22, 26.18, "Pièce"),
    ],
    "Goodies": [
        ("GOO-PEN01", "Stylo publicitaire plastique", 0.85, 1.01, "Pièce"),
        ("GOO-PEN02", "Stylo métal gravé laser", 3.2, 3.81, "Pièce"),
        ("GOO-NOTE01", "Bloc-notes A5 80 pages", 4.8, 5.71, "Pièce"),
        ("GOO-USB16", "Clé USB 16 Go personnalisée", 18, 21.42, "Pièce"),
        ("GOO-USB32", "Clé USB 32 Go personnalisée", 24, 28.56, "Pièce"),
        ("GOO-LANY01", "Lanière badge imprimée", 2.9, 3.45, "Pièce"),
        ("GOO-BADG01", "Badge rond 58 mm", 2.5, 2.97, "Pièce"),
        ("GOO-POW01", "Powerbank 5000 mAh personnalisée", 39, 46.41, "Pièce"),
        ("GOO-UMBR01", "Parapluie publicitaire auto", 22, 26.18, "Pièce"),
        ("GOO-BOTT01", "Gobelet réutilisable 30 cl", 2.2, 2.62, "Pièce"),
        ("GOO-CAP01", "Casquette promo 5 panneaux", 6.5, 7.73, "Pièce"),
        ("GOO-BAG01", "Sac shopping non tissé", 3.8, 4.52, "Pièce"),
        ("GOO-MAG01", "Magnet 7x7 cm", 1.6, 1.9, "Pièce"),
        ("GOO-LIGH01", "Briquet imprimé", 1.2, 1.43, "Pièce"),
    ],
    # ... autres catégories à ajouter
}

def generate_product_card(ref, desc, prix_ht, prix_ttc, unite):
    return f'''                                <div class="col-lg-4 col-md-6">
                                    <div class="card h-100 shadow-sm border">
                                        <div class="card-body">
                                            <h6 class="card-title fw-bold text-primary">{ref}</h6>
                                            <p class="card-text small mb-2">{desc}</p>
                                            <p class="mb-1"><strong>Prix HT:</strong> {prix_ht} TND</p>
                                            <p class="mb-1"><strong>Prix TTC:</strong> <span class="text-success">{prix_ttc} TND</span></p>
                                            <span class="badge bg-secondary">{unite}</span>
                                        </div>
                                    </div>
                                </div>'''

# Cette fonction peut être utilisée pour générer le XML complet
# mais pour l'instant, je vais créer le template directement dans le fichier XML


