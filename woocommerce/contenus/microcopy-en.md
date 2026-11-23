# CHARMED PARIS · Microcopy (EN)

Second person, short sentences, British spelling, prices in euros. Variables in braces: `{first_name}`, `{order_number}`, `{amount}`, `{tracking_link}`… (map to WooCommerce or email-tool variables). « À confirmer » notes are internal.

---

## 1. Buttons

| Context | Text |
|---|---|
| Add to cart (product page, card) | Add to my box |
| After adding (2 s) | Added to your box |
| View cart | View my box |
| Checkout (cart) | Checkout |
| Pay | Pay {amount} |
| Continue shopping | Keep browsing |
| Out of stock | Back soon |
| Notify me | Let me know |
| See all sets | See the sets |
| Home carousel | Choose my box |
| Newsletter | Sign me up |
| Track order | Track my parcel |
| Apply code | Apply |
| Remove item | Remove |
| Load more | Show more sets |
| Filter | Filter · Clear filters |
| Sort | Sort: price low to high · price high to low · newest |

## 2. Product page

- Under the price: **Box included · Free delivery from €50 · Duties paid**
- Delivery: Delivered in 4–9 business days to France, 3–7 to the UK (9 parcels in 10).
- Christmas (until 4/12): For Christmas in Europe, order by Friday 4 December. UK: by Tuesday 8 December.
- Christmas (after the deadline, until 24/12): Free Christmas wrapping until 24 December. Delivery before Christmas can no longer be guaranteed.
- Adjustable ring: Adjustable ring: the band adjusts slightly to fit your finger.
- Sized ring: Choose your size · Size guide
- Accordion: Materials · Care · Shipping & returns
- Returns line: 14 days to change your mind, returns on us.
- Sold out: This set is sold out for now. Leave your email and we'll tell you when it's back.

## 3. Cart ("Your box")

**Title:** Your box
**Empty:** Your box is empty. · Button: See the sets

**Free delivery from €50 (progress bar)**
- €0–49.99: {remaining} away from free delivery.
- ≥ €50: Delivery is on us.
- Cart at €49: Add a second set for free delivery, and 15% off the second one.

**15% off your second set**
- 1 set in cart: Add a second set: 15% off the cheaper of the two.
- 2+ sets: 15% off your second set, already applied.
- Discount line: Second set −15%
- Parcel note (2+ sets): Your sets travel in one parcel: one in the drawer box, the others in sealed bags. For two gifts to two addresses, place two orders.

**Lines**
- Subtotal · Second set −15% · Delivery · Total (VAT included)
- Delivery under €50: {shipping_fee}
- Note: Prices include VAT. Duties already paid.

**Gift option (checkbox)**
- Label: This is a gift
- Help: No prices in the parcel. Put their address for delivery and yours for billing.

## 4. Checkout

- Title: Checkout
- Steps: Details · Delivery · Payment
- Email: Your email · Help: For your confirmation and tracking.
- Phone (required): Phone · Help: The carrier may need it to deliver your parcel.
- Address: Address · Flat, floor, door code · Help: Check your street number: an incomplete address holds up the order.
- Ship elsewhere: Deliver to a different address (for a gift, say)
- Delivery method (only one): **DHL tracked delivery · 4–9 business days · {fee or Free}** · sub-line: Duties already paid. No express option.
- Christmas (until deadline): Ordered today, your set should arrive before Christmas.
- Christmas (after): From today, delivery before Christmas can't be guaranteed.
- Promo: Got a code? · Apply
- Payment: Secure payment. [À CONFIRMER: card, Apple Pay, PayPal depending on gateway]
- Terms: I have read and accept the terms and conditions of sale.
- Newsletter (unticked by default): Email me about new sets and dates that matter.
- Final button: Pay {amount}
- Under the button: By paying, you confirm your order. You have 14 days from delivery to change your mind.
- Thank-you page: Thank you, {first_name}. Order no. {order_number} is confirmed. You'll get an email in a few minutes, then another with your tracking number once it ships.

## 5. WooCommerce transactional emails

### 5.1 Order confirmation ("Processing")
- **Subject:** Your CHARMED PARIS order no. {order_number} is confirmed
- **Preheader:** We're getting your box ready.
- **Body:**
  Hello {first_name},

  Thank you for your order. It's confirmed and going into preparation.

  What happens next:
  - Your order is prepared in 1 to 2 business days.
  - You'll get an email with your DHL tracking number as soon as it ships.
  - Allow 4 to 9 business days from order to delivery in France, 3 to 7 in the UK.

  Duties and import taxes are already paid: nothing to pay on arrival.

  {order_summary}

  Spotted a mistake in the address? Reply to this email straight away: we can fix it until the order goes into preparation.

  See you soon,
  CHARMED PARIS

### 5.2 Shipped
- **Subject:** Your set is on its way
- **Preheader:** Your DHL tracking number is inside.
- **Body:**
  Hello {first_name},

  Order no. {order_number} has just left.

  DHL tracking: {tracking_number}
  [Track my parcel]({tracking_link})

  Tracking can take 24 to 48 hours to show. Estimated delivery: between {date_min} and {date_max}.

  The carrier may use your phone number to deliver.

  CHARMED PARIS

