# Offre parures en paliers (décision du 23/11/2026, remplace « 2e parure −15 % »)

| Palier | Onglet (angle) | Ce que paie la cliente | Exemple Solar Sphere (69 €) |
|---|---|---|---|
| 1 parure | Pour toi | prix normal, livraison offerte dès 50 € | 69 € |
| 2 parures | Une pour toi, une à offrir | la moins chère à **−50 %** | 103,50 € (économie 34,50 €) |
| 3 parures | Tous tes cadeaux de Noël | la moins chère **offerte** + **collier Golden Arc offert** | 138 € (économie 69 € + collier 29 €) |

Règle exacte (identique dans le prototype `site/assets/js/app.js` et le thème `inc/commerce.php`, mode `tiers`) : parures éligibles triées par prix décroissant, par groupes de 3 ; la moins chère de chaque groupe complet est offerte ; s'il reste 2 parures hors groupe, la moins chère des deux est à −50 %. Le collier cadeau est ajouté une fois, dès 3 parures. **Joaillerie 925 exclue** (coût argent + moissanite) : la configurer via « Catégories éligibles ».

Onglets d'angle : l'onglet du duo reprend la phrase « Pour l'offrir à… » de chaque fiche produit (ex. « une pour ta tante qui porte du camel tout l'hiver »), donc chaque parure a son avatar.

## Marge par commande (hypothèses : coût parure ≈ 19 €, livraison Branvas 8,99 $ ≈ 8,20 €, frais 2,9 % + 0,30 $, franchise de TVA, collier cadeau ≈ 7 € à relever)
| Panier | Encaissé | Coûts | Marge | vs 1 parure |
|---|---|---|---|---|
| 1 × 69 € | 69 € | 19 + 8,20 + 2,30 | **≈ 39 €** | — |
| 2 × 69 € | 103,50 € | 38 + 8,20 + 3,30 | **≈ 54 €** | +38 % |
| 3 × 69 € | 138 € | 57 + 7 + 8,20 + 4,30 | **≈ 61 €** | +56 % |

À 49 € (Sculpture) : 1 = ≈ 21 € ; 2 = ≈ 26 € ; 3 = ≈ 22 €. **À surveiller** : le trio sur les parures à 49 € rapporte autant qu'une seule. Si les paniers trio à 49 € dominent, passer le cadeau à « dès 120 € » ou remplacer le collier par un cadeau moins cher.
Le panier moyen visé passe de ≈ 72 € à ≈ 105 € : c'est ce qui rend la publicité payante viable (CPA cible 40–60 €).

## Points juridiques (vérifiés contre FAITS-BRANVAS et legal/points-de-vigilance)
- Pas de prix barré de référence : on affiche le vrai prix unitaire et l'économie réelle de l'offre. Ne jamais augmenter un prix avant de lancer l'offre (L112-1-1, plus bas prix des 30 derniers jours).
- « Offerte » = vraiment 0 € sur la ligne ; conditions écrites sous l'offre et dans la FAQ.
- Pas de « le plus choisi » / « best-seller » tant qu'il n'y a pas de ventes réelles.
- Une seule boîte cadeau par commande (Branvas) : dit sur l'accueil et dans chaque fiche (« Ce que contient le colis »).
- Le collier cadeau doit exister et être vendu 29 € (pièces seules) pour afficher « valeur 29 € ».

## À faire dans WooCommerce
1. Réglages > Produits > CHARMED PARIS : mode « Paliers », pourcentage 50, catégories éligibles sans Joaillerie 925, ID produit cadeau = collier Golden Arc.
2. Créer le produit Golden Arc (JNEJ8J) dans Branvas, prix 29 €.
3. Tester : 1, 2, 3, 4, 5, 6 parures, mélange de prix, avec et sans code promo, puis vérifier que la commande remonte dans Branvas avec le collier à 0 €.
