# Offre parures : calculs vérifiés avec les tarifs officiels Branvas (23/11/2026)

## Décision
**2 parures : la 2e à −30 % · 3 parures : la 3e à −50 %** (par groupe de 3, sur la moins chère). Pas de cadeau. Joaillerie 925 exclue.
Remplace « 2e −50 % / 3e offerte + collier offert », qui **perdait de l'argent** au scénario pessimiste (trio −5 à −15 € par commande).

## Tarifs Branvas utilisés (FAQ officielle, articles 12875190, 12241736, 13048992, 15948119, 18510957, 12241451)
- Coût unitaire : visible seulement dans ton compte (ex. Molten Art 16,87 $, Solar Sphere 22,01 $, Emerald Dreams 29,41 $ pour un prix conseillé de 89 $).
- Livraison : 8,99 $ **par commande**, quel que soit le nombre de pièces, droits et taxes d'import compris (DDP). Branvas ne facture pas de taxe.
- Frais de carte facturés par Branvas : 2,9 % + 0,30 $ sur chaque commande que Branvas te facture.
- Tout est facturé en **dollars** : ta banque convertit (compter 1 à 2 % de frais de change, sauf carte en dollars).
- Abonnement Growth 29 $/mois (75 produits publiés : 30 parures + pièces seules, ça tient).
- Retours pour changement d'avis : **jamais repris par Branvas**, à ta charge (rétractation de 14 jours obligatoire dans l'UE).
- Marge brute officielle au prix conseillé : 60 à 70 % en général (Prism Party 59–73 %, Liquid Sculpture 53–74 %, Moissanite 42–80 %).

## Ce qui reste par commande (calculateur `woocommerce/finances/calcul-marge.py`)
Coûts inclus : coût Branvas + 8,99 $ + 2,9 % + 0,30 $, change, frais de paiement de la boutique, cotisations micro-entreprise 12,4 % du chiffre d'affaires, retours (6 à 10 % des commandes).

| Parure | 1 parure | 2 parures | 3 parures |
|---|---|---|---|
| Molten Art 49 € (coût réel), central | 19 € | 28 € | 44 € |
| Molten Art 49 €, pessimiste | 16 € | 22 € | 36 € |
| Solar Sphere 69 € (coût réel), central | 27 € | 46 € | 70 € |
| Solar Sphere 69 €, pessimiste | 23 € | 38 € | 59 € |

Chaque palier rapporte plus que le précédent, dans les deux scénarios : **tu es gagnant à chaque commande**. C'est la condition qu'on garde pour toute future offre (le calculateur affiche « palier moins rentable » sinon).

## Règle de prix
1. **Jamais en dessous du prix conseillé Branvas converti en euros** (prix conseillé en $ ÷ 1,0968), sauf raison précise. Exemple : Emerald Dreams, conseillé 89 $ ≈ 81 € → vendu 79 € (et non 45 €, qui ne rapportait que ≈ 6 €).
2. Bénéfice net minimum visé : **15 € pour une commande d'1 article** au scénario pessimiste.
3. Les pièces seules à 29–39 € sont sous ce seuil si elles sont achetées seules : à vendre au prix conseillé ou en complément d'une parure.
4. Si le chiffre d'affaires dépasse le seuil de la franchise de TVA, la TVA de 20 % mange environ 1/6 du prix : il faudra augmenter les prix (exemple : Solar Sphere seule passe de 27 € à 17 € de bénéfice).

## Publicité
Le bénéfice d'une commande, c'est le maximum que tu peux payer en pub pour l'obtenir (coût par achat). Avec ces marges : 15 à 25 € pour une parure seule, 35 à 60 € pour un trio. Couper toute pub dont le coût par achat dépasse le bénéfice moyen par commande.

## À faire
- Relever dans ton compte Branvas le **coût unitaire et le prix conseillé des 36 articles** et les noter dans `woocommerce/finances/couts-branvas.csv`, puis relancer `python3 woocommerce/finances/calcul-marge.py` (et `--scenario pessimiste`). Toute ligne avec une alerte doit être repricée avant le lancement.
- WooCommerce : Réglages > Produits > CHARMED PARIS : mode « Paliers », 30 %, 3e parure 50 %, catégories éligibles sans Joaillerie 925, cadeau vide.
