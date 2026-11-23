# Flow emails: English

CHARMED PARIS · branch `LANGUE = en`. Same IDs as `emails-flows.md` (FR); the mechanics are in `flows.md`. Abandoned cart copy lives in `woocommerce/contenus/microcopy.md`.

## Conventions

- **Variables**: Brevo syntax (`{{ contact.PRENOM }}`; if empty, greeting becomes "Hi,"). Notes in brackets like this, **[to confirm]**, are for the team and come out before sending.
- **Sign-off**: "The CHARMED PARIS team".
- **Tone**: warm, plain, short sentences. Write the way a friend who knows jewellery would talk.
- **Banned words**: elevate, timeless, indulge, stunning, curated, treat yourself, must-have, luxury, exclusive, waterproof, hypoallergenic, nickel-free, engraving, personalised, limited stock, only X left, hurry, countdowns, made-up reviews or sales numbers.
- **Spelling**: British spelling (jewellery, colour). For US recipients, a version with US spelling (jewelry, color) is optional; one EN version is fine at launch.
- **Materials**:
  - Sculpture and Éclat: "gold-plated brass", with a real-gold finish and an anti-tarnish coating.
  - Couleur précieuse: "silver-tone finish" [to confirm per product page].
  - Joaillerie 925: "925 sterling silver and lab-grown moissanite".
  - Pearls: "cultured freshwater pearls" only if the product page says so.
  - Never "solid gold" or "vermeil".
- **Universe names**: keep the French names (Sculpture, Éclat, Couleur précieuse, Joaillerie 925, Mixte), with a short English gloss on first mention.
- **Currency**: prices shown in € [to confirm whether the site will show GBP or USD].
- **Footer** (required for CAN-SPAM in the US and PECR in the UK):
  - CHARMED PARIS · [company name, postal address in France].
  - "You're receiving this because you signed up at charmedparis.com."
  - Preferences · Unsubscribe.

**Delivery times quoted in emails** (Branvas, 90% of parcels, order to doorstep, business days):

| Destination | Delivery time |
|---|---|
| UK | 3–7 |
| US | 3–8 |
| Canada and Australia | 4–8 |
| Ireland | 5–11 |
| EU (France, Germany, Spain) | 4–9 |
| Netherlands | 4–6 |
| Italy | 3–10 |
| Rest of world | 4–12 |

One shipping method only: no express, no guaranteed date. Duties and taxes are prepaid (DDP).

---

## Welcome

### B0. Double opt-in confirmation

**Subject**: One click to confirm
**Preheader**: Your welcome code comes right after.

Hi {{ contact.PRENOM }},

Thanks for wanting to hear from us.
One last step: please confirm your email, so we know it's really you.

**[Confirm my subscription]**

Your welcome code (10% off your first set) arrives as soon as you click.
Didn't sign up? Just ignore this email and we won't write again.

The CHARMED PARIS team

### B0 bis. Reminder (48 hours later, once)

**Subject**: Your sign-up is waiting for a click
**Preheader**: No confirmation, no emails. That's the rule.

Hi,

You left your email with us two days ago. All we need is your confirmation.

**[Confirm]**

Changed your mind? Do nothing. This is the last message.

### B1. Welcome and code (straight after confirmation)

**Subject**: Welcome. Here's 10% off
**Preheader**: Open it. Let yourself be charmed.

Hi {{ contact.PRENOM }},

Welcome to CHARMED PARIS.

We only sell sets: a necklace and earrings, made to go together. No more hunting for what matches. It's already done.

Our logo says it too. The C and the D open like the two sides of a jewellery box. Your order arrives in one: a drawer-style jewellery box tied with a ribbon bearing our logo, plus a velvet pouch, a polishing cloth and a care card.

Your code, valid for 14 days on your first order:

**{{ contact.CODE_BIENVENUE }}**, 10% off
*Valid until {{ params.DATE_FIN_CODE }}. Can't be combined with other offers.*

**[See the sets]**

Speak soon,
The CHARMED PARIS team

### B1-customer. If the contact has already ordered

