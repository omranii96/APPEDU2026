# CHARMED PARIS — Offres, panier moyen et rentabilité publicitaire

> Version du 23/11/2026. Chiffres Branvas : `source/FAITS-BRANVAS.md` (prioritaire). Tous les calculs sont reproductibles avec les hypothèses du §1.
> Cohérence avec le simulateur budget déjà réalisé : marge ≈ 24 €/commande avec TVA (≈ 35 € en franchise), panier moyen ≈ 72 €. Ici, le scénario de référence **B (Solar Sphere 69 € + 4,90 € de port = 73,90 €)** donne **26,39 €** avec TVA et **37,48 €** en franchise. Ce sont les mêmes ordres de grandeur.

---

## 1. Hypothèses

| Poste | Valeur retenue | Statut |
|---|---|---|
| Change | **1 € = 1,16 $** (1 $ = 0,862 €). Sensibilité à 1,05 et 1,25 au §3.3 | [hyp.], à mettre à jour au moment du lancement |
| Coût parure Molten Art (JSGRQR) | 16,87 $ = 14,54 € (prix conseillé Branvas 46 $) | **[fait]** |
| Coût Solar Sphere (JS1AQ5) | 22,01 $ = 18,97 € | [fait probable] |
| Coût parure Éclat à 79 € | 29 $ (ratio coût/prix conseillé de Molten = 36,7 %, appliqué au prix médian Prism Party de 79 $) | [hyp.] à relever dans Branvas |
| Coût parure Joaillerie 925 à 189 € | 80 $ (même ratio sur le prix médian Moissanite Spark de 219 $) | [hyp.] à relever |
| Livraison Branvas | **8,99 $ par commande** = 7,75 €, quel que soit le nombre de pièces ; packaging de marque **inclus** (boîte à bijoux à ruban, pochette velours, chamoisine, bordereau sans prix) | **[fait]** |
| Frais Branvas | **2,9 % + 0,30 $** sur ce que Branvas te facture (coût + 8,99 $) | **[fait]** |
| Frais de paiement côté boutique | **2 % + 0,25 €** du montant TTC (mélange : cartes UE Stripe/WooPayments ≈ 1,5 % + 0,25 €, PayPal ≈ 2,9 % + 0,35 €) | [hyp.] à confirmer selon les grilles en vigueur |
| Frais bancaires de change sur les débits USD | 0 € (carte multidevise type Wise/Revolut) ; sinon +1 à 2 % du coût Branvas | [hyp.] |
| TVA | 20 % incluse dans le prix TTC (régime réel ou dépassement de la franchise) ; variante franchise au §3.4 | Légal ; régime à valider avec un comptable |
| **Rétractation 14 j** (à ta charge : Branvas ne reprend pas les changements d'avis [fait]) | **8 % des commandes** [hyp.]. Tu rembourses tout ce que la cliente a payé (port aller compris). Tu perds la parure, les 8,99 $ et les frais de paiement. Tu revends ou réutilises la pièce retournée à 30 % de son coût (échange, stock de remplacement, photos). **Frais de retour à la charge de la cliente** (autorisé si c'est indiqué avant la commande) | [hyp.] + décision recommandée (§5) |
| SAV garantie légale 2 ans, hors fenêtre Branvas de 10 jours | 2 % du CA HT | [hyp.] |
| Défauts, casse et erreurs signalés sous 10 jours | Couverts par Branvas (crédit ou remplacement) [fait] ; coût ≈ 0 € si la réclamation est faite à temps | [fait] |
| Coûts fixes mensuels | Hors calcul unitaire (§8) | — |

