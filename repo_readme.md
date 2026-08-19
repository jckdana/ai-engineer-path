# Predicting Nightly Price for Austin, TX Airbnb Listings CAPSTONE

**Jack Danache** · Berkeley ML/AI Professional Certificate · Capstone Final Report

📓 **[Link to the Jupyter Notebook →](Austin_Airbnb_Pricing_Capstone.ipynb)**

---
## Executive summary

**Project overview and goals.** Airbnb hosts in Austin set nightly prices by hand, usually by
eyeballing a few nearby listings. That is slow, inconsistent, and leaves money on the table in both
directions: price too high and the calendar sits empty, price too low and every booked night is a
discount the host did not have to give. The goal of this project is to build a tool that answers a
concrete question for a host — **given this property, what should a night cost?** I identify which
listing, host, and location characteristics actually drive nightly price in Austin, quantify how
much each is worth in dollars, and compare five models that predict price from those
characteristics. I then layer on a demand-seasonality adjustment so the output is a *pricing
calendar* rather than a single flat number.

**Findings.** The price in Austin is driven extremely by **capacity and property type**, not by the
things hosts tend to fuss over. The best model to choose — a tuned gradient-boosting regressor — this predicts
the nightly price with a typical error of **$71 per night (MAE)**, a **57% reduction** against the $166
error you get from simply charging the citywide median, and lands within $50 of the true price on
**61%** of listings.

| Model | CV R² (log) | Train R² (log) | Test R² (log) | Test RMSE | Test MAE |
|---|---|---|---|---|---|
| **Gradient Boosting** | **0.8314** | 0.9442 | **0.8218** | **$130.42** | **$71.37** |
| Random Forest | 0.8023 | 0.9742 | 0.8017 | $138.22 | $73.89 |
| Lasso (α = 0.0001) | 0.7241 | 0.7348 | 0.6991 | $159.36 | $94.80 |
| Ridge (α = 0.1) | 0.7253 | 0.7363 | 0.6990 | $160.23 | $95.05 |
| Linear Regression | 0.7253 | 0.7363 | 0.6989 | $160.33 | $95.09 |
| Baseline (median price) | — | −0.0005 | −0.0001 | $236.46 | $165.83 |

The tree easily beats the regularized linear models (CV R² 0.83 vs 0.73), which tells us
the price surface is non-linear — the value of an extra bedroom is not constant; it depends on
the property. All five models rank the same features at the top, which is good evidence the signal
is real rather than an artifact of one algorithm. Lasso retained 6 of 6 engineered features, which
means that the feature engineering (bathroom parsing, amenity count, host tenure, shared-bath flag,
has-reviews flag, distance to downtown) added genuine information rather than noise.

**Results and conclusion.** The effects that matter most are structural facts about the building.

| Feature | Effect on nightly price | 95% CI |
|---|---|---|
| Hotel room (vs. entire home) | **+48.7%** | +36.3% to +62.3% |
| Each additional bathroom | **+19.6%** | +17.2% to +21.9% |
| Each additional guest accommodated | **+9.4%** | +8.8% to +10.0% |
| Review score (per **full** point) | +14.1% | +10.3% to +18.0% |
| Each km from downtown | −1.1% | −1.3% to −1.0% |
| Host tenure (per year) | +0.2% (**not significant**, p = 0.26) | −0.1% to +0.4% |
| Private room (vs. entire home) | **−9.9%** | −13.3% to −6.4% |
| Shared bathroom | **−48.8%** | −51.7% to −45.7% |
| Shared room (vs. entire home) | **−68.6%** | −72.8% to −63.8% |

Privacy, not luxury, is what Austin guests pay for. Listings also separate into **four natural
market segments** — clustered on property attributes only, never on price — that nonetheless land
in distinct price tiers, and a one-size-fits-all model prices the extremes of that range poorly.

**Next steps and recommendations** are stated in full in Sections 10–11 of the notebook. The
headline one: **estimate price elasticity**, which is what would convert this from a model of what
the market charges into a model of what a host should charge.

---

## Rationale

Austin is one of the most competitive short-term rental markets in the entire United States, and the pricing
is the lever hosts control most directly. Yet it is the decision they have the least information
about. A host listing a 2-bedroom bungalow in 78704 has no real, reliable way to know whether $210 a night
is an aggressive or generous amount, and the cost of being wrong compounds every night of the year. A model
that explains which attributes carry price, and by how much, converts pricing from a gut call
into an estimate with a known error bar — for hosts, property managers, and prospective investors
alike.

## Research question

**What listing, host, and location characteristics drive nightly price for Austin, TX Airbnb
listings, and how accurately can we predict nightly price from those characteristics?**

Two sub-questions follow:

1. Do Austin listings separate into distinct market segments that should be priced differently?
2. Is there exploitable time-based demand seasonality that should modulate a listing's base price?

