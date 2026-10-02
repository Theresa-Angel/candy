"""Nassau Candy — synthetic sales data generator (8000 rows, 2021-2024)."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random, os

np.random.seed(42)
random.seed(42)

FACTORIES = {
    "Lot's O' Nuts":     {"lat": 32.881893, "lon": -111.768036},
    "Wicked Choccy's":   {"lat": 32.076176, "lon":  -81.088371},
    "Sugar Shack":       {"lat": 48.119140, "lon":  -96.181150},
    "Secret Factory":    {"lat": 41.446333, "lon":  -90.565487},
    "The Other Factory": {"lat": 35.117500, "lon":  -89.971107},
}

PRODUCTS = [
    ("Chocolate","Wonka Bar - Nutty Crunch Surprise","Lot's O' Nuts",    3.50,0.42),
    ("Chocolate","Wonka Bar - Fudge Mallows",        "Lot's O' Nuts",    3.20,0.38),
    ("Chocolate","Wonka Bar - Scrumdiddlyumptious",  "Lot's O' Nuts",    4.00,0.45),
    ("Chocolate","Wonka Bar - Milk Chocolate",       "Wicked Choccy's",  2.80,0.35),
    ("Chocolate","Wonka Bar - Triple Dazzle Caramel","Wicked Choccy's",  3.90,0.40),
    ("Sugar",    "Laffy Taffy",                      "Sugar Shack",      1.50,0.48),
    ("Sugar",    "SweeTARTS",                        "Sugar Shack",      1.20,0.52),
    ("Sugar",    "Nerds",                            "Sugar Shack",      1.10,0.55),
    ("Sugar",    "Fun Dip",                          "Sugar Shack",      1.30,0.50),
    ("Sugar",    "Everlasting Gobstopper",           "Secret Factory",   2.50,0.60),
    ("Sugar",    "Hair Toffee",                      "The Other Factory",2.00,0.30),
    ("Other",    "Fizzy Lifting Drinks",             "Sugar Shack",      5.00,0.25),
    ("Other",    "Lickable Wallpaper",               "Secret Factory",   8.00,0.18),
    ("Other",    "Wonka Gum",                        "Secret Factory",   6.50,0.22),
    ("Other",    "Kazookles",                        "The Other Factory",4.50,0.28),
]

CITIES = {
    "East":   [("New York","NY",40.7128,-74.0060),("Philadelphia","PA",39.9526,-75.1652),
               ("Boston","MA",42.3601,-71.0589),("Baltimore","MD",39.2904,-76.6122),
               ("Charlotte","NC",35.2271,-80.8431)],
    "West":   [("Los Angeles","CA",34.0522,-118.2437),("Seattle","WA",47.6062,-122.3321),
               ("Phoenix","AZ",33.4484,-112.0740),("Denver","CO",39.7392,-104.9903),
               ("Portland","OR",45.5051,-122.6750)],
    "Central":[("Chicago","IL",41.8781,-87.6298),("Dallas","TX",32.7767,-96.7970),
               ("Houston","TX",29.7604,-95.3698),("Minneapolis","MN",44.9778,-93.2650),
               ("Kansas City","MO",39.0997,-94.5786)],
    "South":  [("Miami","FL",25.7617,-80.1918),("Atlanta","GA",33.7490,-84.3880),
               ("New Orleans","LA",29.9511,-90.0715),("Nashville","TN",36.1627,-86.7816),
               ("Memphis","TN",35.1495,-90.0490)],
}

SHIP_MODES   = ["Standard Class","Second Class","First Class","Same Day"]
SHIP_W       = [0.50,0.25,0.20,0.05]
SHIP_DAYS    = {"Standard Class":(4,7),"Second Class":(2,4),"First Class":(1,3),"Same Day":(0,0)}
SEGMENTS     = ["Retail","Wholesale","Online"]
CUST_IDS     = [f"CUST-{i:04d}" for i in range(1000,2001)]
CUST_SEG     = {c: random.choice(SEGMENTS) for c in CUST_IDS}

start = datetime(2021,1,1)
end   = datetime(2024,12,31)
span  = (end-start).days

rows = []
for i in range(8000):
    div,prod,factory,base_p,base_m = random.choice(PRODUCTS)
    region = random.choice(list(CITIES.keys()))
    city,state,clat,clon = random.choice(CITIES[region])
    odate  = start + timedelta(days=random.randint(0,span))
    smode  = random.choices(SHIP_MODES,SHIP_W)[0]
    lo,hi  = SHIP_DAYS[smode]
    sdays  = random.randint(lo,hi)
    sdate  = odate + timedelta(days=sdays)
    units  = random.randint(10,500)
    season = 1 + 0.18*np.sin(2*np.pi*(odate.month-3)/12)
    trend  = 1 + 0.04*(odate.year-2021)
    price  = round(base_p*season*trend*np.random.normal(1.0,0.05),2)
    sales  = round(price*units,2)
    margin = max(0.05,min(0.75,np.random.normal(base_m,0.04)))
    gp     = round(sales*margin,2)
    cost   = round(sales-gp,2)
    cust   = random.choice(CUST_IDS)
    pidx   = PRODUCTS.index((div,prod,factory,base_p,base_m))
    fi     = FACTORIES[factory]
    rows.append({
        "Row ID":i+1, "Order ID":f"ORD-{odate.year}-{i:05d}",
        "Order Date":odate.strftime("%Y-%m-%d"),
        "Ship Date":sdate.strftime("%Y-%m-%d"),
        "Ship Mode":smode,"Ship Days":sdays,
        "Customer ID":cust,"Customer Segment":CUST_SEG[cust],
        "Country/Region":"United States",
        "City":city,"State/Province":state,
        "Customer Lat":clat,"Customer Lon":clon,
        "Region":region,"Division":div,
        "Product ID":f"PROD-{pidx:03d}","Product Name":prod,
        "Factory":factory,"Factory Lat":fi["lat"],"Factory Lon":fi["lon"],
        "Sales":sales,"Units":units,"Gross Profit":gp,"Cost":cost,
    })

os.makedirs("data",exist_ok=True)
pd.DataFrame(rows).to_csv("data/nassau_candy_sales.csv",index=False)
print(f"Generated {len(rows)} rows -> data/nassau_candy_sales.csv")
