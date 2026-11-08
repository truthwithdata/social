# Press pitches: Is renting really 'dead money' in the UK?

- Article: https://truthwithdata.com/blog/is-renting-dead-money-uk.html (published 2026-10-23, Data Journalism)
- Tool: https://truthwithdata.com/tools/rent-vs-buy-calculator.html
- Prepared: 2026-11-04. 12 Gmail drafts created in truthwithdata@gmail.com (not sent). Addresses filled only where the outlet publishes one; 6 of 12 have an address.
- UTM: `?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk`

Note: several printed addresses come from Corrections/Contact boxes in older print editions on PressReader (2020-2022). Check each is still current before sending. Chronicle Live and Bristol Post print only a named editor's corrections address, so those drafts were left without a recipient.

## Angles and where the numbers come from

- Most local: Newcastle upon Tyne fastest of 316 authorities (1.0 years, yield 6.98%); Manchester and Portsmouth 1.08; Bristol and Southampton 1.17. Never within 30 years: 15 authorities incl. Elmbridge, Waverley, Mole Valley, South Hams, East Devon, Powys. Source: `data/uk-rent-vs-buy-breakeven-by-local-authority-2026.csv`; article section 5.
- Regional: Scotland fastest region 1.4 years, South East slowest 4.1 (article region table; `data/uk-rent-vs-buy-breakeven-by-region-2026.csv`).
- Surprising national: first-year mortgage interest is 77-107% of rent, more than rent in 5 regions; owning costs 5-45% more before price growth (article section 3). Flat prices: median 26 years (key stats).
- Backtest: 79% of 5-year holds buyer ahead; 2022-24 buyers behind in 8 of 12 regions by July 2026 (section 6; `data/uk-rent-vs-buy-backtest-2005-2026.csv`).
- Rates: +1 point stretches break-even to 2.3-12.2 years; 4%/6%/7% rate gives median 1.3/4.9/13 years (section 7; `data/uk-rent-vs-buy-sensitivity-2026.csv`).
- What it means for you: under two years buying usually loses; beyond five it won in 79% of historical cases; the local rent-to-price ratio decides how fast (section 8).

## Targets

| # | Outlet | Contact | Source URL | Angle |
|---|---|---|---|---|
| 1 | Manchester Evening News | newsdesk@men-news.co.uk | https://www.pressreader.com/uk/manchester-evening-news/20210404/281522228889295 | Manchester is the second-fastest place in England and Wales where buying beats renting (1.1 years) |
| 2 | Chronicle Live (Newcastle) | (none published; use contact page) | https://www.chroniclelive.co.uk/how-to-complain/ | Newcastle is the fastest place in England and Wales for buying to beat renting (1.0 year) |
| 3 | Bristol Post / Bristol Live | (none published; use contact page) | https://www.bristolpost.co.uk/how-to-complain | Bristol: buying beats renting in 1.2 years, while parts of Devon and Gloucestershire never break even |
| 4 | Surrey Live | surreylive@reachplc.com | https://www.getsurrey.co.uk/how-to-complain/ | Elmbridge, Waverley and Mole Valley: buying never beats renting within 30 years |
| 5 | The News (Portsmouth) | (none published; use contact page) | https://www.portsmouth.co.uk/contact-us | Portsmouth is joint second-fastest for buying to beat renting (1.1 years), against the South East as the slowest region |
| 6 | The Herald (Scotland) | news@theherald.co.uk | https://www.pressreader.com/uk/the-herald-1130/20200529/281578062875503 | Scotland is the fastest UK region for buying to beat renting (1.4 years) |
| 7 | WalesOnline | newsdesk@walesonline.co.uk | https://www.pressreader.com/uk/wales-on-sunday/20210418/281513638984200 | Wales: mortgage interest exceeds rent in year one; Powys never breaks even, Merthyr Tydfil fastest |
| 8 | Devon Live | (none published; use contact page) | https://www.devonlive.com/about-us/ | South Hams and East Devon never break even; Exeter 1.4 years |
| 9 | This is Money | (none published; use contact page) | https://www.thisismoney.co.uk/money/article-1595535/How-This-Money-make-wealthier.html | National: first-year mortgage interest is 77-107% of rent; buying wins only on price growth |
| 10 | Guardian Money | (none published; use contact page) | https://www.theguardian.com/help/contact-us | National: 'dead money' is half right; 2022-24 buyers behind renters in 8 of 12 regions |
| 11 | Property Industry Eye (trade) | news@propertyindustryeye.com | https://propertyindustryeye.com/contact-us/ | Trade: buying beats renting within 5 years in 181 of 316 authorities; yield explains the pattern |
| 12 | Mortgage Solutions (trade) | shekina.tuahene@ae3media.co.uk | https://www.mortgagesolutions.co.uk/contact-us/ | Trade: one point on mortgage rates stretches rent-v-buy break-even to 2.3-12.2 years |