**Subject**: Thanks for following along
**Preheader**: New sets, care tips and holiday deadlines. That's it.

Hi {{ contact.PRENOM }},

You already know us. Thanks for joining the list too.
We'll write about new sets, care tips and order-by dates before the holidays. Once or twice a month, no more.

Choose what you get here: **[My preferences]**

The CHARMED PARIS team

### B2. The five universes (day 2)

**Subject**: Five styles. Which one is you?
**Preheader**: From sculpted gold to sterling silver.

Hi {{ contact.PRENOM }},

All our sets live in five "universes". Here's the quick tour.

**Sculpture.** Fluid shapes, like metal caught mid-pour. Gold-plated brass. Easy every day, with jeans or a dress.
**[See Sculpture]**

**Éclat (sparkle).** Gold tones and zirconia stones that catch the light. For nights out, or to lift a plain black jumper.
**[See Éclat]**

**Couleur précieuse (precious colour).** Coloured stones, green, pink or blue, set like fine jewellery. For a touch of colour near your face.
**[See Couleur précieuse]**

**Joaillerie 925 (fine jewellery).** 925 sterling silver and lab-grown moissanite. The set you keep for years, or give for an occasion that matters.
**[See Joaillerie 925]**

**Mixte.** On cord, more raw. Wear it as a pair, or on its own.
**[See Mixte]**

Not sure? Reply to this email with your go-to outfit or the occasion. A real person will answer.

Your 10% code runs until {{ params.DATE_FIN_CODE }}.

The CHARMED PARIS team

### B3. For you, or for someone else (day 5)

**Subject**: What's inside the box
**Preheader**: Pouch, cloth, care card, and nothing to pay on delivery.

Hi {{ contact.PRENOM }},

Whether your set is for you or for someone else, here's what turns up at the door.

**In the parcel**
- Your set, in our drawer-style jewellery box with a logo ribbon. Joaillerie 925 sets come in a blue velvet box instead.
- A velvet pouch to keep it in.
- A polishing cloth.
- A care card.
- A packing slip with no prices on it.

*Ordering two sets? They come in the same parcel, but there's one jewellery box per order: the second set travels in a sealed pouch. To give each one in its own box, place two separate orders (two parcels, two delivery charges).*

**Delivery**
- Tracked by DHL (USPS in the US). You'll get the tracking link by email.
- [[ by `PAYS` ]] It usually arrives within [[ 3–7 / 3–8 / 4–9 ]] business days of your order.
- Duties and taxes are already paid, so there's nothing to pay on delivery.
- Free delivery from €50 [threshold to confirm].

**If it's not the one**
- EU customers have 14 days after delivery to change their mind [returns terms for UK/US to confirm in the T&Cs].
- Legal guarantee of conformity: 2 years in the EU.

Buying a gift? Have it delivered straight to them. The parcel arrives ready to give, with no prices inside. We can't add a gift message, so send your note separately.

**[Find my set]**

The CHARMED PARIS team

### B4. Code reminder (day 11, if unused)

**Subject**: Your code is valid until {{ params.DATE_FIN_CODE }}
**Preheader**: Just a reminder, nothing more.

Hi {{ contact.PRENOM }},

A quick reminder: your welcome code **{{ contact.CODE_BIENVENUE }}** (10% off) works until {{ params.DATE_FIN_CODE }}.

In case you haven't found your set yet, here are the ones you looked at most:
[[ products block: 3 last viewed, otherwise 3 from the universe picked in the pop-up, otherwise one per universe ]]

**[Use my code]**

And if now's not the time, that's fine. We'll keep writing, without pushing.

The CHARMED PARIS team

---

## Browse abandonment

### N1. The set you looked at (+4 hours)

**Subject**: {{ params.NOM_PRODUIT }}, still here
**Preheader**: You were looking at it earlier.

Hi {{ contact.PRENOM }},

You were looking at this one:

[[ product image · {{ params.NOM_PRODUIT }} · {{ params.UNIVERS }} · €{{ params.PRIX }} ]]

