---
title: How is probabilistic forecasting used in power systems?
description: Learn how forecast quantiles help power-system decisions, with a practical renewable reserve-bidding example and its limitations.
published: 2026-10-06
topic: Forecasting
tags: [Renewables, Uncertainty, Electricity markets]
featured: true
draft: false
takeaway: Probabilistic forecasts make uncertainty visible so operators and traders can weigh commitments against the risk of shortfalls. A useful forecast still needs calibrated probabilities and a decision model that respects physical constraints.
---

Power-system decisions often have to be made before the weather, demand, or renewable output is known. A single forecast gives one number. A probabilistic forecast adds information about the range of possible outcomes and how likely they are. That helps answer a more practical question: **how much can we commit, given the consequences of being wrong?**

## What does a forecast quantile mean?

For generation, a P10 forecast is a threshold below which output is predicted to fall with 10% probability. Equivalently, output is predicted to reach or exceed that threshold with approximately 90% probability. P50 is the **median**, not necessarily the mean: half the predicted distribution lies on either side.

Consider an **invented teaching example** for one future interval. A wind farm has a P50 forecast of 100 MW and a P10 forecast of 70 MW. Committing 100 MW leaves more exposure to lower-than-forecast production than committing 70 MW. The latter sacrifices potential sales in exchange for a smaller predicted shortfall probability. Neither number is a guarantee, and the best decision depends on the cost of shortfalls and the value of additional commitments.

## A practical example: renewable reserve bids

[Dexter Energy's article on probabilistic wind and solar forecasting](https://dexterenergy.ai/news/probabilistic-wind-and-solar-power-forecasting/) is a good practical example of quantiles informing reserve-bid sizing. Leon Overweel and Roy van den Kieboom describe using lower generation quantiles to size bids for automatic frequency restoration reserve (aFRR). Their solar example compares a P10-based rule with fixed discounts of a point forecast, illustrating how an uncertainty estimate can inform a commercial decision.

This is a useful case study of the decision process. It should be read as a vendor's illustration, rather than evidence that one quantile is always the best bidding rule.

## Available output is different from upward reserve

There is an important physical distinction in applying this idea. Forecast renewable availability describes the power that could be generated. **Upward reserve** requires the ability to increase output from the operating baseline when requested.

A renewable plant already generating all its available power has no upward headroom. Providing upward reserve therefore requires an appropriate operating arrangement, such as curtailing output below availability or using a coordinated resource. The deliverable reserve also depends on response speed, equipment limits, and how long the increase must be sustained. A generation quantile alone does not establish that capability.

## One interval is different from a whole block

A calibrated P10 forecast for each interval does not imply a 90% probability of meeting a commitment throughout a multi-interval block. Forecast errors across time are related, and any one interval can cause a shortfall. Taking the lowest interval P10 gives a conservative-looking number, but does not by itself establish a block-wide reliability level. That requires information about the joint outcomes across time, such as suitably validated forecast trajectories.

## What makes the probabilities useful?

Check **calibration** against historical observations: across many comparable forecasts, outcomes should fall below P10 roughly 10% of the time. Check this across seasons and operating conditions, not just overall. Also assess how informative the forecast ranges are; very broad ranges may be cautious but offer little help.

The same principle can guide storage scheduling, demand planning, and other decisions: forecast uncertainty, connect it to operational constraints, and evaluate the resulting decision against observed outcomes.

## Reference

Leon Overweel and Roy van den Kieboom, [*Probabilistic wind and solar power forecasting for bidding into aFRR*](https://dexterenergy.ai/news/probabilistic-wind-and-solar-power-forecasting/), Dexter Energy, 12 August 2026. Accessed 6 October 2026.