Contact notes:

- **Manchester Evening News**: Newsdesk address printed in the paper's Corrections and Complaints box (PressReader edition, April 2021).
- **Chronicle Live (Newcastle)**: No newsdesk address found. The paper's printed Corrections box lists an editor address for corrections only (https://www.pressreader.com/uk/the-chronicle/20220519/282192244594026), which is not used here. Check the contact page.
- **Bristol Post / Bristol Live**: No newsdesk address found. The printed Corrections box names print editor Richard Bache's address for corrections (https://www.pressreader.com/uk/bristol-post/20221109/281530819996805), which is not used here. Check the contact page.
- **Surrey Live**: Main editorial address on the outlet's 'How to complain' page (found via subagent fetch).
- **The News (Portsmouth)**: Contact page returned an error and the addresses on the outlet's contact article are hidden by email protection; check by hand.
- **The Herald (Scotland)**: 'How to get in touch with us' box printed in the paper (PressReader edition, May 2020), for news tips.
- **WalesOnline**: Newsdesk address printed in Wales on Sunday's Clarifications and Corrections box (PressReader edition, April 2021).
- **Devon Live**: No published address found; about/contact page could not be read automatically.
- **This is Money**: No published desk address found; About page could not be read automatically.
- **Guardian Money**: No published Money desk address found; check the help/contact page.
- **Property Industry Eye (trade)**: General news desk address on the outlet's contact page.
- **Mortgage Solutions (trade)**: Shekina Tuahene, group editor, listed for editorial queries on the outlet's contact page.

## Pitches

### 1. Manchester Evening News

**To:** newsdesk@men-news.co.uk  
**Subject:** Manchester: buying beats renting in about a year, one of the fastest in England and Wales  
**Figures from:** data/uk-rent-vs-buy-breakeven-by-local-authority-2026.csv (Manchester, Salford, Stockport, Trafford rows); article sections 3 and 5  
**Words:** 194

```
Hello,

Buying the average home in Manchester beats renting the same home after about 13 months (1.08 years), joint second-fastest of 316 local authorities in England and Wales. That's because rents there are high compared with prices: the average home costs £252,309 and rents for £1,365 a month, a 6.5% gross yield. Salford is 1.25 years. Stockport (4.8 years) and Trafford (6.6 years) take much longer.

Nationally, mortgage interest alone costs 77% to 107% of the rent in the first year, so rent isn't the only 'dead money'. If house prices stopped rising, buying would take decades to come out ahead in most regions.

Method: the same average home bought or rented, using HM Land Registry and ONS prices and rents for July 2026, a 10% deposit at the Bank of England's quoted 90% LTV rate (5.37%), 3% a year growth in prices and rents (the 2005-2026 average) and the renter investing the difference at 5%.

Full analysis, data and code: https://truthwithdata.com/blog/is-renting-dead-money-uk.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk
Free calculator with regional presets: https://truthwithdata.com/tools/rent-vs-buy-calculator.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk

I can send a chart or a table of break-even years for every local authority in your area.

Best wishes,
Vishal Sharma
Truth with Data
truthwithdata@gmail.com
```

### 2. Chronicle Live (Newcastle)

