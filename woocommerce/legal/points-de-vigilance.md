# Points de vigilance juridiques : CHARMED PARIS (dropshipping de bijoux)

*Document interne, ne pas publier. Ce document est une aide à la mise en conformité. Il ne remplace pas la consultation d'un avocat ou d'un expert-comptable. Textes vérifiés au 22/11/2026 : revérifier les articles sur Légifrance avant la mise en ligne.*

## 1. Vous êtes le vendeur, pas Branvas

- **Responsabilité de plein droit** envers la cliente pour toute l'exécution du contrat : livraison, retard, perte, défaut (art. L. 221-15 du code de la consommation). « C'est le fournisseur » n'est jamais une défense.
- **L'écart entre Branvas et le droit français est à votre charge.** Branvas ne couvre que l'article endommagé, défectueux ou erroné signalé **dans les 10 jours** suivant la livraison, et rembourse en crédit Branvas. Il refuse tout retour pour changement d'avis. Restent donc à votre charge :
  - la **rétractation de 14 jours** (L. 221-18) : remboursement intégral, frais de livraison initiaux compris, et pièce retournée chez vous ;
  - la **garantie légale de conformité de 2 ans** (L. 217-3, présomption de 24 mois, L. 217-7) : tout défaut signalé après J+10 est à vos frais ;
  - le colis perdu ou « livré mais non reçu » : le risque reste sur vous jusqu'à la prise de possession physique (L. 216-4), alors que Branvas ne garantit pas un colis marqué « livré ».
  
  **À intégrer dans les prix et la trésorerie** : taux de retour à provisionner, coût d'un envoi retour, stock de pièces retournées à revendre.
- **Ne jamais publier les modèles de politiques Branvas tels quels** (« no change-of-mind returns », 10 jours) : ce serait une clause illicite et une pratique commerciale trompeuse (L. 121-2 et suivants).
- **Adresse de retour en France obligatoire en pratique** : [À COMPLÉTER]. Domicile, local ou prestataire de réception des retours.
- **Annulation** : Branvas ne peut plus annuler une commande payée. Désactivez l'auto-fulfillment si vous voulez une fenêtre de correction d'adresse. La cliente peut se rétracter même avant l'expédition : le colis partira quand même, à vos frais.

## 2. Délais et informations à afficher

- **Délai ou date de livraison obligatoire avant la commande** (L. 111-1, 3° ; L. 221-5). À défaut, le maximum légal est de 30 jours (L. 216-1). Afficher **« 4 à 9 jours ouvrés en France »** (90 % des colis, selon Branvas) et un **engagement maximal** tenable : [À COMPLÉTER : 15 jours ouvrés, par exemple]. Ne jamais promettre moins que Branvas.
- **Pas de livraison express ni de date garantie** : n'en proposer aucune au checkout.
- **Pays d'expédition** : l'expédition depuis l'étranger (États-Unis ou Chine, hors UE) doit apparaître sans ambiguïté (fiche produit, page livraison, CGV art. 6). Le taire alors que la marque s'appelle CHARMED PARIS peut constituer une **omission trompeuse** (L. 121-3).
- **Origine et « Paris »** : ne jamais écrire ni suggérer « fabriqué à Paris », « Made in France », « créé dans notre atelier parisien » ou « artisanal », sauf si c'est exact (L. 121-2, 2°, b : tromperie sur l'origine). Une formule comme « sélectionné et pensé à Paris » n'est acceptable que si c'est vrai.
- **Noël** : afficher la date limite Branvas, **commande au plus tard le 4 décembre 2026** pour l'Europe, et dire qu'au-delà rien n'est garanti. Ne jamais garantir « livré avant Noël » au-delà de cette date.
- **Bouton de rétractation** obligatoire depuis le **19 juin 2026** (ordonnance n° 2026-2 du 5 janvier 2026, art. L. 221-21 ; décret n° 2026-3). Amende administrative pouvant aller jusqu'à 15 000 € pour une personne physique et 75 000 € pour une personne morale. WooCommerce ne le propose pas en natif : à développer, ou extension à vérifier.
- **Bouton de commande** : renommer « Commander » en **« Commander avec obligation de paiement »** (L. 221-14), sinon la commande peut être frappée de nullité.
- **Téléphone obligatoire au checkout** (exigé par DHL et la douane hors US/UK). À rendre obligatoire dans WooCommerce et à mentionner dans la politique de confidentialité.