### Model outcomes and predictions

This is also a supervised regression problem. This model takes a listing's attributes as an input and 
outputs a continuous value. This value is the predicted nightly price in dollars. The models are fit 
on`log(1 + price)` and back-transformed, so the output is a dollar figure a host can act on.

My project also has unsupervised learning for another purpose: PCA, which is then followed by K-Means
groups listings into market segments. Prices are also never shown to either of the steps, so the segment
label is an actual genuine model input rather than just another restatement of the target. 

| Component | Type of learning | Algorithms | Output |
|---|---|---|---|
| Price prediction | **Supervised — regression** | Linear Regression, Ridge, Lasso, Random Forest, Gradient Boosting | Predicted nightly price ($) |
| Market segmentation | **Unsupervised — clustering** | PCA + K-Means | Segment label (one of four) |
| Demand seasonality | Time-series decomposition | STL, ARIMA | Day-of-week demand index |

### Relationship to the original problem statement (Assignment 11.1)

My original problem statement asked this question: could a model set prices that
generate **higher expected revenue** than hosts' actual pricing? Answering that properly requires
modeling how demand responds to price (elasticity) and ideally a causal design, because in
observational data price and demand are surprising — we only ever observe the price the host chose
and the bookings that followed. I therefore scoped this project to the predictive question above,
then went as far toward the revenue question as the data honestly supports: quantifying demand-side
weekly seasonality from the booking calendar and converting it into a recommended pricing calendar.
The remaining gap is stated as the primary next step.

## Data sources