**To:** (blank)  
**Subject:** Newcastle is the fastest place in England and Wales where buying beats renting  
**Figures from:** LA CSV (Newcastle, Gateshead, Northumberland rows; North East: 11 of 12 within 5 years); article region table (North East flat prices 18.3 years)  
**Words:** 187

```
Hello,

Newcastle upon Tyne is where buying the average home beats renting it fastest: after one year, the quickest of 316 local authorities in England and Wales. The average home costs £207,547 and rents for £1,207 a month, a 7.0% gross yield, the highest in our data. After five years the buyer is £32,508 better off than an equivalent renter. Gateshead takes 1.6 years. Northumberland takes 12.6 years.

Nationally, mortgage interest alone costs 77% to 107% of the rent in the first year. Buying wins because of house-price growth: with flat prices it would take 18 years in the North East.

Method: the same average home bought or rented, using HM Land Registry and ONS prices and rents for July 2026, a 10% deposit at the Bank of England's quoted 90% LTV rate (5.37%), 3% a year growth in prices and rents (the 2005-2026 average) and the renter investing the difference at 5%.

Full analysis, data and code: https://truthwithdata.com/blog/is-renting-dead-money-uk.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk
Free calculator with regional presets: https://truthwithdata.com/tools/rent-vs-buy-calculator.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk

I can send a chart or the figures for all 12 North East authorities.

Best wishes,
Vishal Sharma
Truth with Data
truthwithdata@gmail.com
```

### 3. Bristol Post / Bristol Live

**To:** (blank)  
**Subject:** Bristol: buying beats renting in 14 months. In South Hams and East Devon it never does  
**Figures from:** LA CSV (Bristol; East Devon, South Hams, Forest of Dean = no break-even)  
**Words:** 187

```
Hello,

In Bristol, buying the average home beats renting it after 1.17 years, one of the five fastest of 316 local authorities in England and Wales. Bristol rents are high (£1,880 a month on a £352,262 average home, a 6.4% yield), and after five years the buyer is £46,051 ahead. Elsewhere in the South West, East Devon, South Hams and the Forest of Dean are among the 15 areas where the buyer is still behind after 30 years.

Nationally, mortgage interest alone costs 77% to 107% of the rent in year one. Buying wins on house-price growth, and on little else.

Method: the same average home bought or rented, using HM Land Registry and ONS prices and rents for July 2026, a 10% deposit at the Bank of England's quoted 90% LTV rate (5.37%), 3% a year growth in prices and rents (the 2005-2026 average) and the renter investing the difference at 5%.

Full analysis, data and code: https://truthwithdata.com/blog/is-renting-dead-money-uk.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk
Free calculator with regional presets: https://truthwithdata.com/tools/rent-vs-buy-calculator.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk

I can send a chart or the figures for all 26 South West authorities.

Best wishes,
Vishal Sharma
Truth with Data
truthwithdata@gmail.com
```

### 4. Surrey Live

**To:** surreylive@reachplc.com  
**Subject:** Elmbridge, Waverley and Mole Valley: where renting beats buying for 30 years  
**Figures from:** LA CSV (Elmbridge, Waverley, Mole Valley rows); article section 5 (181 of 316, 15 never)  
**Words:** 186

```
Hello,

Surrey has three of the 15 local authorities in England and Wales where buying the average home never beats renting it within 30 years: Elmbridge, Waverley and Mole Valley. In Elmbridge the average home costs £748,080 but rents for £1,867 a month, a 3.0% gross yield. A buyer there is £72,310 behind an equivalent renter after five years and £109,452 behind after ten. Waverley's buyer is £47,640 behind after five years; Mole Valley's is £41,287 behind.

Across England and Wales, buying wins within five years in 181 of 316 authorities. The difference comes down to rent as a share of price.

Method: the same average home bought or rented, using HM Land Registry and ONS prices and rents for July 2026, a 10% deposit at the Bank of England's quoted 90% LTV rate (5.37%), 3% a year growth in prices and rents (the 2005-2026 average) and the renter investing the difference at 5%.

Full analysis, data and code: https://truthwithdata.com/blog/is-renting-dead-money-uk.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk
Free calculator with regional presets: https://truthwithdata.com/tools/rent-vs-buy-calculator.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk

I can send a chart or the figures for every Surrey district.

Best wishes,
Vishal Sharma
Truth with Data
truthwithdata@gmail.com
```

