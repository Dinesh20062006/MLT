"""
Synthetic Expense Transaction Dataset Generator
For Academic Experimentation - Smart Expense Category Prediction & Financial Analytics

Ethics Notice:
This dataset is synthetically generated for academic experimentation and does not
represent real users or real financial transactions.
"""

import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

RANDOM_SEED = 42
TOTAL_RECORDS = 18000

# Category configurations with realistic descriptions, merchants, amounts, and payment methods
CATEGORIES_DATA = {
    "Food": {
        "templates": [
            "{merchant} dinner", "{merchant} lunch", "{merchant} breakfast",
            "{merchant} order", "Delicious {dish} at {merchant}", "Takeout from {merchant}",
            "Grocery shopping at {merchant}", "Fresh vegetables at {merchant}",
            "Coffee and snacks at {merchant}", "Bakery purchase at {merchant}",
            "Late night pizza from {merchant}", "Burger combo at {merchant}",
            "Ice cream with friends at {merchant}", "Office tea and samosa at {merchant}",
            "Biryani treat from {merchant}", "South Indian breakfast at {merchant}",
            "Family restaurant buffet at {merchant}", "Juice bar refreshments at {merchant}",
            "Supermarket pantry refill at {merchant}", "Weekly grocery basket at {merchant}",
            "{dish} delivery", "Quick bite at {merchant}", "Snacks and beverages {merchant}",
            "Weekend food order", "Casual dining", "Evening cafeteria snack", "Online meal order"
        ],
        "merchants": [
            "Swiggy", "Zomato", "Blinkit", "Zepto", "Instamart", "McDonald's", "Dominos Pizza",
            "Starbucks", "KFC", "Haldiram's", "Barbeque Nation", "Subway", "Chai Point",
            "Local Supermarket", "BigBasket", "Nature's Basket", "Cafe Coffee Day",
            "Pizza Hut", "Dunkin Donuts", "Street Food Corner", "Sangeetha Veg", "Udipi Bhavan",
            "Amazon", "Tata Neu"
        ],
        "dishes": [
            "Biryani", "Pizza", "Burger", "Dosa", "Sandwich", "Pasta", "Shawarma", "Fried Rice",
            "Noodles", "Paneer Tikka", "Cold Coffee", "Chai", "Paratha", "Salad", "Sushi"
        ],
        "amount_range": (80, 2600),
        "amount_mean": 420,
        "amount_std": 280,
        "payment_weights": [0.65, 0.15, 0.10, 0.05, 0.05]
    },
    "Transportation": {
        "templates": [
            "{merchant} ride to office", "{merchant} ride to college", "{merchant} trip to airport",
            "{merchant} auto fare", "{merchant} cab booking", "{merchant} bike taxi ride",
            "Fuel refill at {merchant}", "Petrol tank full at {merchant}", "Diesel top-up at {merchant}",
            "Metro smart card recharge via {merchant}", "Local bus monthly pass at {merchant}",
            "Train ticket reservation on {merchant}", "Intercity bus booking on {merchant}",
            "Toll plaza payment via {merchant}", "Airport parking fee at {merchant}",
            "EV charging station fee at {merchant}", "Scooter rental via {merchant}",
            "Vehicle service oil change at {merchant}", "Fastag automatic toll recharge {merchant}",
            "Weekly transit pass", "Commute fare", "Travel recharge", "Express transport ticket"
        ],
        "merchants": [
            "Uber", "Ola", "Rapido", "Namma Yatri", "Indian Oil", "Bharat Petroleum",
            "HP Fuel Station", "Shell Petrol Pump", "IRCTC", "RedBus", "AbhiBus",
            "Delhi Metro", "Bangalore Metro", "Fastag Toll", "MakeMyTrip",
            "Yulu Bikes", "BluSmart Cab", "City Bus Depot", "Zoomcar", "Google Pay"
        ],
        "dishes": [],
        "amount_range": (40, 3500),
        "amount_mean": 380,
        "amount_std": 350,
        "payment_weights": [0.60, 0.18, 0.12, 0.05, 0.05]
    },
    "Shopping": {
        "templates": [
            "{merchant} clothing purchase", "{merchant} electronic gadget order",
            "{merchant} running shoes purchase", "Summer apparel sale on {merchant}",
            "Wireless headphones bought on {merchant}", "Home decor item from {merchant}",
            "Office desk accessories on {merchant}", "Smartphone case and screen protector {merchant}",
            "Smartwatch order from {merchant}", "Backpack and luggage from {merchant}",
            "Beauty products and skincare at {merchant}", "Kitchen cookware set from {merchant}",
            "Branded formal shirts at {merchant}", "Denim jeans purchase at {merchant}",
            "Festive gift hampers from {merchant}", "Fitness gear and dumbbells on {merchant}",
            "Perfume and cosmetics at {merchant}", "Casual sneakers from {merchant}",
            "Online store order", "Weekend retail purchase", "Festival seasonal shopping", "Product order"
        ],
        "merchants": [
            "Amazon", "Flipkart", "Myntra", "Ajio", "Zara", "H&M", "Nike Store",
            "Croma", "Reliance Digital", "Nykaa", "Decathlon", "Shoppers Stop",
            "Westside", "Tata CLiQ", "Uniqlo", "Levi's Store", "IKEA", "Puma", "Apple"
        ],
        "dishes": [],
        "amount_range": (250, 18500),
        "amount_mean": 2400,
        "amount_std": 1900,
        "payment_weights": [0.35, 0.40, 0.15, 0.08, 0.02]
    },
    "Entertainment": {
        "templates": [
            "{merchant} monthly premium subscription", "{merchant} annual plan renewal",
            "Weekend blockbuster movie tickets on {merchant}", "IMAX 3D cinema booking via {merchant}",
            "Live music concert pass on {merchant}", "Standup comedy evening show tickets on {merchant}",
            "Online gaming battle pass on {merchant}", "Gaming console digital game purchase on {merchant}",
            "Audiobook and podcast membership on {merchant}", "Amusement park entry pass at {merchant}",
            "Streaming video family pack on {merchant}", "Music streaming student discount {merchant}",
            "Board games cafe entry at {merchant}", "Bowling arena evening pass at {merchant}",
            "Monthly subscription pack", "Weekend entertainment ticket", "Digital media pass", "Annual membership fee"
        ],
        "merchants": [
            "Netflix", "Spotify", "BookMyShow", "Amazon", "Disney+ Hotstar",
            "YouTube Premium", "Sony LIV", "PVR INOX", "Apple", "PlayStation Network",
            "Steam Games", "Audible", "Cinepolis", "Comic Con", "Wonderla Parks", "Google"
        ],
        "dishes": [],
        "amount_range": (149, 4500),
        "amount_mean": 750,
        "amount_std": 600,
        "payment_weights": [0.45, 0.35, 0.12, 0.07, 0.01]
    },
    "Utilities": {
        "templates": [
            "{merchant} monthly electricity consumption bill", "{merchant} piped kitchen gas bill payment",
            "{merchant} broadband high-speed fiber bill", "{merchant} postpaid mobile family plan",
            "{merchant} prepaid SIM validity recharge", "{merchant} municipal water supply tax",
            "{merchant} apartment maintenance society fee", "{merchant} DTH satellite TV monthly recharge",
            "{merchant} LPG cooking cylinder refill", "{merchant} trash collection and utility levy",
            "Solar panel grid maintenance fee at {merchant}", "Landline broadband combo bill on {merchant}",
            "Monthly recurring bill payment", "Utility account payment", "Service connection bill", "Scheduled monthly charge"
        ],
        "merchants": [
            "Bescom Electricity", "Tata Power", "Adani Electricity", "Mahanagar Gas",
            "Indane Gas", "Airtel Broadband", "Jio Fiber", "ACT Fibernet", "Vi Prepaid",
            "BSNL Telecom", "Municipal Water Board", "Tata Play", "Airtel",
            "MyGate Society", "Cred", "Amazon Pay", "Google Pay"
        ],
        "dishes": [],
        "amount_range": (299, 8500),
        "amount_mean": 1850,
        "amount_std": 1200,
        "payment_weights": [0.55, 0.20, 0.15, 0.09, 0.01]
    },
    "Healthcare": {
        "templates": [
            "{merchant} doctor specialist consultation fee", "Prescription medicines purchase at {merchant}",
            "Annual whole body checkup package at {merchant}", "Dental cleaning and root canal at {merchant}",
            "Diagnostic blood test pathology report at {merchant}", "Eye clinic checkup and optical lens at {merchant}",
            "Physiotherapy rehabilitation session at {merchant}", "First aid supplies and vitamins at {merchant}",
            "Hospital emergency OPD visit at {merchant}", "Health insurance copay at {merchant}",
            "Dermatologist consultation and ointment from {merchant}", "Ayurvedic herbal medicines at {merchant}",
            "Medical prescription refill", "Clinic consultation fee", "Pharmacy healthcare bill", "Health test charges"
        ],
        "merchants": [
            "Apollo Pharmacy", "MedPlus", "1mg", "PharmEasy", "Netmeds", "Practo Care",
            "Manipal Hospital", "Max Healthcare", "Fortis Hospital", "Dr Lal PathLabs",
            "Metropolis Pathology", "Lenskart Clinic", "Clove Dental", "Suburban Diagnostics", "Tata 1mg"
        ],
        "dishes": [],
        "amount_range": (150, 12500),
        "amount_mean": 1950,
        "amount_std": 1650,
        "payment_weights": [0.40, 0.30, 0.20, 0.05, 0.05]
    },
    "Education": {
        "templates": [
            "{merchant} semester tuition fee installment", "{merchant} online certification course enrollment",
            "Academic textbook and study material from {merchant}", "{merchant} competitive exam registration fee",
            "Coding bootcamp monthly installment on {merchant}", "{merchant} cloud computing lab subscription",
            "Language learning yearly membership on {merchant}", "School stationery and notebook supplies at {merchant}",
            "GRE TOEFL mock exam prep test series on {merchant}", "University admission application processing {merchant}",
            "AI and machine learning masterclass at {merchant}", "Library membership fee at {merchant}",
            "Annual membership fee", "Monthly learning subscription", "Educational certification enrollment", "Online course fee"
        ],
        "merchants": [
            "Coursera", "Udemy", "edX", "UpGrad", "Scaler Academy", "Duolingo Plus",
            "Oxford Book Store", "Crossword Books", "National Testing Agency",
            "College Board", "Simplilearn", "LeetCode Premium", "Pluralsight",
            "University Office", "Wiley Publications", "Cambridge Press", "Amazon", "Google"
        ],
        "dishes": [],
        "amount_range": (350, 36000),
        "amount_mean": 4200,
        "amount_std": 3800,
        "payment_weights": [0.35, 0.35, 0.18, 0.11, 0.01]
    },
    "Other": {
        "templates": [
            "{merchant} miscellaneous household maintenance", "{merchant} courier parcel speed post charges",
            "{merchant} key duplication and locksmith service", "{merchant} pet grooming and dog food care",
            "{merchant} dry cleaning and laundry service", "{merchant} tailoring and clothing alteration",
            "{merchant} charity donation relief fund", "{merchant} passport visa document legal notary stamp",
            "{merchant} vehicle wash and detailing service", "{merchant} general hardware store tools purchase",
            "{merchant} stationary printing and xerox copies", "{merchant} gift wrapping and greeting card",
            "General personal expense", "Miscellaneous payment", "Service charge fee", "Quick routine expense"
        ],
        "merchants": [
            "India Post", "BlueDart Courier", "DHL Express", "Urban Company",
            "Fabrico Laundry", "Heads Up For Tails", "Local Hardware Store",
            "Prime Notary Services", "Prime Dry Cleaners", "Pet Store & Vet Care",
            "Rotary Charity Fund", "Quick Print Xerox", "Local Crafts Store", "Amazon", "Cred"
        ],
        "dishes": [],
        "amount_range": (100, 6500),
        "amount_mean": 850,
        "amount_std": 650,
        "payment_weights": [0.55, 0.15, 0.15, 0.05, 0.10]
    }
}

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"]