### 5.3 Delivered
- **Subject:** Your box has arrived
- **Preheader:** A few tips to make it last.
- **Body:**
  Hello {first_name},

  Tracking shows that order no. {order_number} has been delivered.

  Before you wear it:
  - Keep it dry: take it off before showering or swimming.
  - Perfume and lotion first, jewellery last.
  - Store it in its velvet pouch.

  Something not right? A damaged piece, the wrong design: reply with a photo as soon as you can and we'll sort it.

  You have 14 days to change your mind. Return costs are on us.

  CHARMED PARIS

### 5.4 Cancelled / refunded
- Cancelled: **Subject:** Order no. {order_number} is cancelled · Body: Done, your order is cancelled. If you've paid, the refund goes out today to your original payment method. It usually shows within 3 to 10 days, depending on your bank.
- Refunded: **Subject:** Your refund is on its way · Body: We've refunded {amount} to your original payment method. Depending on your bank, it shows within 3 to 10 days.

## 6. Abandoned cart (3 emails)

No fake urgency, no "only 2 left", no countdowns. The discount only appears in email 3 (optional).

### Email 1 · after 1 hour
- **Subject:** Your box is waiting
- **Preheader:** We've kept it just as you left it.
- **Body:**
  Hello {first_name},

  You left {set_name} in your box. We've kept it just as it was.

  {product_image}

  [Back to my order]({cart_link})

  A question about materials, sizing or delivery? Just reply to this email.

### Email 2 · after 24 hours
- **Subject:** What's in the box
- **Preheader:** And what isn't: any prices.
- **Body:**
  Hello {first_name},

  If you're still deciding, here's what comes with {set_name}:
  - every piece of the set, in a CHARMED PARIS drawer box tied with ribbon,
  - a velvet pouch and a polishing cloth,
  - a care card,
  - and no prices anywhere in the parcel, if it's a gift.

  Delivered in 4 to 9 business days to France, 3 to 7 to the UK, duties already paid. 14 days to change your mind.

  [Back to my box]({cart_link})

### Email 3 · after 72 hours (optional)
- **Subject:** 10% off to finish your order
- **Preheader:** Valid for 7 days.
- **Body:**
  Hello {first_name},

  Last email about this, promise.

  If you still like {set_name}, here's 10% off with the code {code}, valid for 7 days.

  [Use my code]({cart_link})

  If not, no problem. We won't write about this cart again.

## 7. Newsletter welcome (10% off)
- **Subject:** Welcome to the circle, here's your 10%
- **Preheader:** Your code is inside.
- **Body:**
  Hello,

  Thanks for joining. Here's your code for your first order:

  **{code}** · 10% off · valid [TO COMPLETE: duration] on every set

  Three things to know about CHARMED PARIS:
  1. We only sell sets: pieces that match, in one box.
  2. We tell you the real material: gold-plated brass, 925 sterling silver, cubic zirconia, lab-grown moissanite, cultured freshwater pearls.
  3. Delivery is free from €50, and duties are already paid.

  [See the sets]({shop_link})

  You'll hear from us when a new set arrives or a date matters. That's all.

  CHARMED PARIS · Open. Be charmed.

  Unsubscribe link: Stop receiving our emails

## 8. Gifts: ready-to-give parcel (no gift message)

Today: **no message can be printed into the parcel** (no field at our partner; custom cards are VIP-plan only). The packing slip shows no prices.

Gift option text:
- Checkbox: This is a gift
- Help: No prices in the parcel. The set arrives in its drawer box tied with ribbon.
- Note: We can't add a note to the parcel. You can send your message yourself on delivery day: your shipping email gives you the estimated date.

Don't offer any gift-message field in cart or checkout. If a customer writes a message in the order notes, reply: "Thank you for your note. We can't add it to the parcel, but your set ships ready to give, with no prices anywhere."

## 9. Error messages

| Situation | Message |
|---|---|
| Invalid email | That email doesn't look complete. Check the @ and the dot. |
| Required field empty | We need this to send you your set. |
| Missing phone | Add your number: the carrier may need it to deliver. |
| Incomplete address | The street number or flat number is missing. An incomplete address holds up the order. |
| Postcode / country mismatch | The postcode doesn't match the country you chose. |
| Invalid promo code | This code isn't working. Check the spelling or the expiry date. |
| Code can't be combined | This code can't be combined with the second-set discount. We've kept the better one for you. |
| Payment declined | The payment didn't go through. Your bank may want you to approve it: try again, or choose another method. |
| Sold out during checkout | This set has just sold out. We've taken it out of your box. |
| Session expired | Your session has expired. Your box is still here; reload the page. |
| Server error | Something went wrong on our side. Try again in a moment, or email us at [TO COMPLETE: email]. |
| 404 | This page doesn't exist, or no longer does. · Button: See the sets |
| Country not served | We don't deliver to this country yet. |
| Already subscribed | You're already in the circle. If your code hasn't arrived, check your spam folder. |