### 5. The News (Portsmouth)

**To:** (blank)  
**Subject:** Portsmouth: buying beats renting in 13 months, in the slowest region for it  
**Figures from:** LA CSV (Portsmouth, Gosport, East Hampshire); article region table and section 3 (South East 4.1 years, 107%)  
**Words:** 182

```
Hello,

Portsmouth is joint second-fastest of 316 local authorities in England and Wales where buying the average home beats renting it: 1.08 years. The average home costs £251,220 and rents for £1,367 a month (a 6.5% yield), and the buyer is £34,482 ahead after five years. Gosport takes 1.4 years. That's unusual for the South East, the slowest region overall (4.1 years), where four districts, including East Hampshire, never break even within 30 years.

Nationally, mortgage interest alone costs 77% to 107% of the rent in year one. In the South East it's 107%, the highest of any region.

Method: the same average home bought or rented, using HM Land Registry and ONS prices and rents for July 2026, a 10% deposit at the Bank of England's quoted 90% LTV rate (5.37%), 3% a year growth in prices and rents (the 2005-2026 average) and the renter investing the difference at 5%.

Full analysis, data and code: https://truthwithdata.com/blog/is-renting-dead-money-uk.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk
Free calculator with regional presets: https://truthwithdata.com/tools/rent-vs-buy-calculator.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk

I can send a chart or the figures for Hampshire districts.

Best wishes,
Vishal Sharma
Truth with Data
truthwithdata@gmail.com
```

### 6. The Herald (Scotland)

**To:** news@theherald.co.uk  
**Subject:** Scotland is the fastest UK region for buying to beat renting  
**Figures from:** Article region table (Scotland row), section 3 (77%), property-type table  
**Words:** 188

```
Hello,

Of 12 UK regions and nations, Scotland is where buying the average home beats renting it fastest: after 1.4 years, against 4.1 years in the South East of England. Scottish rents are high compared with prices (£1,016 a month on a £196,349 average home, a 6.2% yield) and LBTT for a first-time buyer is £427. After five years the buyer is £20,691 ahead. With flat prices it would take 10.8 years, still the UK's shortest.

First-year mortgage interest is 77% of the rent in Scotland, the lowest share of any region.

Method: the same average home bought or rented, using HM Land Registry and ONS prices and rents for July 2026, a 10% deposit at the Bank of England's quoted 90% LTV rate (5.37%), 3% a year growth in prices and rents (the 2005-2026 average) and the renter investing the difference at 5%.

Full analysis, data and code: https://truthwithdata.com/blog/is-renting-dead-money-uk.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk
Free calculator with regional presets: https://truthwithdata.com/tools/rent-vs-buy-calculator.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk

I can send a chart or the figures by property type for Scotland. Council-level rents aren't published for Scotland, so we compared regions only.

Best wishes,
Vishal Sharma
Truth with Data
truthwithdata@gmail.com
```

### 7. WalesOnline

**To:** newsdesk@walesonline.co.uk  
**Subject:** Wales: from 2 years in Merthyr Tydfil to never in Powys, when buying beats renting  
**Figures from:** LA CSV (Wales rows: Merthyr Tydfil, Monmouthshire, Powys; 11 of 22 within 5y); article region table and section 3  
**Words:** 195