def generate_dataset(output_dir: str = "ml/data", num_records: int = TOTAL_RECORDS) -> str:
    """Generate the synthetic expense dataset with realistic distributions and cross-category vocabulary."""
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    os.makedirs(output_dir, exist_ok=True)
    records = []

    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 9, 30)
    date_delta_days = (end_date - start_date).days

    categories = list(CATEGORIES_DATA.keys())
    base_per_category = num_records // len(categories)

    txn_id = 10001
    for category in categories:
        cat_config = CATEGORIES_DATA[category]
        records_to_generate = base_per_category

        for _ in range(records_to_generate):
            template = random.choice(cat_config["templates"])
            merchant = random.choice(cat_config["merchants"])
            dish = random.choice(cat_config["dishes"]) if cat_config["dishes"] else ""

            description = template.format(merchant=merchant, dish=dish)

            min_amt, max_amt = cat_config["amount_range"]
            mean_amt = cat_config["amount_mean"]
            std_amt = cat_config["amount_std"]

            raw_amt = np.random.normal(mean_amt, std_amt)
            amt = max(min_amt, min(max_amt, raw_amt))
            if amt > 500:
                amount = int(round(amt / 10.0) * 10)
            else:
                amount = int(round(amt))

            payment_method = random.choices(PAYMENT_METHODS, weights=cat_config["payment_weights"])[0]

            random_days = random.randint(0, date_delta_days)
            txn_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

            records.append({
                "transaction_id": txn_id,
                "description": description,
                "amount": amount,
                "merchant": merchant,
                "payment_method": payment_method,
                "transaction_date": txn_date,
                "category": category
            })
            txn_id += 1

    df = pd.DataFrame(records)
    df = df.sample(frac=1.0, random_state=RANDOM_SEED).reset_index(drop=True)

    csv_path = os.path.join(output_dir, "expense_dataset.csv")
    df.to_csv(csv_path, index=False)
    print(f"Generated {len(df)} records in {csv_path}")

    generate_report(df, output_dir)
    return csv_path