Two things worth knowing:
- [[ Sculpture/Éclat: "Gold-plated brass with an anti-tarnish coating." ]] [[ 925: "925 sterling silver and lab-grown moissanite." ]] [[ Couleur précieuse: "Coloured stones, silver-tone finish [to confirm]." ]] [[ Mixte: "Set on cord." ]]
- It comes with its matching earrings, in our ribboned box, with a velvet pouch and a polishing cloth.

**[Take another look]**

Questions about chain length or earring size? Just reply.

The CHARMED PARIS team

### N2. Same universe (+2 days)

**Subject**: A few more in the same spirit
**Preheader**: In case that one wasn't quite right.

Hi {{ contact.PRENOM }},

You like {{ params.UNIVERS }}. Here are three more, from subtle to statement:

[[ 3 products, same universe, by price ascending ]]

To help you choose:
- Every day, or special occasions?
- Gold tones, or silver tones?
- Open neckline or polo neck? Shorter necklaces sit best on an open neckline.

Tracked delivery, nothing to pay on arrival.

**[See {{ params.UNIVERS }}]**

The CHARMED PARIS team

---

## After purchase

### P1. Shipped (as soon as the tracking number is available)

**Subject**: Your set is on its way
**Preheader**: Your tracking link is inside.

Hi {{ contact.PRENOM }},

Good news: order no. {{ params.ORDER_ID }} has left.

**[Track my parcel]** → {{ params.TRACKING_URL }}
*Tracking no.: {{ params.TRACKING_NUMBER }}*

**When will it arrive?**
In 9 cases out of 10, your set arrives by **{{ params.DATE_LIVRAISON_MAX }}**.
Tracking can take a day or two to show the first updates. That's normal.

**On delivery**
Duties and taxes are already paid. There's nothing to pay the courier.

**In the parcel**
Your set in our ribboned jewellery box (a blue velvet box for Joaillerie 925), a velvet pouch, a polishing cloth, a care card and a packing slip with no prices.
[[ if 2+ sets: "Your second set is in a sealed pouch in the same parcel. There's one jewellery box per order." ]]

**Your order**
[[ summary: image, name, quantity, price ]]

Any questions? Just reply.

The CHARMED PARIS team

### P2. "Your box is arriving" (when DHL shows "out for delivery", otherwise order + minimum business days)

**Subject**: Your box is arriving
**Preheader**: Two minutes to open it right.

Hi {{ contact.PRENOM }},

[[ if "out for delivery" event: "Your parcel is out for delivery today." ]]
[[ otherwise: "Your parcel could arrive as soon as today. In 9 cases out of 10, it's with you by {{ params.DATE_LIVRAISON_MAX }}." ]]

**[[ For herself (`ACHAT_CADEAU = non`) ]]**
When you open it:
1. Keep the velvet pouch. That's where your set lives between wears.
2. Put the polishing cloth aside. You'll use it after each wear.
3. Read the care card. It takes thirty seconds.

One habit from day one: perfume and lotion first, jewellery last.

**[[ Gift (`ACHAT_CADEAU = oui`) ]]**
Is it a gift? A few tips:
- Don't throw the outer box away too quickly. Check everything's there first.
- The velvet pouch and care card are part of the gift. Leave them in the box.
- There are no prices and no message in the parcel. The note is up to you.
- Sent straight to them? Let them know a parcel is on its way in their name. Nothing to pay on delivery.

**[[ Unknown (`ACHAT_CADEAU = inconnu`) ]]**
Quick question so we can write to you better, one click:
**[It's for me]**   **[It's a gift]**

**Something wrong when you open it?**
Damaged parcel, missing piece, wrong set: email us **within 10 days of delivery** with a photo, and we'll sort it quickly.
*Your statutory rights stay the same either way.*

The CHARMED PARIS team

### P3. Care tips (delivery + 2 days, service email, no promotion)

**Subject**: How to keep your set looking its best
**Preheader**: Five habits that make the difference.

Hi {{ contact.PRENOM }},

Your set has arrived. Here's how to keep it looking good for longer.

