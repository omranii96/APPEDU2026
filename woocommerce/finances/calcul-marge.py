#!/usr/bin/env python3
"""Calculateur de marge CHARMED PARIS, avec les tarifs officiels Branvas.

Lit woocommerce/finances/couts-branvas.csv (coût unitaire et prix conseillé relevés dans le compte Branvas)
et calcule, pour chaque produit et chaque palier de l'offre, le bénéfice net PAR COMMANDE après :
  - coût unitaire Branvas ($) + livraison 8,99 $ par commande (DDP, emballage compris)
  - frais de carte facturés par Branvas : 2,9 % + 0,30 $ sur ce que Branvas te facture
  - conversion dollar → euro (taux + frais de change de ta banque)
  - frais de paiement de ta boutique (Stripe / WooPayments, carte européenne)
  - cotisations micro-entreprise vente de marchandises : 12,3 % + CFP 0,1 % du chiffre d'affaires
  - retours pour changement d'avis (14 jours, à ta charge : Branvas ne reprend rien)
Coût inconnu : estimé à partir de la marge brute officielle de la collection (scénario indiqué).

Usage : python3 woocommerce/finances/calcul-marge.py [--scenario pessimiste] [--tva]
"""
import csv, pathlib, sys

HERE = pathlib.Path(__file__).parent
FX = 1.0968                      # 1 € = 1,0968 $ (Banque de France, 18/11/2026) : à mettre à jour
BRANVAS_SHIP = 8.99              # $ par commande, quel que soit le nombre de pièces
BRANVAS_FEE_P, BRANVAS_FEE_F = 0.029, 0.30
URSSAF = 0.124                   # micro-entreprise, vente de marchandises (12,3 % + CFP 0,1 %)
SHIP_FEE, FREE_FROM = 4.90, 50   # ce que paie la cliente sous 50 €
OFFER = dict(d2=0.30, d3=0.50)   # 2e parure −30 %, 3e −50 %
SC = {
    # ratio = coût unitaire estimé / prix de vente converti en $, quand le coût réel n'est pas encore relevé
    'central':    dict(ratio=0.31, ratio925=0.35, fxfee=0.01, payp=0.015, payf=0.25, ret=0.06, label=6.0, recov=0.5),
    'pessimiste': dict(ratio=0.40, ratio925=0.50, fxfee=0.02, payp=0.029, payf=0.30, ret=0.10, label=6.0, recov=0.0),
}

CODE_MAX = 0.15                  # pire code promo prévu (anniversaire Le Cercle −15 % ; bienvenue et cross-sell −10 %)
MIN_NET = 15.0                   # bénéfice net minimum par commande d'un seul article (scénario central, sans code)

def prix_regle(srp_usd, cost_usd=None, eligible=True):
    """Règle de prix (prix psychologique, effet du chiffre de gauche) :
    le plus petit prix finissant par 9 (49, 59, 69, 79, 89, 99, 109, 129…) qui est >= au prix conseillé Branvas converti en €.
    Si cost_usd est donné : on monte au 9 suivant tant qu'une commande de cet article seul rapporte moins de MIN_NET (scénario central)."""
    p = int(srp_usd / FX)
    while p % 10 != 9 or p < srp_usd / FX: p += 1
    if cost_usd is not None:
        while order([(p, cost_usd, eligible)], 'central')['net'] < MIN_NET: p += 10
    return p

def order(items, sc, vat=False, code=0.0):
    """items = [(prix €, coût $, éligible)] ; code = code promo en % appliqué après l'offre. Renvoie le détail d'une commande."""
    s = SC[sc]
    items = sorted(items, key=lambda x: -x[0])
    elig = [x for x in items if x[2]]
    n = len(elig); disc = 0.0
    for g in range(0, n - 2, 3): disc += elig[g + 2][0] * OFFER['d3']
    if n % 3 == 2: disc += elig[-1][0] * OFFER['d2']
    paid = (sum(x[0] for x in items) - disc) * (1 - code)
    ttc = paid + (0 if paid >= FREE_FROM else SHIP_FEE)
    ca = ttc / 1.2 if vat else ttc
    usd = sum(x[1] for x in items) + BRANVAS_SHIP
    usd += usd * BRANVAS_FEE_P + BRANVAS_FEE_F
    branvas = usd / FX * (1 + s['fxfee'])
    pay = ttc * s['payp'] + s['payf']
    urssaf = ca * URSSAF
    before = ca - branvas - pay - urssaf
    returns = s['ret'] * (before + s['label'] + (branvas - BRANVAS_SHIP / FX) * (1 - s['recov']))
    return dict(paye=paid, ca=ca, branvas=branvas, paiement=pay, urssaf=urssaf, retours=returns, net=before - returns)

def cost_of(row, sc):
    if row['cout_unitaire_usd']:
        return float(row['cout_unitaire_usd']), True
    s = SC[sc]; price = float(row['prix_vente_eur'])
    r = s['ratio925'] if row['univers'] == 'j925' else s['ratio']
    return price * FX * r, False

def main():
    sc = 'pessimiste' if '--scenario' in sys.argv and 'pessimiste' in sys.argv else 'central'
    vat = '--tva' in sys.argv
    rows = list(csv.DictReader(open(HERE / 'couts-branvas.csv', encoding='utf-8'), delimiter=';'))
    print(f'Scénario {sc}{" · TVA 20 %" if vat else " · franchise de TVA"} · bénéfice net par commande (€)')
    print(f'« 1/2/3 » = commande de 1, 2 ou 3 fois ce produit avec l’offre ; « pire » = 3 parures (ou 1 pièce) + code −{CODE_MAX:.0%} en plus.\n')
    print(f'{"Produit":32} {"prix":>5} {"règle":>5} {"coût$":>7} {"conseillé":>9} {"1":>7} {"2":>7} {"3":>7} {"pire":>7}  alerte')
    for r in rows:
        price = float(r['prix_vente_eur']); c, real = cost_of(r, sc)
        elig = r['type'] == 'parure' and r['univers'] != 'j925'
        nets = [order([(price, c, elig)] * k, sc, vat)['net'] for k in (1, 2, 3)]
        worst = order([(price, c, elig)] * (3 if elig else 1), sc, vat, CODE_MAX)['net']
        srp = float(r['prix_conseille_usd']) / FX if r['prix_conseille_usd'] else None
        rule = prix_regle(float(r['prix_conseille_usd']), c, elig) if r['prix_conseille_usd'] else None
        warn = []
        if nets[0] < MIN_NET: warn.append(f'marge < {MIN_NET:.0f} €')
        if worst < 0: warn.append('perte avec code')
        if elig and not (nets[0] <= nets[1] <= nets[2]): warn.append('palier moins rentable')
        if srp and price < srp: warn.append(f'sous le prix conseillé ({srp:.2f} €)')
        if rule and price != rule: warn.append(f'règle : {rule} €')
        if not real: warn.append('coût estimé')
        print(f'{r["nom"][:32]:32} {price:5.0f} {(rule or 0):5} {c:7.2f} {(f"{srp:.2f} €" if srp else "-"):>9} ' + ' '.join(f'{x:7.2f}' for x in nets) + f' {worst:7.2f}  ' + ', '.join(warn))
    print('\nPrix conseillé = prix conseillé Branvas converti en €. Règle = plus petit prix en 9 au-dessus du prix conseillé (prix psychologique), relevé si un article seul rapporte moins de 15 €.')

if __name__ == '__main__':
    main()