```
Hello,

In Wales, the time it takes for buying the average home to beat renting it ranges from 2.2 years in Merthyr Tydfil to never in Powys, where the buyer is still behind after 30 years. Monmouthshire takes 28 years. Powys has a £237,762 average home that rents for £622 a month, a 3.1% yield. Wales is one of five regions where a first-time buyer's mortgage interest in year one is larger than the rent. If prices stayed flat, buying would never win within 30 years.

With 3% a year price growth, the all-Wales break-even is 3.2 years. Half of Welsh authorities (11 of 22) break even within five years.

Method: the same average home bought or rented, using HM Land Registry and ONS prices and rents for July 2026, a 10% deposit at the Bank of England's quoted 90% LTV rate (5.37%), 3% a year growth in prices and rents (the 2005-2026 average) and the renter investing the difference at 5%.

Full analysis, data and code: https://truthwithdata.com/blog/is-renting-dead-money-uk.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk
Free calculator with regional presets: https://truthwithdata.com/tools/rent-vs-buy-calculator.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk

I can send a chart or the figures for all 22 Welsh authorities.

Best wishes,
Vishal Sharma
Truth with Data
truthwithdata@gmail.com
```

### 8. Devon Live

**To:** (blank)  
**Subject:** Devon: buying beats renting in 17 months in Exeter. In South Hams and East Devon, never  
**Figures from:** LA CSV (Exeter, South Hams, East Devon, West Devon, Plymouth, Torbay)  
**Words:** 185

```
Hello,

Devon has the full range. In Exeter, buying the average home beats renting it after 1.4 years. In South Hams and East Devon the buyer is still behind after 30 years, and West Devon takes 26.7 years. In South Hams the average home costs £355,483 and rents for £1,009 a month (a 3.4% yield); after five years the buyer is £17,377 behind an equivalent renter. Plymouth takes 1.8 years and Torbay 2.6.

Across 316 authorities in England and Wales, 15 never break even within 30 years. Most are expensive rural and commuter districts where rents are low compared with prices.

Method: the same average home bought or rented, using HM Land Registry and ONS prices and rents for July 2026, a 10% deposit at the Bank of England's quoted 90% LTV rate (5.37%), 3% a year growth in prices and rents (the 2005-2026 average) and the renter investing the difference at 5%.

Full analysis, data and code: https://truthwithdata.com/blog/is-renting-dead-money-uk.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk
Free calculator with regional presets: https://truthwithdata.com/tools/rent-vs-buy-calculator.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk

I can send a chart or the figures for every Devon district.

Best wishes,
Vishal Sharma
Truth with Data
truthwithdata@gmail.com
```

### 9. This is Money

**To:** (blank)  
**Subject:** Is rent dead money? First-year mortgage interest is 77-107% of rent across UK regions  
**Figures from:** Article short answer, section 3, key stats, backtest table and section 6  
**Words:** 195

```
Hello,

In the first year, interest on a 90% mortgage for the average home is 77% to 107% of the rent on the same home in every UK region, and more than the rent in five. Add maintenance, insurance and the return the deposit could have earned, and owning costs 5% to 45% more than renting everywhere. Buying comes out ahead through price growth: with prices rising at their 2005-2026 pace of 3% a year, after 1.4 to 4.1 years. If prices stay flat, the median is 26 years.

In a 2005-2026 backtest, 79% of five-year holds left the buyer ahead, but 2022-24 buyers were behind in 8 of 12 regions.

Method: the same average home bought or rented, using HM Land Registry and ONS prices and rents for July 2026, a 10% deposit at the Bank of England's quoted 90% LTV rate (5.37%), 3% a year growth in prices and rents (the 2005-2026 average) and the renter investing the difference at 5%.

Full analysis, data and code: https://truthwithdata.com/blog/is-renting-dead-money-uk.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk
Free calculator with regional presets: https://truthwithdata.com/tools/rent-vs-buy-calculator.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk

I can send charts, regional tables or figures for any local authority.

Best wishes,
Vishal Sharma
Truth with Data
truthwithdata@gmail.com
```

### 10. Guardian Money

**To:** (blank)  
**Subject:** Rent v buy: 2022-24 buyers still behind renters in 8 of 12 UK regions  
**Figures from:** Article section 6 (backtest), section 3, key stats  
**Words:** 191