**The basics**
1. **Keep it dry.** Take it off before showering, bathing, swimming and sport. Water, soap and chlorine wear the plating down.
2. **Perfume, lotion and hairspray first.** Jewellery goes on last and comes off first.
3. **Wipe it with the polishing cloth** after wearing, gently.
4. **Store each piece in the velvet pouch or its resealable bag**, away from damp. The bathroom isn't the best spot.
5. **No cleaning products**, no toothpaste, no ultrasonic cleaners.

**[[ Block by universe ]]**

**Sculpture and Éclat (gold-plated brass)**
The plating is a thin layer, protected by an anti-tarnish coating. Wipe softly, without pressing. For zirconia stones, a small soft, **dry** brush clears the setting.

**Couleur précieuse**
Each stone is set by hand. Avoid knocks and don't pull on the stones. Store the necklace flat so the chain doesn't tangle.

**Joaillerie 925 (sterling silver and moissanite)**
Silver can darken slightly in air. That's normal, and the polishing cloth brings it back. Moissanite is a hard stone, but the setting is still delicate. Keep the certificate if your parcel includes one (stones of 0.1 carat and above).

**Mixte (on cord)**
Cord doesn't like water or tugging. Keep it dry, and open the clasp rather than pulling it over your head.

**Spotted a problem?** Email us soon, ideally within 10 days of delivery, with a photo.

The CHARMED PARIS team

### P4. Review request (delivery + 14 days, copy for Judge.me)

**Subject**: How are you finding it?
**Preheader**: Your review helps the next person choose.

Hi {{ contact.PRENOM }},

Your {{ params.NOM_PRODUIT }} arrived two weeks ago.

Do you wear it often? Does it look like the photos? Is the size right?
A short review helps people who are on the fence. It also helps us choose our next sets.

**[Leave a review]**

A photo of you wearing it is welcome, never required.
If something's not right, say so, and reply to this email. We'd rather know and help.

The CHARMED PARIS team

*We don't offer anything in return for reviews, good or bad. Every published review comes from a verified customer.*

### P4b. Review reminder (P4 + 7 days, once)

**Subject**: Thirty seconds for a review?
**Preheader**: Last reminder, promise.

Hi {{ contact.PRENOM }},

If you have a moment, a star rating and one line is plenty.

**[Leave my review]**

Thank you. We won't ask again for this order.

---

## Second set (cross-sell)

### X1. The next one (day 21)

**Subject**: What would your next set be?
**Preheader**: Three ideas based on your first one.

Hi {{ contact.PRENOM }},

You've had your {{ params.NOM_PRODUIT }} for a few weeks now. We hope it's getting plenty of wear.

**[[ For herself ]]**
If you fancy a second, for a different look or other outfits, here are three that pair well with yours:
[[ 3 products: 1 same universe + 2 neighbouring universe ]]

**[[ Gift ]]**
Your last set was a gift. What about one for you this time? Or for the next occasion (birthday, thank-you, just because):
[[ 3 products, similar price to the first order ]]

Your code, valid for 14 days: **{{ contact.CODE_X }}**, 10% off your next set.
*Valid until {{ params.DATE_FIN_CODE }}. Can't be combined.*

**[See the sets]**

The CHARMED PARIS team

### X2. Code reminder (X1 + 10 days, if opened or clicked and unused)

**Subject**: Your code ends on {{ params.DATE_FIN_CODE }}
**Preheader**: Just so you know.

Hi {{ contact.PRENOM }},

Your code **{{ contact.CODE_X }}** (10% off) works until {{ params.DATE_FIN_CODE }}.
After that it stops working. The sets aren't going anywhere.

**[See my picks again]**

---

## Birthday

### A1. Happy birthday (3 days before)

**Subject**: Happy birthday, {{ contact.PRENOM }}
**Preheader**: A small gift from us, valid for 30 days.

Hi {{ contact.PRENOM }},

Your birthday's coming up, so we wanted to say it a little early.

Your gift: **{{ contact.CODE_ANNIV }}**
[[ if `CERCLE = oui`: 15% off, else 10% off ]] the set of your choice, until {{ params.DATE_FIN_CODE }}.

A few ideas from your favourite universe:
[[ 3 products `UNIVERS_PREFERE` ]]

