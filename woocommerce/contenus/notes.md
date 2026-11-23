# CHARMED PARIS · Notes de production des contenus

Fichier interne : prix proposés, mode d'import, et liste consolidée des points « à confirmer ». Sources : `BRIEF.md`, `source/FAITS-BRANVAS.md` (prioritaire), FAQ Branvas, photos `branvas-photos/`.

## 1. Prix de vente : PROPOSITIONS à valider

Grille du brief respectée : Sculpture 49–59 € · Éclat 59–79 € · Couleur précieuse 69–89 € · Joaillerie 925 149–249 € · Mixte 49 €. Prix TTC, TVA 20 % incluse. Les parures à 3 ou 4 pièces sont placées en haut de leur fourchette.

| SKU | Parure | Univers | Pièces | Prix proposé |
|---|---|---|---|---|
| JSGRQR | Molten Art | Sculpture | 2 | 49 € |
| JSM1BZ | Crumpled Cube | Sculpture | 2 | 49 € |
| JS8445 | Celestial Star Moon | Sculpture | 2 | 49 € |
| JS411P | Fluid Dreams | Sculpture | 2 | 55 € |
| JS63WT | Liquid Gold Cascade | Sculpture | 2 | 55 € |
| JSG813 | Liquid Art | Sculpture | 2 | 59 € |
| JS0S3W | Baroque Pearl Flow | Sculpture | 2 | 59 € |
| JSVKMZ | Cosmic Circle | Mixte | 2 | 49 € |
| JSCT1F | Lunar Goddess | Mixte | 2 | 49 € |
| JS4P8D | Petal Bloom | Éclat | 2 | 59 € |
| JS4AH6 | Radiant Circle | Éclat | 2 | 59 € |
| JSFAV7 | Geometric Luxe | Éclat | 2 | 65 € |
| JS2KBV | Wave Luxe | Éclat | 2 | 65 € |
| JS1AQ5 | Solar Sphere | Éclat | 2 | 69 € |
| JS63VP | Golden Hour | Éclat | 2 | 69 € |
| JS5N68 | Emerald Cut Halo | Éclat | 2 | 69 € |
| JSQS6W | Shell Glow | Éclat | 2 | 69 € |
| JS4EXR | Crescent Glow | Éclat | 3 | 75 € |
| JSC940 | Golden Square | Éclat | 2 | 75 € |
| JSJB3S | Golden Luxe | Éclat | 2 | 79 € |
| JS3GGZ | Emerald Square | Couleur précieuse | 2 | 69 € |
| JS9XM9 | Linear Luxe | Couleur précieuse | 2 | 69 € |
| JS0DGC | Celestial Cascade | Couleur précieuse | 2 | 79 € |
| JS4EPC | Rose Empress | Couleur précieuse | 2 | 79 € |
| JSX3G6 | Royal Sapphire | Couleur précieuse | 2 | 79 € |
| JSB541 | Pink Pavé | Couleur précieuse | 3 | 85 € |
| JSDYG2 | Emerald Dreams | Couleur précieuse | 3 | 89 € |
| JS1PPS | Golden Radiance | Joaillerie 925 | 2 | 149 € |
| JSSFYS | Blush Dreams | Joaillerie 925 | 4 | 189 € |
| JSDQA1 | Heart Symphony | Joaillerie 925 | 4 | 229 € |

**Contrôle de marge (seul coût connu, Molten Art à 49 €)** : 40,83 € HT. Coût 16,87 $ + livraison 8,99 $ + frais 2,9 % + 0,30 $ ≈ 26,91 $ ≈ 24,50 € (hypothèse 1 € = 1,10 $). Marge brute ≈ 16 € HT avant publicité et frais de paiement Woo, et ≈ 9 € si c'est la 2e parure à −15 %. Les 29 autres coûts sont à relever dans le compte Branvas avant publication ; ne pas publier un prix sans ce contrôle, surtout pour la Joaillerie 925 (PVC Branvas médian 219 $).

**Seuil de livraison offerte** : la règle Branvas conseille un seuil 20–30 % au-dessus du panier moyen. Avec 5 parures à 49 €, un seuil à 50 € pousse à prendre une 2e parure : cohérent avec « 2e parure −15 % ». Frais sous 50 € : proposition 4,90 €, à valider.

## 2. Import WooCommerce

- `produits-woocommerce.csv` (FR) et `produits-woocommerce-en.csv` (EN) : UTF-8, virgule, colonnes officielles + `Meta: _charmed_a_confirmer`. Type = simple, **Published = -1 (brouillon)** : passer à 1 une fois les points à confirmer levés.
- Catégories : univers (`Parures > …` / `Sets > …`) + budget (`Cadeaux > Moins de 50 €` / `Gifts > Under €50`…), créées automatiquement par l'importateur.
- **Branvas crée déjà les produits dans Woo** (même SKU attendu). Importer ensuite avec « Mettre à jour les produits existants » (correspondance SKU) et, à l'étape de correspondance des colonnes, mettre **Images** sur « Ne pas importer » pour ne pas effacer les photos synchronisées. Vérifier d'abord que les SKU créés par Branvas sont bien les SKU `JS…` du bundle.
- **Version anglaise** : les deux fichiers ont les mêmes SKU. Un import natif du fichier EN écraserait le FR. Il faut passer par l'outil de traduction choisi (WPML + WooCommerce Multilingual, ou Polylang for WooCommerce) et lier chaque produit EN à son original FR. Choix du plugin à confirmer.
- La colonne `Meta: _charmed_a_confirmer` est une méta privée (préfixe `_`) : invisible côté client. La vider une fois les points levés.