## 3. Sécurité des produits : GPSR, REACH, nickel, plomb, cadmium

- **Vous êtes l'opérateur économique responsable dans l'UE** (règlement (UE) 2023/988, dit « GPSR », applicable depuis le 13 décembre 2024). En vendant sous votre propre marque, vous êtes même **réputée fabricant** (art. 13 GPSR) : analyse des risques, documentation technique, traçabilité, rappels, déclaration des accidents sur Safety Business Gateway. Branvas, société américaine, ne remplit pas ce rôle. Il est possible de mandater un représentant autorisé dans l'UE.
- **Fiches produits en ligne** (art. 19 GPSR) : nom, marque et adresse postale et électronique de l'opérateur responsable (CHARMED PARIS), photo et identification du produit (référence SKU), avertissements et consignes de sécurité en français. **Sur le produit ou l'emballage** : nom, adresse, référence ou lot (art. 9). Vérifier que l'emballage Branvas à votre logo peut porter ces mentions, sinon ajouter une étiquette ou une carte.
- **REACH, annexe XVII** (règlement (CE) n° 1907/2006) : **nickel**, libération inférieure ou égale à 0,5 µg/cm²/semaine pour les parties en contact prolongé avec la peau (entrée 27) ; **cadmium**, 0,01 % en poids dans les parties métalliques (entrée 23) ; **plomb**, moins de 0,05 % en poids (entrée 63). La DGCCRF relève régulièrement des bijoux fantaisie non conformes et exige du vendeur les **preuves de conformité** (rapports d'analyse).
- **Branvas n'a pas de rapport global** : les tests sont faits par SKU, sur devis (300 à 800 $ par article, environ 15 jours ouvrés). **À faire** : demander les rapports existants pour les 30 SKU sélectionnés, et faire tester en priorité les pièces en laiton et alliage de zinc portées sur la peau (boucles d'oreilles, colliers).
- **Allégations interdites sans rapport par SKU** : « sans nickel », « sans plomb », « hypoallergénique », « certifié », « testé dermatologiquement », « poinçonné ». « Nickel-safe », toléré par Branvas pour les États-Unis, est à proscrire en français.

## 4. Dénominations : métaux, dorure, pierres, perles

- **Dorure** : en dessous de 3 microns, ou d'une épaisseur non certifiée, seule la dénomination **« doré »** est permise. Pas de **« plaqué or »** (3 µm minimum), ni de **« vermeil »** (argent recouvert d'au moins 5 µm d'or à 750 ‰ minimum), ni d'« or » seul. Branvas ne publie pas l'épaisseur. **« Doré à l'or fin »** : « or fin » désigne l'or pur (24 carats). N'employer cette formule que si la fiche Branvas du produit indique une dorure 24 carats, sinon écrire « doré à l'or 18 carats » ou « doré ». Le carat est à relever produit par produit.
- **En anglais, sur un site qui vise la France** : éviter « gold-plated », équivalent de « plaqué or », bien que Branvas l'accepte. Préférer « gold-tone, electroplated with [18k] gold » ou « gold-dipped ».
- **Argent 925** : la garantie des métaux précieux relève désormais du **code de commerce, articles L. 831-1 à L. 835-6**, depuis le 1er juillet 2025 (anciennement art. 521 et suivants du CGI). L'importateur d'ouvrages en argent venant de pays tiers doit en principe les présenter à la douane et faire apposer le **poinçon de responsabilité** et le **poinçon de garantie** français. Les ouvrages de **moins de 30 g d'argent** sont dispensés du poinçon de garantie. La marque « 925 » apposée par le fabricant n'est **pas** un poinçon au sens français.
  - **[À VÉRIFIER auprès du service de la garantie (douane)]** : statut d'importateur quand Branvas expédie en DDP directement à la cliente, et poids de chaque pièce 925.
  - En attendant, écrire « **argent 925** » ou « **estampillé 925** », jamais « poinçonné ».
