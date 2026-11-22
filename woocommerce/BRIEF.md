# CHARMED PARIS — brief commun (site WooCommerce réel)

> **MISE À JOUR (prioritaire)** :
> 1. **Site bilingue français + anglais** (FR par défaut, EN complet : contenus, SEO, emails, légal, maquettes). Prévoir l'outil multilingue (WPML/Polylang/TranslatePress à recommander), hreflang, URLs `/en/`.
> 2. **Informations réelles uniquement** : lire `woocommerce/source/FAITS-BRANVAS.md` (FAQ officielle Branvas, prioritaire sur ce brief) et les articles complets dans `woocommerce/source/branvas-faq/`. Corrections clés : expédition depuis États-Unis/Chine (pas d'entrepôt UE), DHL, France 4–9 jours ouvrés, pas d'express, retours Branvas = seulement endommagé/défectueux/erroné sous 10 jours (la rétractation UE 14 j est à la charge du marchand), pas de « sans nickel/hypoallergénique » dans l'UE sans rapport, perles = perles de culture d'eau douce véritables sauf mention contraire, date limite Noël Europe = 4 décembre 2026, GPSR = le marchand est responsable UE.

Document de référence pour tout le travail de préparation du site. Les faits ci-dessous sont vérifiés ; tout ce qui n'y figure pas est à marquer « à confirmer ».

## Marque
- Nom : **CHARMED PARIS** (toujours avec PARIS). Logo : wordmark Didone (Bodoni Moda), le C et le D sont deux parenthèses qui encadrent « HARME » = un écrin qui s'ouvre ; « PARIS » en dessous, espacé.
- Sens : « charmée » + « charm » (breloque) + porte-bonheur. Cible : femmes d'abord (25–45 ans, cadeau et achat pour soi), mixte possible (petite ligne homme).
- Signature : « Ouvre. Laisse-toi charmer. » Ton : tutoiement, phrases courtes, chaleureux, jamais mièvre, jamais de superlatifs creux.
- Palette : velours #1A1015, grenat #7A1F3A, or doux #A9813F / or clair #E9CB8F, porcelaine #F4F2F5, poudre #D9C6CC. Typo : Bodoni Moda (titres, logo), Jost (texte), DM Mono (détails).
- Domaines libres au 22/11/2026 : charmedparis.com, charmedparis.fr, charmed-paris.com/.fr. Marque INPI/EUIPO **non vérifiée** (à faire).
- Instagram @charmed_paris est **pris** par un autre compte ; @charmedparis à tester.

## Offre : uniquement des parures (bundles)
- Fournisseur : **Branvas** (dropshipping marque blanche, Cupertino). 81 bundles (SKU préfixe `JS`), sélection de **30** pour CHARMED PARIS : voir `branvas-photos/bundles.csv` (colonne `selection_charmed`, `univers`, `description_photo` = description Branvas en anglais, fiable pour les matières).
- 5 univers : Sculpture (7, Liquid Sculpture, alliage zinc/laiton doré), Éclat (11, Prism Party, laiton plaqué/doré + zircons), Couleur précieuse (7, Prism Party), Joaillerie 925 (3, Moissanite Spark, argent 925 + moissanite), Mixte (2, sur cordon).
- Prix conseillés Branvas (USD) par collection : Liquid Sculpture 26–76 (méd. 39) ; Prism Party 29–189 (méd. 79) ; Moissanite Spark 69–1036 (méd. 219).
- Seul coût réel connu : **Molten Art (JSGRQR)** coût 16,87 $, prix conseillé 46 $, marge 29,13 $. Solar Sphere (JS1AQ5) : 22,01 $ (probablement coût unitaire). Les autres coûts sont à relever dans le compte Branvas.
- Prix de vente visés (exemples maquette, à valider) : Sculpture 49–59 € ; Éclat 59–79 € ; Couleur précieuse 69–89 € ; Joaillerie 925 149–249 € ; Mixte 49 €.

## Logistique Branvas (faits)
- Livraison forfaitaire **8,99 $ par commande**, DDP (droits payés), 100+ pays. Préparation 1–3 jours ; UE 3–9 jours ouvrés.
- Packaging à ton logo (offres payantes) : coffret d'envoi blanc logo dans le couvercle, papier nid d'abeille, boîte cadeau blanche ruban chocolat à cœurs dorés, pochette velours, chamoisine, carte de remerciement. Version homme (noir, pochette cuir, écrin cadre). **Noël : packaging festif offert du 20 novembre au 24 décembre.**
- Offres Branvas : Growth 29 $/mois (75 produits), Scale 79 $ (150), VIP 149 $ (300, carte insert personnalisée).
- WooCommerce : connexion par clé API REST (lecture/écriture), aucun plugin. Produits créés en natif (variations, images, poids), stock synchronisé, seules les commandes payées (« En cours ») partent, suivi écrit dans la commande. Retours gérés par le marchand. Woo 3.5+, HTTPS obligatoire.

## Contraintes légales / honnêteté (non négociables)
- Aucune parure n'est en acier : **toutes « à garder au sec »**, ne jamais écrire « waterproof » / « ne craint pas l'eau ».
- « Plaqué or » est réglementé en France (≥ 3 microns) : sans épaisseur confirmée, écrire **« doré à l'or fin »** ou « doré ». « Vermeil » = argent + ≥ 5 µm d'or 18 ct : ne pas l'utiliser.
- Pierres : zircons / oxydes de zirconium ; moissanite pour la ligne 925 ; perles « simulées » quand Branvas l'indique ; perles de Liquid Art Pearl = nature **à confirmer**.
- Jamais d'avis, de chiffres de ventes, de « stock limité », de compte à rebours ou de presse inventés. Les avis viendront d'un vrai outil (Judge.me, etc.).
- Vente à distance UE : rétractation 14 jours, garantie légale de conformité 2 ans, mentions légales, CGV, RGPD/cookies (CNIL), prix TTC en euros (TVA 20 %).

## Ce qui existe déjà dans le dépôt
- `charmed-paris/charmed-site.html` : maquette HTML de la page d'accueil (intro 3D Three.js au scroll, carrousel de coffrets photo, « La file des parures » focus/file/grille avec étiquette ticket, bandeau défilant, packagings réels, panier fonctionnel avec « 2e parure −15 % » et livraison offerte dès 50 €).
- `charmed-paris/charmed-paris.html` : dossier de marque.
- `charmed-paris/img/`, `charmed-paris/cut/` (parures détourées PNG/WebP transparents), `charmed-paris/img/pack-*.webp` (packagings réels avec logo), `box-closed.webp` / `box-open.webp`.
- `branvas-photos/` : 983 photos 400×400 + `catalogue.csv` + `bundles.csv`.

## Objectif
Préparer le site WooCommerce réel avec **conversion maximale** : SEO, contenus, UX/CRO, technique, design. Marché : France d'abord (FR), euros.