def generate_report(df: pd.DataFrame, output_dir: str):
    """Generate detailed dataset summary report."""
    report_path = os.path.join(output_dir, "dataset_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 65 + "\n")
        f.write("SYNTHETIC EXPENSE TRANSACTION DATASET REPORT\n")
        f.write("Academic Mini-Project: Smart Expense Category Prediction\n")
        f.write("=" * 65 + "\n\n")

        f.write("ETHICS & EXPERIMENTATION NOTICE:\n")
        f.write("This dataset is synthetically generated for academic experimentation\n")
        f.write("and does not represent real users or real financial transactions.\n\n")

        f.write(f"Total Transactions : {len(df):,}\n")
        f.write(f"Total Categories   : {df['category'].nunique()}\n")
        f.write(f"Missing Values     : {df.isnull().sum().sum()}\n")
        f.write(f"Duplicate Rows     : {df.duplicated().sum()}\n")
        f.write(f"Unique Merchants   : {df['merchant'].nunique()}\n")
        f.write(f"Date Span          : {df['transaction_date'].min()} to {df['transaction_date'].max()}\n\n")

        f.write("-" * 45 + "\n")
        f.write("RECORDS PER CATEGORY:\n")
        f.write("-" * 45 + "\n")
        cat_counts = df["category"].value_counts()
        for cat, count in cat_counts.items():
            f.write(f"  - {cat:<18}: {count:>5} records ({count/len(df)*100:.1f}%)\n")

        f.write("\n" + "-" * 45 + "\n")
        f.write("PAYMENT METHOD DISTRIBUTION:\n")
        f.write("-" * 45 + "\n")
        pm_counts = df["payment_method"].value_counts()
        for pm, count in pm_counts.items():
            f.write(f"  - {pm:<18}: {count:>5} ({count/len(df)*100:.1f}%)\n")

        f.write("\n" + "-" * 45 + "\n")
        f.write("TRANSACTION AMOUNT STATISTICS (INR):\n")
        f.write("-" * 45 + "\n")
        stats = df["amount"].describe()
        f.write(f"  - Mean Amount    : ₹{stats['mean']:,.2f}\n")
        f.write(f"  - Std Deviation  : ₹{stats['std']:,.2f}\n")
        f.write(f"  - Minimum Amount : ₹{stats['min']:,.2f}\n")
        f.write(f"  - 25th Percentile: ₹{stats['25%']:,.2f}\n")
        f.write(f"  - Median (50%)   : ₹{stats['50%']:,.2f}\n")
        f.write(f"  - 75th Percentile: ₹{stats['75%']:,.2f}\n")
        f.write(f"  - Maximum Amount : ₹{stats['max']:,.2f}\n\n")

        f.write("-" * 45 + "\n")
        f.write("CATEGORY AMOUNT BREAKDOWN:\n")
        f.write("-" * 45 + "\n")
        cat_stats = df.groupby("category")["amount"].agg(["mean", "median", "min", "max"])
        for cat, row in cat_stats.iterrows():
            f.write(f"  - {cat:<15}: Mean=₹{row['mean']:>7.1f} | Med=₹{row['median']:>5.0f} | Min=₹{row['min']:>4.0f} | Max=₹{row['max']:>6.0f}\n")

        f.write("\n" + "=" * 65 + "\n")

    print(f"Report written to {report_path}")


if __name__ == "__main__":
    generate_dataset()
