# Intercom

Source : https://faq.branvas.com/en/articles/18321590-where-does-tracking-information-appear-in-my-woocommerce-store (lu le 22/11/2026)

When Branvas ships an order from your WooCommerce store, the tracking number is sent back to your store automatically. Where it shows up in your WooCommerce admin, and how your customer is told, depends on which tracking tools your store has. In every case your customer gets the tracking number by email.

Quick summary

Your store has

Where you see the tracking number

What your customer receives

A shipment tracking plugin (Advanced Shipment Tracking or WooCommerce Shipment Tracking)

The Shipment Tracking box in the order's right sidebar

The "Your order is on its way!" (Completed order) email, with the tracking number in it

WooCommerce Fulfillments turned on

The Fulfilled badge at the top of the order; click it to see the tracking number

An "item has been fulfilled" email with the tracking number, then the Completed order email

Both

Both places above

One Completed order email with the tracking number (no duplicate email)

Neither

A customer note in Order notes (shown in blue)

A "A note has been added to your order" email with the tracking number, then the Completed order email

Your store has a shipment tracking plugin

If you use Advanced Shipment Tracking (AST), free or Pro, or the official WooCommerce Shipment Tracking extension, we add the tracking number directly to the plugin.

Where to look: open the order in WooCommerce > Orders. The Shipment Tracking box in the right sidebar shows the carrier and the tracking number, which links to the carrier's tracking page. It also says "Added via REST API", which means Branvas added it. AST also adds a private note ("Order was shipped with ... tracking number is ...") that only you can see.

Your customer: we mark the order Completed, and WooCommerce sends the customer the "Your order is on its way!" email. The tracking plugin adds the tracking number to that email.

Your store has WooCommerce Fulfillments turned on

WooCommerce 10.1 and later include a built-in Fulfillments feature. It is off by default. If you have turned it on, we record each shipment as a fulfillment, with the items shipped, the carrier and the tracking number.

Where to look: at the top right of the order, next to the order status, you will see a green Fulfilled badge. The tracking number is not shown on the page itself. Click the badge or the pencil icon beside it. A panel opens on the right showing the fulfillment, the items it covers and the tracking number. Expand the tracking row to see the carrier and the tracking link.

Your customer: WooCommerce sends an "An item from your order has been fulfilled!" email with the tracking number. Because we also mark the order Completed, the customer then receives the "Your order is on its way!" email too.

If the carrier is not in WooCommerce's built-in carrier list, it appears as "Other" with the carrier's name, for example "YunExpress". The tracking number and link are still included.

Your store has both a tracking plugin and Fulfillments

We write the tracking number to both places, so you will see it in the Shipment Tracking box and in the Fulfilled panel.

Your customer: receives one email, "Your order is on its way!", with the tracking number from your tracking plugin. We do not ask WooCommerce to send a second fulfillment email for the same tracking number.

Your store has neither

A standard WooCommerce store has nowhere to store a tracking number. In that case we add the tracking details to the order as a customer note, which WooCommerce emails to your customer straight away. This is common practice among fulfillment and dropshipping services.

Where to look: in the Order notes box in the right sidebar. Customer notes are shown in blue; grey notes are private and visible only to you. The note, titled "Shipment tracking information", lists the tracking number, the carrier and the tracking link.

Your customer: receives the note by email ("A note has been added to your order"), followed by the "Your order is on its way!" email.

Want tracking in a dedicated box instead of a note? Install the free Advanced Shipment Tracking plugin. Orders we ship after you install it will show the tracking number in the Shipment Tracking box.

Order status: when we mark an order Completed

WooCommerce has no "Shipped" status. Completed means the order has been fulfilled and is on its way, not that it has been delivered. So after adding the tracking number, we move the order from Processing to Completed, and WooCommerce sends your customer the "Your order is on its way!" email.

We only do this when it is safe to. We leave the status as it is when:

- The order is not in Processing, for example On hold (waiting for you to confirm payment), Cancelled, Refunded, or already Completed. We still add the tracking number.

- The order also contains items we do not fulfill, such as your own products. A WooCommerce status covers the whole order, so marking it Completed would tell your customer that your items have shipped too. We add the tracking number for our items and leave the status for you to change once you ship the rest. With Fulfillments turned on, the order shows as Partially fulfilled.

Common questions

I installed a tracking plugin, but an earlier order only has a note. Why?

We send the tracking number once, when the order ships. If your store had no tracking plugin at that moment, the tracking was saved as a customer note and your customer was emailed. Installing a plugin later does not move existing notes into it. You can add the tracking number to the plugin by hand if you want it there; orders shipped after the plugin was installed are added to it automatically.

I use a different tracking plugin (AfterShip, YITH, ParcelPanel/CWILL, Orders Tracking by VillaTheme, and others). Where does the tracking go?

These plugins do not provide a way for us to add tracking to them, so the tracking is saved as a customer note, the same as a store with no plugin. Your customer is still emailed the tracking number. AfterShip has an option to import tracking numbers from Advanced Shipment Tracking, so if you run AfterShip, installing AST alongside it lets the tracking reach AfterShip too.

How do I turn on WooCommerce Fulfillments?

It is an optional feature in WooCommerce 10.1 and later, and WooCommerce still describes it as in testing. See WooCommerce's announcement for how to enable it. You do not need it for tracking to sync: a tracking plugin, or no plugin at all, works too.

My customer says they never got the tracking number.

Open the order and check the place listed for your setup in the summary table above. If the tracking is there, the email was sent by your store, so ask your customer to check their spam folder. WooCommerce emails are sent from your own store, so your store's email settings and email delivery also affect whether they arrive.

For how tracking works in general and why a tracking number may not show movement right away, see How does order tracking work, and why isn't my tracking number updating?

Related Articles
- How does branded dropshipping with Branvas work?

- How does order tracking work, and why isn't my tracking number updating?

- What sales channels are supported?

- Is there a shipping policy template I can use?

- Can I use Branvas without Shopify? (WooCommerce, Wix, Squarespace, custom sites)