```
Hello,

People who bought the average home in July 2022, 2023 or 2024 were behind an equivalent renter in 8 of 12 UK regions by July 2026, by a median of 2-5% of the price. That's from a backtest of 2,418 buy-and-sell pairs since 2005, using actual prices, rents and mortgage rates. Over longer periods buying usually won: 79% of five-year holds and 86% of ten-year holds came out ahead. Buyers in 2007 took 6 to 19 years to get ahead.

Looking forward, at today's rates mortgage interest alone is 77-107% of the rent in year one. Buying wins only if prices rise. With flat prices the median break-even is 26 years.

Method: the same average home bought or rented, using HM Land Registry and ONS prices and rents for July 2026, a 10% deposit at the Bank of England's quoted 90% LTV rate (5.37%), 3% a year growth in prices and rents (the 2005-2026 average) and the renter investing the difference at 5%.

Full analysis, data and code: https://truthwithdata.com/blog/is-renting-dead-money-uk.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk
Free calculator with regional presets: https://truthwithdata.com/tools/rent-vs-buy-calculator.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk

I can send charts or regional tables.

Best wishes,
Vishal Sharma
Truth with Data
truthwithdata@gmail.com
```

### 11. Property Industry Eye (trade)

**To:** news@propertyindustryeye.com  
**Subject:** Rent v buy across 316 local authorities: where buying wins within five years, and where it never does  
**Figures from:** Article section 5 and 6; LA CSV  
**Words:** 177

```
Hello,

Buying the average home beats renting it within five years in 181 of 316 local authorities in England and Wales (57%). In 55 it takes more than ten years, and in 15 the buyer is still behind after 30. The deciding factor is gross rental yield (correlation -0.77 with break-even). Fastest: Newcastle (1.0 years), then Manchester, Portsmouth, Bristol and Southampton. Never: Elmbridge, Waverley, Mole Valley, South Hams, Powys and others with yields of 2.7-3.5%.

A backtest against 2005-2026 found buyers from 2022-24 behind an equivalent renter in 8 of 12 regions by July 2026.

Method: the same average home bought or rented, using HM Land Registry and ONS prices and rents for July 2026, a 10% deposit at the Bank of England's quoted 90% LTV rate (5.37%), 3% a year growth in prices and rents (the 2005-2026 average) and the renter investing the difference at 5%.

Full analysis, data and code: https://truthwithdata.com/blog/is-renting-dead-money-uk.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk
Free calculator with regional presets: https://truthwithdata.com/tools/rent-vs-buy-calculator.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk

I can send the full local-authority table or a chart.

Best wishes,
Vishal Sharma
Truth with Data
truthwithdata@gmail.com
```

### 12. Mortgage Solutions (trade)

**To:** shekina.tuahene@ae3media.co.uk  
**Subject:** Rent v buy: what one point on mortgage rates does to the break-even, region by region  
**Figures from:** Article short answer, key stats, section 7 (rate sensitivity), section 3  
**Words:** 183

```
Hello,

At the Bank of England's quoted 90% LTV two-year fix (5.37%, September 2026), buying the average home beats renting it after 1.4 to 4.1 years across UK regions, if prices rise 3% a year. One percentage point more (6.37%) stretches that to 2.3 to 12.2 years. Across regions, the median break-even is 1.3 years at a 4% rate, 4.9 years at 6% and 13 years at 7%. With a 10% deposit, the rate applies to a loan nine times the buyer's stake.

In year one, mortgage interest alone is 77-107% of the rent, and more than the rent in five regions.

Method: the same average home bought or rented, using HM Land Registry and ONS prices and rents for July 2026, a 10% deposit at the Bank of England's quoted 90% LTV rate (5.37%), 3% a year growth in prices and rents (the 2005-2026 average) and the renter investing the difference at 5%.

Full analysis, data and code: https://truthwithdata.com/blog/is-renting-dead-money-uk.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk
Free calculator with regional presets: https://truthwithdata.com/tools/rent-vs-buy-calculator.html?utm_source=press&utm_medium=email&utm_campaign=is-renting-dead-money-uk

I can send the rate-by-price-growth grid or a chart.

Best wishes,
Vishal Sharma
Truth with Data
truthwithdata@gmail.com
```
