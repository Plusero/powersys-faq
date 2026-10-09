---
title: How does Tibber charge my EV when electricity is cheap, and which markets am I part of?
description: How a price signal starts home EV charging, why day-ahead prices differ from real-time balancing, and where Tibber participates on your behalf.
published: 2026-10-09
topic: Electricity markets
tags: [Electric vehicles, Smart charging, Dynamic tariffs, Tibber, Demand response]
featured: false
draft: false
takeaway: You buy electricity from Tibber as a retail customer. Smart charging shifts your demand towards cheap day-ahead prices; Grid Rewards can additionally use your charging flexibility in other markets through Tibber.
---

This example uses **Tibber in the Netherlands**. Tariffs, integrations, and flexibility services vary by country.

## Is the price really real-time?

Usually, the price triggering ordinary smart charging is a **day-ahead price**: tomorrow's prices are published today. Tibber's Dutch tariff changes every 15 minutes, but those changes follow an announced schedule. A low price becoming effective at 02:00 does not mean a new market trade happens for your car at 02:00. The app's consumption price includes taxes and the purchasing fee; fixed charges are separate. [Tibber's price explanation](https://tibber.com/nl/stroomprijs)

## How does the car start charging?

1. **Connect and set your needs.** Plug in, link a supported car or charger to Tibber, and set your departure time and target battery level.
2. **Choose charging intervals.** Tibber uses prices, charging power, available time, and the battery target to plan charging. Its Smart Charging feature optimizes a schedule; it is more than a fixed “charge below this price” rule. [How Smart Charging works](https://support.tibber.com/hc/nl/articles/48351672486417-Wat-is-Slim-laden)
3. **Send a control command.** Through the supported car or charger integration, Tibber starts or pauses charging. Electricity flows through your normal grid connection; the software controls when you consume it. [Tibber's charging integrations](https://tibber.com/nl/slimme-bediening/slim-opladen)

For an **invented threshold example**, a home automation could allow charging below €0.20/kWh and pause above it. Compare against the consumption tariff including taxes and fees. A strict threshold alone cannot ensure sufficient charge by departure if prices never fall far enough.

## Which markets do I participate in?

| Market or mechanism | Your role |
| --- | --- |
| **Retail electricity** | Direct: you have a supply contract with Tibber and pay for metered consumption. |
| **Day-ahead wholesale market** | Indirect: Tibber buys electricity for customers; your charging responds to the resulting tariff. You submit no exchange bids yourself. |
| **Intraday trading** | Through Grid Rewards, Tibber can shift charging and trade closer to delivery, sharing the value with you. |
| **Imbalance settlement** | Grid Rewards can adjust charging in response to system imbalance signals. This settles deviations from scheduled energy; it is not an exchange where you personally place orders. |

These additional roles depend on participation in Grid Rewards. Tibber describes both intraday trading and imbalance response in its [market overview](https://tibber.com/nl/magazine/inside-tibber/grid-rewards-en-energiemarkten). That page labels Dutch **aFRR**, a contracted balancing reserve service, as forthcoming when checked on 9 October 2026; cheap-price charging alone does not establish participation in it.

With **Grid Rewards**, Tibber aggregates devices and can increase, reduce, or pause charging for a reward while respecting your charging settings. This is an additional service beyond saving through the retail tariff. [Grid Rewards for EVs](https://support.tibber.com/hc/nl/articles/48351672784401-Grid-Rewards-voor-elektrische-auto-s)