## 3. Points « à confirmer » consolidés

### Juridique / marque
1. Adresse de retour en France pour les rétractations : **[À COMPLÉTER]**.
2. Mode de prise en charge des frais de retour (étiquette fournie ou remboursement sur justificatif).
3. Clause boucles d'oreilles / hygiène pour la rétractation : à valider avec un conseil.
4. Formulaire type de rétractation à publier ; CGV, mentions légales, RGPD/cookies.
5. GPSR : CHARMED PARIS est l'opérateur économique responsable dans l'UE (ou mandater un représentant).
6. Marque INPI/EUIPO non vérifiée ; Instagram @charmedparis à tester.
7. Noms anglais contenant « Emerald » et « Sapphire » (Emerald Dreams, Emerald Square, Royal Sapphire) : pas de pierres précieuses ; textes explicites, mais envisager de renommer.
8. Aucune mention « sans nickel / sans plomb / hypoallergénique » tant qu'il n'y a pas de rapport de test par SKU (300–800 $ par article).

### Logistique / commerce
9. Frais de livraison sous 50 € (proposition 4,90 €).
10. Moyens de paiement réels (Carte, Apple Pay, PayPal annoncés dans la maquette).
11. Règle exacte de la remise « 2e parure −15 % » (la moins chère des deux ?) et plugin ; cumul ou non avec −10 % newsletter et relance panier.
12. Une parure de plusieurs pièces compte-t-elle comme une seule « pièce » pour la boîte-tiroir ? (FAQ : une boîte par commande, pièces supplémentaires en sachet scellé.)
13. Conflit commercial : « 2e parure −15 % » et « une boîte par commande ». Pour deux cadeaux, conseiller deux commandes (textes déjà rédigés ainsi), ce qui fait perdre la remise. À arbitrer.
14. Délai réel d'annulation (réglage « Auto-Fulfillment » dans Branvas).
15. Packaging homme ou femme : comment est-il choisi (parures Mixte) ?
16. Papier nid d'abeille : uniquement offres Scale/VIP à Noël ; ne pas l'annoncer en standard.
17. E-mails « Expédiée » et « Livrée » : nécessitent un plugin de suivi (Woo n'a pas ces statuts en natif).
18. Date limite de commande pour la fête des mères (aucune date officielle).
19. Maquette d'accueil à corriger : boîte blanche → beige métallisé ; case « carte Ouvre-moi » à supprimer ; Royal Sapphire sans bague ; Emerald Square = petites créoles, pas puces ; « Argent massif » → « Argent 925 » ; titre « Le collier et ses boucles » faux pour Golden Radiance ; réassurance « 3 à 9 jours » → « 4 à 9 jours ouvrés ».

### Produits (détail dans la colonne Meta de chaque ligne)
20. Pour les 30 : relever sur la fiche Branvas le carat de la dorure, longueurs de chaîne, dimensions, poids, type d'attache des boucles, coût d'achat.
21. Liquid Sculpture : descriptions « gold-toned » sans matière ; confirmer laiton doré (FAQ) ; **JS0S3W Baroque Pearl Flow** annoncée « eco-zinc alloy », métal non listé dans la FAQ : base et finition argentée à confirmer (texte client neutre).
22. Perles (JSG813, JS0S3W) : FAQ = perles de culture d'eau douce ; vérifier que les fiches ne disent pas « simulated ».
23. Pierres à identifier : pierre verte (JSDYG2), « crystals » (JSVKMZ), « crystal accents » (JS4EPC), « clear crystal halos » (JSX3G6), « square golden stones » (JSC940), « white beads » (JS4P8D), dôme bronze (JS1AQ5), dôme gris (JSQS6W), résine (JS411P).
24. Finitions « white gold plated » / « rose gold » (JS0DGC, JSDYG2, JS9XM9, JSX3G6, JSQS6W, JSB541) : nature exacte.
25. JS63VP Golden Hour : « 14K gold plated » à vérifier avant mention du carat.
26. JS8445 : nature de la finition argentée (bicolore).
27. Bagues (JSDYG2, JSB541, JSSFYS, JS1PPS, JSDQA1) : réglables ou en tailles US ? JSDYG2 : bague visible sur la photo mais non citée par Branvas. JS4EXR : réglable (confirmé), mesures à relever.
28. Joaillerie 925 : toutes les pierres sont-elles des moissanites (pavages compris) ? lesquelles dépassent 0,1 ct (certificat GRA) ?
29. **JS1PPS Golden Radiance : la photo montre collier + bague, aucune boucle d'oreille.**
30. Classement : JS0DGC Celestial Cascade et JS9XM9 Linear Luxe ont des pierres incolores : plutôt Éclat que Couleur précieuse.
31. Breloques en forme de lettre sur les chaînes de JS3GGZ et JS2KBV : lesquelles ?
32. Matière des cordons (JSVKMZ, JSCT1F).