**[Choose my set]**

Have a lovely day,
The CHARMED PARIS team

### A2. Reminder (A1 + 20 days, if unused)

**Subject**: Your birthday gift is still here
**Preheader**: Valid until {{ params.DATE_FIN_CODE }}.

Hi {{ contact.PRENOM }},

Your birthday code **{{ contact.CODE_ANNIV }}** works until {{ params.DATE_FIN_CODE }}.
No pressure at all. It's there if you want it.

**[See the sets]**

---

## Win-back (90 days)

### R1. What's new (day 90)

**Subject**: New since you last visited
**Preheader**: A few sets you haven't seen yet.

Hi {{ contact.PRENOM }},

It's been a while. Here's what's changed.

[[ block: new sets from `UNIVERS_PREFERE`; if none, the 3 most viewed sets in that universe. Never "bestsellers" without real data. ]]

**[See what's new]**

The CHARMED PARIS team

### R2. Free delivery (day 97, if R1 not clicked)

**Subject**: Delivery's on us
**Preheader**: No minimum spend, for 14 days.

Hi {{ contact.PRENOM }},

If a set has caught your eye, delivery is free on your next order, whatever the amount.

Your code: **{{ params.CODE_RV }}**, valid until {{ params.DATE_FIN_CODE }}.

**[Choose my set]**

The CHARMED PARIS team

### R3. Shall we keep in touch? (day 111, if R1 and R2 not clicked)

**Subject**: Should we keep writing?
**Preheader**: Your call. One click.

Hi {{ contact.PRENOM }},

We haven't heard from you in a while, and that's OK.
We'd rather write less and make it count. Tell us what you'd like:

**[Keep things as they are]**
**[Only before the holidays]** (Christmas, Valentine's, Mother's Day)
**[Change style or language]**
**[Stop emails]**

If we don't hear back, we'll write much less often.

Thanks for being here,
The CHARMED PARIS team

---

## Christmas 2026

Order-by dates (Branvas, official):

| Destination | Order by |
|---|---|
| UK, US, Australia | **Tuesday 8 December** |
| Europe and Canada | **Friday 4 December** |
| Rest of world | **Monday 30 November** |

`{{ params.DATE_LIMITE }}` is filled in by `PAYS`. Festive wrapping is free until 24 December. No engraving or personalisation.

### NO1. Ideas and order-by date (Tuesday 24 November)

**Subject**: Christmas: order by {{ params.DATE_LIMITE }}
**Preheader**: And festive wrapping is on us.

Hi {{ contact.PRENOM }},

We'd rather tell you early: for your set to arrive before Christmas, order by **{{ params.DATE_LIMITE }}**. After that, we can't promise the date.

**Until 24 December, every order ships in festive wrapping**: gift paper, ribbon, decorations and a Christmas card. It's free, and there's nothing to tick.

**Ideas, by person**
- Wears gold every day → **Sculpture** [[ 2 products ]]
- Loves a bit of sparkle at night → **Éclat** [[ 2 products ]]
- Isn't afraid of colour → **Couleur précieuse** [[ 2 products ]]
- A gift that really counts → **Joaillerie 925** [[ 2 products ]]

**By budget**: under €60 · €60–90 · €150+ [align with real prices]

You can have it sent straight to them. Duties and taxes are prepaid, so there's nothing to pay on delivery.

**[Find their gift]**

The CHARMED PARIS team

### NO2. One week left (UK/US/AU: Tuesday 1 December · EU/Canada: Monday 30 November)

**Subject**: Delivery before Christmas: order by {{ params.DATE_LIMITE }}
**Preheader**: A practical reminder.

Hi {{ contact.PRENOM }},

A practical reminder: to get your set before Christmas, order by **{{ params.DATE_LIMITE }}**.

Can't decide? Reply with three words about them (their style, colours, the occasion) and we'll suggest two or three sets.

[[ 4 products, one per universe ]]

**[See gift ideas]**

The CHARMED PARIS team

### NO3. Last recommended day is tomorrow (UK/US/AU: Monday 7 December · EU/Canada: Thursday 3 December · rest of world: Saturday 28 November)

**Subject**: Tomorrow's the last day for Christmas
**Preheader**: Order by {{ params.DATE_LIMITE }} for delivery before the 24th.

Hi {{ contact.PRENOM }},

Tomorrow, **{{ params.DATE_LIMITE }}**, is the last day to order with delivery expected before Christmas.

Festive wrapping is still free.

**[Choose now]**

All sorted already? Thank you. Ignore this one.

### NO-SMS (UK only: Tuesday 8 December, 10am · SMS opt-in only · no US SMS at launch)

> CHARMED PARIS: last day today to order for delivery before Christmas. Festive wrapping included. charmedparis.com/christmas Reply STOP to opt out

### NO4. After the deadline (UK/US/AU: Wednesday 9 December · EU/Canada: Monday 7 December · rest of world: Tuesday 1 December)

**Subject**: Too late for the 24th? Not too late to give it
**Preheader**: A card to put under the tree in the meantime.

Hi {{ contact.PRENOM }},

The last order date for delivery before Christmas has passed. We won't promise the impossible.

But you can still give a set:
1. Order now. It usually arrives within [[ 3–7 / 3–8 / 4–9 ]] business days, with no guaranteed date.
2. Print our "**Your box is on its way**" card and put it under the tree on the 24th.
3. The box follows a few days later, in festive wrapping if it ships before 24 December.

**[Download the printable card]**   **[Choose the set]**

Happy holidays,
The CHARMED PARIS team

---

## Valentine's Day 2027 (Sunday 14 February)

Calculated order-by dates, for delivery by Friday 12 February. Replace them with Branvas's official dates if published.

| Destination | Order by |
|---|---|
| UK | Wednesday 3 February |
| US | Tuesday 2 February |
| France, Germany, Spain | Monday 1 February |
| Italy | 29 January |
| Ireland | 28 January |
| Rest of world | 27 January |

### SV1. To give, or to be given (Tuesday 19 January)

**Subject**: Valentine's: to give, or to drop a hint
**Preheader**: Order by {{ params.DATE_LIMITE }} for 14 February.

Hi {{ contact.PRENOM }},

Valentine's Day is a Sunday this year. For delivery in time, order by **{{ params.DATE_LIMITE }}**.

**To give**: the parcel arrives ready to give, with the ribboned box, velvet pouch, care card and no prices. We can't include a message, so send your note separately.

**To drop a hint**: pick your set, then forward this email to the right person. Or just send them the link. Your secret's safe.

[[ 4 products: Éclat, Couleur précieuse (pink), Joaillerie 925 (heart) ]]

**[See the Valentine's edit]**

The CHARMED PARIS team

### SV2. Order-by reminder (UK/US: Monday 1 February)

**Subject**: For 14 February: order by {{ params.DATE_LIMITE }}
**Preheader**: After that, we can't promise the date.

Hi {{ contact.PRENOM }},

A simple reminder: to get your set before Valentine's Day, order by **{{ params.DATE_LIMITE }}**.

**[Choose my set]**

### SV-SMS (UK only: Tuesday 2 February, 11am)

> CHARMED PARIS: for a set delivered before 14/02, order by Wed 3 Feb. charmedparis.com/valentines Reply STOP to opt out

---

## Mother's Day 2027 (the date depends on the country)

| Country | Date | Order by (calculated) |
|---|---|---|
| UK, Ireland (Mothering Sunday) | Sunday 7 March | UK: **Wednesday 24 February** · Ireland: **Thursday 18 February** |
| US, Canada, Australia | Sunday 9 May | **Tuesday 27 April** |

`{{ params.DATE_FETE }}` and `{{ params.DATE_LIMITE }}` are filled in by `PAYS`. Recipients in other countries get the date of their own country, or no send if it isn't known.

### FM1. Ideas (about 12 days before the order-by date: UK/IE 10 February, US/CA/AU 15 April)

**Subject**: Mother's Day: a set that already matches
**Preheader**: For {{ params.DATE_FETE }}, order by {{ params.DATE_LIMITE }}.

Hi {{ contact.PRENOM }},

Mother's Day is on **{{ params.DATE_FETE }}** this year. For delivery in time, order by **{{ params.DATE_LIMITE }}**.

A set is easy to give: the necklace and earrings already go together, so there's no guessing what she'll wear them with.

**Depending on your mum**
- Classic and understated → **Sculpture** [[ 2 products ]]
- Loves colour → **Couleur précieuse** [[ 2 products ]]
- Worth marking properly → **Joaillerie 925** [[ 2 products ]]

We can deliver to her door, with nothing to pay on arrival.

**[Find her set]**

The CHARMED PARIS team

### FM2. Day before the order-by date

**Subject**: Mother's Day: last day is tomorrow
**Preheader**: Order by {{ params.DATE_LIMITE }} for {{ params.DATE_FETE }}.

Hi {{ contact.PRENOM }},

Tomorrow, **{{ params.DATE_LIMITE }}**, is the last day to order with delivery expected before Mother's Day.

**[Choose her set]**

### FM-SMS (UK only, on the order-by date, 10am)

> CHARMED PARIS: Mothering Sunday is 7 March. Last day today to order in time. charmedparis.com/mothers-day Reply STOP to opt out

---

## Back in stock

### RS1. It's back (on restock, one send only)

**Subject**: {{ params.NOM_PRODUIT }} is available again
**Preheader**: You asked us to let you know.

Hi {{ contact.PRENOM }},

You asked us to tell you: **{{ params.NOM_PRODUIT }}** is available again.

[[ product image · price ]]

**[See it]**

That's our only message about it. We won't email you about this set again.

The CHARMED PARIS team

### RS-SMS (SMS opt-in and request made by SMS, UK only)

> CHARMED PARIS: {{ params.NOM_COURT }} is available again. {{ params.URL_COURTE }} Reply STOP to opt out

---

## Le Cercle and referrals

### C1. Welcome to Le Cercle

**Subject**: You're in Le Cercle
**Preheader**: Free delivery, early access and a gift every 3 orders.

Hi {{ contact.PRENOM }},

Two sets with us [[ or "a Joaillerie 925 set" ]]: thank you. You're now part of **Le Cercle**, our loyalty circle. There's nothing to do. It's all linked to your email.

**What it means for you**
- **Free delivery** on every order, no minimum.
- **New sets 48 hours before everyone else**, by email.
- **€15 off every 3 orders**, on orders of €79 or more.
- **Birthday**: 15% off instead of 10%, if you tell us the date. **[Add my birthday]**

Log in with this email when you order and free delivery applies automatically.

The CHARMED PARIS team

### C2. Your €15 (every 3 orders)

**Subject**: Your €15 is ready
**Preheader**: Valid for 60 days, on orders of €79+.

Hi {{ contact.PRENOM }},

Three sets since you joined Le Cercle. Here's **€15** towards the next one.

Your code: **{{ params.CODE_CERCLE }}**, on orders of €79 or more, until {{ params.DATE_FIN_CODE }}.

**[Choose my set]**

Thank you for sticking with us,
The CHARMED PARIS team

### PA1. Referral invite (delivery + 30 days)

**Subject**: Give €10, get €10
**Preheader**: For a friend who'd love our sets.

Hi {{ contact.PRENOM }},

If you like your set, you probably know someone who would too.

**How it works**
1. Share your personal link.
2. Your friend gets **€10 off** her first order of €59 or more.
3. Once she's kept her order (14 days after delivery), you get **€10** off your next set of €59 or more.

Your link: **{{ params.LIEN_PARRAINAGE }}**

**[Share my link]**

*Up to 5 rewarded referrals per year. New customers only. Full terms: [link].*

The CHARMED PARIS team

### PA2. Referrer reward

**Subject**: Thank you, your €10 is here
**Preheader**: Your friend kept her set.

Hi {{ contact.PRENOM }},

Your friend ordered through you and kept her set. Thank you!

Your €10: **{{ params.CODE_PARRAIN }}**, on orders of €59 or more, until {{ params.DATE_FIN_CODE }}.

**[Choose my set]**

The CHARMED PARIS team