Both files come from [Inside Airbnb](http://insideairbnb.com/get-the-data/), Austin TX snapshot
(scraped June 2026).

| File | Grain | Rows | Role |
|---|---|---|---|
| `listings.csv` | one row per listing | 11,295 × 90 cols | modeling dataset and price target |
| `calendar.csv` | one row per listing-night | 4,131,800 | demand seasonality (Section 3) |

**Data quality constraints found during profiling.** Thirteen columns are **100% empty** in this
snapshot, several of which a pricing model would want: `host_since`, `host_response_rate`,
`host_acceptance_rate`, `host_response_time`, and `instant_bookable`. Two consequences were handled
explicitly rather than silently:

- **Host tenure was recovered from a different source.** `host_since` is empty, so tenure is
  reconstructed from `hosts_time_as_host_years` / `_months` (only 4 missing).
- **`instant_bookable` was dropped entirely** rather than imputed to a constant, which would have
  added a useless column to the model.

**Target leakage was identified and removed.** `estimated_revenue_l365d` is literally price ×
occupancy, and the entire `price_quote_*` family is a re-quote of the same nightly rate. Including
any of them would produce a near-perfect score from a model that is useless in practice. All six
were dropped, and the drop reasons (empty / identifier / leakage / redundant) are kept separate in
the notebook so the rationale is auditable.

**Cleaning.** After dropping duplicates, listings with no price, and listings outside a realistic
$10–$1,500 nightly range, the modeling dataset holds **10,081 listings (89.3% of raw)**. Review
scores are missing precisely because a listing has no reviews yet, so a `has_reviews` flag is
added before median-imputing — otherwise imputation silently claims a brand-new listing has average
reviews.

## Methodology

Models are trained on `log(1 + price)` because the target is severely right-skewed (median $217,
mean $352, max $58,600). Training on log-price means the model minimizes *proportional* error, which
matches how pricing mistakes actually hurt.

**Evaluation metric: Mean Absolute Error in dollars.** The audience is a host asking "how far off
will this be?" MAE answers that in the units of the decision. RMSE squares the errors, so a handful
of unusual luxury listings would dominate it and make the number unrepresentative of the typical
case. R² in log space is reported alongside because it is what cross-validation optimizes and what
makes models comparable. Every model is measured against a `DummyRegressor` predicting the median
price, so the scores have a reference point.

Each model is fine tuned with **`GridSearchCV` over a 5-fold cross-validation**. The train/test split
(80/20) is divided on price so both sides cover the same price range.

### Correction to the initial report: the seasonality analysis

My initial submission built a "citywide average listed price by date" series by merging each
listing's static price onto its calendar rows, ran STL on it, and reported a weekly *price*
seasonality. That result was an artifact. This snapshot's `calendar.csv` contains no price
column — only `listing_id`, `date`, `available`, `minimum_nights`, `maximum_nights`. Because each
listing contributes the same price to every one of its calendar dates, the daily average could only
move as the composition of listings changed. The notebook verifies this directly: day-of-week
averages span $2.32 on a $349 mean (CV = 0.056). There is no weekly price signal there.

What the calendar can measure is demand, which is the more useful quantity anyway. Rebuilding
the analysis on booking rate — after trimming to the 355 dates with ≥90% listing coverage, since the
scrape spans four dates and each listing carries a 365-day forward calendar — gives me a real and
statistically significant weekly cycle:

| Day | Avg booking rate | vs. weekly average | Demand index |
|---|---|---|---|
| Monday | 36.00% | −1.29 pts | 0.966 |
| Tuesday | 35.54% | −1.75 pts | 0.953 |
| Wednesday | 35.84% | −1.45 pts | 0.961 |
| Thursday | 37.69% | +0.41 pts | 1.011 |
| **Friday** | **39.24%** | **+1.96 pts** | **1.053** |
| **Saturday** | **39.35%** | **+2.07 pts** | **1.055** |
| Sunday | 37.26% | −0.02 pts | 0.999 |

STL decomposition puts the annual trend swing at about ~23 percentage points against about ~15 for the weekly
cycle, so which season matters somewhat more than which day.

### Segmentation

PCA is applied before K-Means because the capacity features are collinear (r ≈ 0.6–0.8); feeding
them in raw would effectively triple-count "size." Nine features reduce to **6 components retaining
93.6%** of variance. Price is never shown to the PCA or the clustering, so using the segment label
as a model feature does not leak the target.

## Model evaluation and results

**Gradient Boosting is the best model**, with test MAE **$71.41** and test R² (log) **0.8217**
against a naive baseline of $165.83 — a **56.9% reduction** in typical pricing error. Predictions
land within about $25 of the actual price 40% of the time and within $50 at about 61% of the time.

**Two interpretation cautions are documented in the notebook rather than glossed over:**

1. `bedrooms` carries a negative OLS coefficient (−3.0%), which taken at face value says an
   extra bedroom lowers price.
2. **Review score is quoted per full rating point.** Austin ratings are compressed into 4.5–5.0,
   so a realistic 0.1-point improvement is worth 1–2% on price, not 14%.

## Findings

1. **Price is set by what the property is, not how well it is run** — capacity, bathrooms, room
   type, and property type dominate. A shared bathroom is associated with a 49% lower rate and a
   shared room a 69% lower rate versus an entire home. Privacy, not luxury, is what guests pay
   for.
2. **Review scores buy occupancy, not price** Hosts routinely invert this
   priority.
3. **Location is about specific neighborhoods, not distance from downtown.** Raw distance is a weak
   predictor (−1.1%/km). What matters is which ZIP: a handful carry a clear premium that survives
   controlling for size and type, while some lake-adjacent outer-ring listings out-price closer-in
   ones. Austin's price map is a set of pockets, not a gradient.
4. **There are four distinct markets, not one** — and clustering found them without ever seeing a
   price.
5. **Demand follows a reliable weekly and seasonal rhythm.** A host charging one flat rate every
   night is underpricing their highest-demand nights and overpricing their lowest.
6. **The model beats guesswork by a wide margin, with a known limit** — 57% better than the median
   rule, degrading above $500/night.

## Actionable recommendations

**For an individual host:** benchmark against the model and investigate any large gap; adopt a
weekly pricing calendar instead of a flat rate (the notebook generates one, with a 0.5 dampening
factor applied since elasticity is not yet estimated); invest in capacity, not polish; and do not
convert an entire home into private rooms expecting to earn more.

**For a property manager or investor:** price by segment rather than applying one rule across a
mixed portfolio; target the specific premium ZIP codes rather than optimizing for proximity to
downtown; and treat the $500+ band as human-in-the-loop, since model error roughly doubles there.

## Next steps

1. **Estimate price elasticity** by joining booking outcomes to price changes across successive
   Inside Airbnb snapshots. Revenue = price × occupancy, and this project has modeled only the first
   term. This is the highest-value extension.
2. **Move from a static snapshot to a panel** to enable out-of-time validation.
3. **Fit segment-specific models**, particularly for the high-price band where error concentrates.
4. **Extract signal from text fields** (`description`, `name`) — the most direct attack on the
   model's known weak spot above $500.
5. **Engineer richer amenity features** — a pool and a coat hanger currently count the same.
6. **Try stacked ensembles** — the tree and linear models make different errors.

## Limitations

- Observational, single-snapshot data: all effects are associations, not causal estimates.
- Listed price is not transacted price — we observe what hosts ask, not what guests pay.
- Key host-behavior fields are entirely empty in this snapshot, removing a whole category of
  plausible price drivers from consideration.
- Austin only; nothing here should be assumed to transfer to another city without proper research.

## Thank you for this amazing class!
I just wanted to preface with a thank you. This class was everything and more than I expected.
I am super grateful to have had this opportunity to learn alongside my classmates and learn
from those who are extremely well versed in this field. I am leaving this class with confidence
that I learned more than I could have ever imagined. So thank you for whoever is reading this and
I am happy to have been a part of this class :D

### Contact and Further Information

Jack Danache

Email: JMDanache@gmail.com

LinkedIn: https://www.linkedin.com/in/jack-d-25a333195/