**Formule** (par commande) :
`Marge de contribution = CA HT − coût parures − 7,75 € − frais (boutique + Branvas) − SAV − coût attendu de rétractation`
`Coût attendu de rétractation = 8 % × CA HT − 8 % × 30 % × coût parures`
**Marge de contribution = CPA maximal** (au-delà, chaque commande issue d'une pub fait perdre de l'argent dès la 1re commande).
**ROAS seuil = CA / marge de contribution**, donné pour 2 définitions de la « valeur » : TTC payé, ou **valeur HT des produits hors port** (c'est la valeur recommandée pour le tracking, cf. `tracking-et-tests.md`).

---

## 2. Tableau de rentabilité par scénario (TVA 20 %, change 1,16 $/€, seuil de livraison offerte 89 €)

| # | Scénario | CA TTC payé | dont port | CA HT | Parures | Livraison Branvas 8,99 $ | Frais paiement (toi + Branvas) | Rétractation 8 % (hyp.) | SAV garantie 2 % | **Marge de contribution = CPA max** | Marge / CA HT | ROAS seuil sur TTC | ROAS seuil sur valeur HT produits |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A0 | 1 Molten Art 49 €, livraison offerte | 49,00 € | 0,00 € | 40,83 € | 14,54 € | 7,75 € | 2,14 € | 2,92 € | 0,82 € | **12,67 €** | 31 % | 3,87 | 3,22 |
| A | 1 Molten Art 49 € + 4,90 € de port | 53,90 € | 4,90 € | 44,92 € | 14,54 € | 7,75 € | 2,23 € | 3,24 € | 0,90 € | **16,25 €** | 36 % | 3,32 | 2,51 |
| B0 | 1 Solar Sphere 69 €, livraison offerte | 69,00 € | 0,00 € | 57,50 € | 18,97 € | 7,75 € | 2,66 € | 4,14 € | 1,15 € | **22,82 €** | 40 % | 3,02 | 2,52 |
| **B** | **1 Solar Sphere 69 € + 4,90 € de port (référence ≈ panier moyen 72 €)** | 73,90 € | 4,90 € | 61,58 € | 18,97 € | 7,75 € | 2,76 € | 4,47 € | 1,23 € | **26,39 €** | 43 % | 2,80 | 2,18 |
| C | 1 parure Éclat 79 € (coût hyp. 29 $) + 4,90 € de port | 83,90 € | 4,90 € | 69,92 € | 25,00 € | 7,75 € | 3,14 € | 4,99 € | 1,40 € | **27,64 €** | 40 % | 3,04 | 2,38 |
| D | 1 parure Joaillerie 925 à 189 € (coût hyp. 80 $) | 189,00 € | 0,00 € | 157,50 € | 68,97 € | 7,75 € | 6,51 € | 10,94 € | 3,15 € | **60,18 €** | 38 % | 3,14 | 2,62 |
| **E** | **Duo Molten 49 + Solar 69, −15 % sur la moins chère** | 110,65 € | 0,00 € | 92,21 € | 33,52 € | 7,75 € | 3,92 € | 6,57 € | 1,84 € | **38,61 €** | 42 % | 2,87 | 2,39 |
| F | Duo Solar 69 + Éclat 79, −15 % sur la moins chère | 137,65 € | 0,00 € | 114,71 € | 43,97 € | 7,75 € | 4,76 € | 8,12 € | 2,29 € | **47,81 €** | 42 % | 2,88 | 2,40 |
| G | Alternative : coffret duo à prix fixe 99 € (Molten + Solar) | 99,00 € | 0,00 € | 82,50 € | 33,52 € | 7,75 € | 3,69 € | 5,80 € | 1,65 € | **30,10 €** | 36 % | 3,29 | 2,74 |
| H | Bienvenue −10 % sur Solar (62,10 € + 4,90 € de port) | 67,00 € | 4,90 € | 55,83 € | 18,97 € | 7,75 € | 2,62 € | 4,01 € | 1,12 € | **21,36 €** | 38 % | 3,14 | 2,42 |
| I | Bienvenue « livraison offerte » sur Solar | 69,00 € | 0,00 € | 57,50 € | 18,97 € | 7,75 € | 2,66 € | 4,14 € | 1,15 € | **22,82 €** | 40 % | 3,02 | 2,52 |
| K | Duo E + bienvenue −10 % cumulés | 99,59 € | 0,00 € | 82,99 € | 33,52 € | 7,75 € | 3,70 € | 5,83 € | 1,66 € | **30,53 €** | 37 % | 3,26 | 2,72 |

### CPA cible (marge nette de 10 % du CA HT conservée après la pub)

| # | A0 | A | B0 | B | C | D | E | F | G | H | I | K |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CPA cible | 8,59 € | 11,76 € | 17,07 € | 20,24 € | 20,65 €* | 44,43 € | 29,39 € | 36,34 € | 21,85 € | 15,77 € | 17,07 € | 22,23 € |
| ROAS cible (valeur HT produits) | 4,75 | 3,47 | 3,37 | 2,84 | 3,19* | 3,55 | 3,14 | 3,16 | 3,78 | 3,28 | 3,37 | 3,73 |

\*C recalculé avec le port à 4,90 € (seuil 89 €).

### Ce que dit le tableau
1. **Le CPA maximal d'une commande d'une seule parure est de 16 à 28 €.** Le benchmark de CPA publicitaire du simulateur est de **40 à 100 €**. **La prospection payante n'est donc pas rentable à la 1re commande** sur une parure seule, quel que soit l'univers sous 90 €. C'est le risque n°1 du projet.
2. **Le duo change l'équation** : la 2e parure ajoute **+12 à +22 € de marge** (E − B = +12,21 € ; E − A = +22,36 € ; F − B = +21,41 €) parce que les 8,99 $ de livraison ne sont payés qu'une fois [fait]. C'est le meilleur levier de rentabilité disponible.
3. **La Joaillerie 925 (D) est la seule ligne qui supporte un CPA de 40 à 60 €.** Elle mérite des campagnes dédiées (cadeau, fiançailles, anniversaire) [hyp. : coût à relever].
4. **Molten Art à 49 € ne doit pas être poussé seul en pub** (CPA max 12,67 € s'il est livré gratuitement). Il sert de 2e pièce idéale dans un duo, ou peut être repositionné à 59 € (CPA max → 23,55 €).
5. Cible pondérée (mix [hyp.] : 10 % A, 40 % B, 20 % C, 15 % E, 10 % F, 5 % D) : **panier moyen 91,54 €, marge 31,29 €, ROAS seuil TTC 2,93**. C'est l'objectif à atteindre avec les leviers des §4 à §7.

---

## 3. Sensibilités

### 3.1 Prix de vente (+10 €)
| Variante | CA TTC | Marge | ROAS seuil TTC |
|---|---:|---:|---:|
| Molten Art 59 € (+ port) | 63,90 € | 23,55 € | 2,71 |
| Solar Sphere 79 € (+ port) | 83,90 € | 33,69 € | 2,49 |
| Duo Solar 79 + Éclat 89 −15 % | 156,15 € | 61,31 € | 2,55 |

+10 € de prix public = **+7 € de marge environ** par commande. À tester avant d'acheter du trafic. Les prix conseillés Branvas en USD (Prism Party médiane 79 $) sont compatibles avec 69–89 €. [hyp.]

### 3.2 Taux de rétractation
| Taux | A | B | E |
|---|---:|---:|---:|
| 4 % | 17,87 € | 28,63 € | 41,89 € |
| **8 % (base)** | 16,25 € | 26,39 € | 38,61 € |
| 15 % | 13,41 € | 22,48 € | 32,86 € |

Chaque tranche de +1 point de rétractation coûte environ **0,5 € par commande**. Photos fidèles (portées, échelle) et dimensions exactes = moins de déception = moins de retours.

### 3.3 Change EUR/USD
| 1 € = | A | B | E |
|---|---:|---:|---:|
| 1,05 $ | 13,85 € | 23,53 € | 34,21 € |
| **1,16 $** | 16,25 € | 26,39 € | 38,61 € |
| 1,25 $ | 17,89 € | 28,36 € | 41,62 € |

Les coûts sont en USD et les ventes en EUR : une baisse de l'euro de 10 % coûte environ **3 € par commande**. Revoir les prix si le change passe sous 1,08 $ [hyp.].

### 3.4 Franchise en base de TVA (si éligible : à valider avec un comptable)
| # | A0 | A | B0 | B | C | D | E | F |
|---|---|---|---|---|---|---|---|---|
| Marge | 20,02 € | 24,33 € | 33,17 € | **37,48 €** | 35,91 €* | 88,53 € | 55,20 € | 68,45 € |
| ROAS seuil TTC | 2,45 | 2,22 | 2,08 | 1,97 | 2,20* | 2,13 | 2,00 | 2,01 |

\*C livré gratuitement dans ce sous-calcul. La franchise ajoute environ **+11 € par commande**, mais elle a un plafond de CA et la mention « TVA non applicable, art. 293 B du CGI » est obligatoire. Les ventes vers d'autres pays de l'UE au-delà de 10 000 €/an déclenchent la TVA du pays de destination (guichet OSS). [à vérifier avec un comptable]

### 3.5 Marchés EN (indicatif)
| Marché | Prix | CA en € | Marge | ROAS seuil |
|---|---|---:|---:|---:|
| US, Solar à 79 $ (hors sales tax, sans port) | 79 $ | 68,10 € | 31,70 € | 2,15 |
| US, Molten à 59 $ | 59 $ | 50,86 € | 21,15 € | 2,40 |
| UK, Solar à 65 £ TTC (1 £ = 1,15 € [hyp.], TVA UK 20 %) | 65 £ | 74,75 € | 26,27 € | 2,85 |

Le marché US est le plus rentable par commande (pas de TVA, délai de 3 à 8 jours [fait]). Le UK suppose une immatriculation TVA UK [à vérifier] et se fait **sans la ligne Joaillerie 925** (poinçon UK obligatoire au-delà de 7,78 g). L'Irlande et le Benelux suivent les calculs EUR ci-dessus (même TVA si sous le seuil OSS).

---

## 4. Seuil de livraison offerte : décision

### Règle Branvas
« Seuil 20–30 % au-dessus du panier moyen » [fait]. Avec un panier moyen ≈ 72 € : **86 à 94 €** → **89 €**.

### Pourquoi 89 € fonctionne particulièrement bien ici
- Les parures seules coûtent 49–89 € (hors 925) : une cliente qui achète une parure paie 4,90 € de port, sauf sur le haut de gamme Couleur précieuse et la 925.
- **Le duo le moins cher (49 € + 49 € × 0,85 = 90,65 €) dépasse 89 €** : tout panier de 2 parures est livré gratuitement. Le message devient **« 2 parures : −15 % sur la 2e et livraison offerte »**, une seule règle facile à retenir.
- 4,90 € couvre 63 % des 7,75 € de livraison Branvas : la cliente ne paie pas le vrai coût, ce qui reste juste et compétitif.

### Comparatif des 3 options (commande d'une parure)
| Option | Commande A (Molten) | Commande B (Solar) | Seuil de bascule |
|---|---|---|---|
| Livraison offerte partout | 12,67 € | 22,82 € | — |
| 4,90 € sous 89 € (**recommandé**) | 16,25 € | 26,39 € | La livraison offerte partout ne gagne que si elle augmente le taux de conversion de **plus de 28 %** (A) ou de **plus de 16 %** (B) [calcul] |
| Forfait 4,90 € toujours | Idem en dessous de 89 €, mais on perd le levier duo | — | Déconseillé |

**À tester** (test n°5, `tracking-et-tests.md`) : 89 € vs livraison offerte partout. Le test se fait **par périodes successives**, pas en séparant les visiteuses au même moment : afficher 2 prix de livraison différents en même temps est risqué (transparence des prix, perception d'injustice).

**Mise à jour de la maquette** : `free = after>=50` → `free = after>=89 || n>=2` ; `shipc = 4.9` conservé ; message `ship-txt` → « Ajoute une 2e parure : −15 % et livraison offerte ».

---

## 5. Rétractation : la politique qui limite les pertes sans dark pattern

| Décision | Recommandation | Impact |
|---|---|---|
| Délai | 14 jours légaux à partir de la réception (ne pas allonger au lancement) | — |
| Frais de retour | **À la charge de la cliente**, indiqués avant la commande sur la fiche, au checkout et dans les CGV (sinon ils restent à ta charge) | Sans cette mention, environ 5–7 € par retour à ta charge [hyp. tarif La Poste/Colissimo] |
| Adresse de retour | **La tienne, en France** (jamais celle de Branvas [fait]) | Retour peu coûteux pour la cliente |
| Remboursement | Prix + port aller standard, sous 14 jours ; tu peux attendre la réception du colis retourné ou une preuve d'envoi | Légal |
| Pièces retournées | Contrôle, re-scellage, stock « échange/remplacement » ou ventes privées « pièces contrôlées » clairement étiquetées | Récupération ≈ 30 % du coût [hyp.] |
| Boucles d'oreilles | Exception « hygiène » (art. L221-28 5°) **seulement si** un scellé d'hygiène est présenté comme tel avant l'achat et a été ouvert. Pour une parure (collier + boucles vendus ensemble), son application est incertaine : **ne pas l'utiliser sans avis d'un juriste** | [à vérifier] |
| Défaut / casse / erreur | Demander les photos à la cliente **sous 10 jours** et les transmettre à Branvas (fenêtre de couverture [fait]) ; au-delà, c'est la garantie légale à ta charge | Le provisionnement de 2 % couvre ce risque |

---

## 6. « 2e parure −15 % » face aux alternatives

| Mécanique | Marge (exemple Molten + Solar) | Lisibilité | Risque | Verdict |
|---|---|---|---|---|
| **2e parure −15 % (sur la moins chère)** | **38,61 €** (E) | Bonne, déjà dans la maquette | Faible ; règle à écrire noir sur blanc | **Garder** comme offre permanente |
| Coffret duo à prix fixe 99 € | 30,10 € (G) | Très bonne | −8,51 € de marge par rapport à E ; catalogue figé | Seulement en édition saisonnière (Fête des mères), sur des paires choisies |
| −20 € dès 2 parures | Molten + Solar : 118 − 20 = 98 € → ≈ 29 € de marge [calcul approché] | Bonne | Plus généreux que −15 % sur les petits paniers | Variante de test seulement |
| Cadeau offert (pochette velours, chamoisine) | — | — | **Impossible à présenter comme un « cadeau »** : ces éléments sont déjà inclus dans chaque colis [fait]. Les annoncer comme offerts pour une condition serait trompeur | **Non** : les présenter comme inclus |
| Emballage premium payant | — | — | Pas d'option par commande chez Branvas (packaging unique inclus ; sets supplémentaires à 3,75 $ seulement avec les échantillons ; pas de message cadeau) [fait] | **Non** |
| Carte message personnalisée | — | — | Pas de champ message ; carte personnalisée réservée au plan VIP (149 $/mois) [fait] | Plus tard, si le plan VIP devient rentable |
| 3e parure −25 % | Panier ≥ 150 € | Moyenne | Complexité | Après 3 mois de données |

**Limite à annoncer honnêtement** : un duo = **un colis et une seule boîte à bijoux** ; la 2e parure voyage dans son sachet scellé [fait]. Pour offrir à 2 personnes avec 2 boîtes, il faut 2 commandes (et le −15 % ne s'applique pas). Le dire en FAQ et dans le mini-panier (« Pour 2 cadeaux séparés, passe 2 commandes ») évite les déceptions et les retours.

### Upsells et cross-sells (avant paiement uniquement)
| Endroit | Suggestion | Règle |
|---|---|---|
| Fiche produit | « Complète ta parure : −15 % sur la 2e » | Même univers ou prix ±20 € |
| Mini-panier | 3 vignettes au prix remisé | Exclure ce qui est déjà au panier ; parures sous 70 € en priorité (marge incrémentale max) |
| Fiche femme (oct.–déc., févr.) | « Pour lui » : ligne homme | Saisonnier |
| Panier ≥ 1 parure dorée | Montée en gamme Joaillerie 925 | Seulement si la différence de prix est ≤ 2× |
| Post-achat (e-mail J+30) | Univers complémentaire | Pas de code immédiat |

---

## 7. Offre de bienvenue (newsletter)

| Option | Coût pour toi (commande B) | Attractivité | Recommandation |
|---|---|---|---|
| **−10 % 1re commande** (maquette, **retenu dans `crm/flows.md`** : code unique, 14 jours, non cumulable) | −5,03 € (26,39 → 21,36 €) | Forte | **Offre de lancement** (cohérence CRM). **Non cumulable** avec la 2e parure −15 % (le cumul donnerait 30,53 € au lieu de 38,61 € sur un duo) |
| Livraison offerte sur la 1re commande | −3,57 € (26,39 → 22,82 €) | Bonne, et elle supprime la 1re cause d'abandon | **Variante à tester** (test n°10) : 1,46 € moins chère par commande ; déjà utilisée par le CRM pour la réactivation |
| Rien (contenus seulement) | 0 € | Faible | Inscriptions faibles |

Règles : code unique par e-mail (Brevo/Klaviyo), valable 30 jours, une utilisation, non cumulable, conditions affichées dans le pop-up. **Pas de faux compte à rebours** dans le pop-up ; une date de fin réelle est permise.

---

## 8. Noël 2026 (aujourd'hui : 23/11)

| Date | Événement | Action |
|---|---|---|
| 20/11 → 24/12 | **Packaging de Noël automatique et sans surcoût** (papier cadeau, ruban, décorations, carte de Noël) [fait] | Le montrer (photo `pack-noel-f.webp` / `pack-noel-h.webp`) : c'est un argument, pas une remise. Coût supplémentaire : 0 € |
| 27/11 (Black Friday) → 30/11 (Cyber Monday) | Pic de trafic | Pas de fausse remise. Le site est neuf, donc **aucun « prix barré »** possible sans prix antérieur réellement pratiqué (règle des 30 jours, `legal-checklist.md`). Pousser plutôt le duo « 2 parures : −15 % + livraison offerte », une offre permanente et vraie |
| **Vendredi 4/12** | **Date limite de commande pour Noël en Europe et au Canada** [fait] | Bandeau, fiches, checkout, e-mail le 1/12 (« Plus que 3 jours pour une livraison avant Noël » : c'est une date réelle, pas un compte à rebours artificiel) |
| Mardi 8/12 | Date limite US, UK, Australie [fait] | Version EN |
| 5/12 → 24/12 | Livraison avant Noël non garantie | Mettre en avant l'**e-carte cadeau** (envoyée par e-mail, valable 12 mois [hyp.]) ; garder les ventes « pour soi » ; ne rien promettre sur les délais |

Rentabilité de Noël : le packaging festif ne change pas le coût (déjà inclus). Le levier est le taux de conversion des cadeaux et la part de duos (2 cadeaux) : viser 25 % de paniers à 2 parures ou plus [hyp.].

---

## 9. Coûts fixes et point mort (indicatif)

| Poste | €/mois | Statut |
|---|---:|---|
| Branvas Growth 29 $ | 25 | [fait] |
| Hébergement WooCommerce managé | 25–35 | [hyp.] |
| Plugins payants (traduction, checkout, tracking, cache) amortis | 25–40 | [hyp.], cf. `stack-plugins.md` |
| E-mail (Brevo/Klaviyo, palier de départ) | 0–25 | [à vérifier] |
| Médiateur de la consommation | 5–40 | [à vérifier] (50–500 €/an selon les sources) |
| Assurance RC pro, banque, comptable | 40–90 | [hyp.] |
| **Total** | **≈ 120–255 €/mois** | |

Point mort **sans pub** = 120–255 € / 26,39 € ≈ **5 à 10 commandes par mois** (scénario B). Avec la pub, il faut une **marge après pub positive** : `(marge − CPA réel) × commandes ≥ coûts fixes`. Avec un CPA réel de 40 € et le mix cible (31,29 €), chaque commande issue de la pub perd environ 9 €. D'où les priorités : **acquisition organique et UGC, capture d'e-mails, reciblage (CPA plus bas), duos et 925 en pub, hausse de prix testée**.

### Valeur client (LTV) à 12 mois
| Taux de réachat à 12 mois [hyp.] | 10 % | 20 % | 30 % |
|---|---:|---:|---:|
| Marge cumulée par cliente (mix cible, réachat via e-mail sans coût pub) | 34,42 € | 37,55 € | 40,68 € |

Même avec 30 % de réachat, le CPA acceptable reste **sous 41 €** : le bas de la fourchette du benchmark. **Il ne faut pas monter le budget pub tant que le CPA mesuré dépasse la colonne « CPA max » du scénario réellement vendu.**