- **Pierres et perles** (décret n° 2002-65 du 14 janvier 2002) :
  - la moissanite de laboratoire doit être qualifiée de **« moissanite synthétique »** (« créée en laboratoire » peut compléter, pas remplacer). Le poids « DEW » doit être expliqué ;
  - la zircone cubique doit être nommée **« oxyde de zirconium »** ou « zircone ». **« Zircon »** désigne une pierre naturelle différente : à éviter ;
  - les perles se nomment **« perles de culture d'eau douce »**, jamais « perles fines » ni « naturelles ». « Perle d'imitation » quand la fiche Branvas dit *simulated* ;
  - le certificat GRA n'existe que pour les moissanites de 0,1 ct et plus. Ne pas annoncer « certifiée » pour les autres.
- **Aucune parure n'est en acier** : jamais « waterproof », « ne craint pas l'eau » ni « ne noircit pas ». Toujours « à garder au sec ».

## 5. Prix, prix barrés et promotions

- **Prix TTC en euros**, frais de livraison affichés avant le paiement (L. 112-1 ; arrêté du 3 décembre 1987). Si vous êtes en franchise en base de TVA, mention « TVA non applicable, art. 293 B du CGI » et aucun affichage « TVA 20 % ».
- **Prix barré** : le prix de référence est le **prix le plus bas pratiqué par vous sur les 30 jours précédant la réduction** (L. 112-1-1). Pour une réduction progressive, le prix de référence reste celui d'avant la première réduction. Conséquences :
  - **pas de prix barré au lancement** ni pour le Black Friday du 27/11/2026 si le produit n'a pas été vendu 30 jours au prix barré ;
  - **ne jamais barrer le « prix conseillé » Branvas** (prix en dollars américains jamais pratiqué en France) : pratique trompeuse (L. 121-2) ;
  - conserver l'historique des prix (capture ou export WooCommerce).
- **« 2e parure −15 % » et « livraison offerte dès X € »** : licites si les conditions sont claires et appliquées automatiquement. En cas de rétractation partielle, préciser le remboursement (CGV art. 9.5).
- **Aucun faux signal d'urgence** : ni « stock limité », ni compte à rebours fictif, ni « 12 personnes regardent ce produit » (pratiques réputées trompeuses, L. 121-4).
- **Avis** : seulement de vraies clientes, via un outil de collecte vérifiée. Informer sur le contrôle des avis (L. 111-7-2 et D. 111-17). Aucun avis acheté, rédigé ou filtré. Branvas n'en fournit pas.

## 6. Influence commerciale (loi n° 2023-451 du 9 juin 2023, modifiée par l'ordonnance n° 2024-978 du 6 novembre 2024)

- Chaque contenu sponsorisé doit porter la mention **« Publicité »** ou **« Collaboration commerciale »**, claire et visible pendant toute la durée du contenu. Un bijou offert en échange d'un post est une rémunération en nature. Son absence est une pratique commerciale trompeuse : jusqu'à 2 ans d'emprisonnement et 300 000 € d'amende.
- **Contrat écrit** avec l'influenceuse au-delà du seuil fixé par décret [À VÉRIFIER : seuil en vigueur]. Il doit prévoir l'objet, la rémunération, le droit applicable et le respect de la loi. **L'annonceur (vous) est solidairement responsable** des dommages causés aux tiers par l'influenceuse dans l'exécution du contrat.
- Interdire contractuellement les allégations listées aux sections 3 et 4 (« hypoallergénique », « waterproof », « or »), les faux codes promo « limités » et les avis déguisés.

## 7. Factures, TVA, douane

- **Factures** : émettre une facture conforme à chaque commande. Mentions obligatoires : art. 242 nonies A de l'annexe II au CGI et L. 441-9 du code de commerce. Extension WooCommerce de factures PDF numérotées en continu.
- **Facturation électronique** : réception obligatoire pour toutes les entreprises assujetties depuis le **1er septembre 2026**. Émission et **e-reporting des ventes aux particuliers** à partir du **1er septembre 2027** pour les PME, TPE et micro-entreprises. Choisir une plateforme agréée.
- **TVA sur la vente** : à votre charge (collecte et déclaration). Branvas ne s'occupe que de l'import (DDP, aucun IOSS à fournir). **[À VÉRIFIER avec l'expert-comptable]** :
  - qui est juridiquement importateur ;
  - le traitement de la TVA d'import payée par Branvas (non déductible chez vous) ;
  - le lieu de taxation de la vente ;
  - le seuil de 10 000 € de ventes à distance intra-UE (guichet OSS) si vous ouvrez d'autres pays ;
  - pour le Royaume-Uni : **immatriculation à la TVA britannique dès la première vente** (colis de 135 £ ou moins). Ne pas ouvrir le Royaume-Uni sans l'avoir réglé.
- **Petits colis** : depuis le 1er juillet 2026, l'UE applique un droit forfaitaire de 3 € par catégorie d'article aux envois de 150 € ou moins, et la douane française annonce des frais de traitement de 2 € depuis le 1er novembre 2026. **[À VÉRIFIER]** : faire confirmer **par écrit** par Branvas que son DDP couvre ces montants. Sinon, ils seraient réclamés à la cliente, en contradiction avec « droits inclus », et resteraient à vos frais.

## 8. Données personnelles

- Transfert des données de livraison vers **Branvas (États-Unis)**. **[À VÉRIFIER]** : certification Data Privacy Framework sur dataprivacyframework.gov. À défaut, DPA avec clauses contractuelles types (décision (UE) 2021/914) avant le lancement. Faire de même pour Klaviyo, Stripe et l'outil d'avis.
- Registre des traitements (art. 30 RGPD), même simplifié.
- Bandeau cookies conforme : refus aussi simple qu'acceptation, aucun pixel avant consentement. Voir politique-cookies.md.
- Newsletter : consentement explicite (case non cochée), double opt-in recommandé, désinscription en un clic.

## 9. Divers

- **Statut juridique** : une micro-entreprise doit faire figurer « EI » sur tous les documents. Pour une société : capital, RCS. **[À COMPLÉTER]**.
- **Marque CHARMED PARIS** : non vérifiée. Recherche d'antériorité puis dépôt INPI ou EUIPO (classes 14 et 35) **avant** d'investir en publicité. Un nom contenant « PARIS » doit rester non trompeur quant à l'origine des produits.
- **Visuels Branvas** : utilisables seulement pendant l'abonnement. Prévoir vos propres photos.
- **Langue** : CGV, fiches produits et garanties en français (loi n° 94-665 du 4 août 1994). La version anglaise est une traduction ; la version française fait foi.
- **Accessibilité** : les services de commerce en ligne relèvent de l'European Accessibility Act depuis le 28 juin 2025. Les micro-entreprises (moins de 10 salariés et chiffre d'affaires ou bilan de 2 M€ au plus) en sont exemptées. À anticiper dès que vous dépassez ces seuils.
- **Médiateur** : adhésion obligatoire **avant** la première vente (L. 612-1, L. 616-1). Amende administrative en cas de manquement (L. 641-1). Choisir un médiateur référencé par la CECMC (liste sur economie.gouv.fr/mediation-conso). Il n'est plus nécessaire d'afficher le lien vers la plateforme européenne RLL, supprimée le 20 juillet 2025 (règlement (UE) 2024/3228).
- **Ventes hors de France** : dans l'UE, la loi impérative du pays de la cliente s'applique (Rome I, art. 6). Pour le Royaume-Uni, voir la note UK dans les documents anglais (Consumer Contracts Regulations 2013, Consumer Rights Act 2015).
