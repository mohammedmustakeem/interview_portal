# profit_loss.py
# Arithmetic → Profit & Loss (Intermediate & Expanded Concepts)

AR_PROFIT_LOSS_CONCEPTS = {

    "PL_PROFIT_PERCENT": {
        "topic": "Arithmetic",
        "sub_topic": "Profit & Loss",
        "concept": "Profit Percentage",
        "formula": "profit_percent",
        "unit": "%",
        "params": {
            "cp": ["cp"],
            "sp": ["sp"]
        },
        "param_rules": {
            "cp": {
                "easy": [100, 200, 400],
                "medium": [320, 450, 750, 1200, 1500],
                "hard": [1250, 2400, 5600, 8400]
            },
            "sp": {
                "easy": [120, 250, 500],
                "medium": [384, 540, 900, 1440, 1875],
                "hard": [1500, 3000, 7200, 10500]
            }
        },
        "templates": [
            "An article is bought for {cp} and sold for {sp}. Find the profit percentage.",
            "A trader buys an item at {cp} and sells it at {sp}. What is his profit percent?",
            "If the cost price is {cp} and the selling price is {sp}, calculate the gain percentage.",
            "A wholesale dealer purchases a batch of goods for {cp} and sells them to a retailer for {sp}. Determine the dealer's gain percent.",
            "A second-hand car was purchased for {cp}. After spending some money on repairs, the total cost became {cp} and it was sold for {sp}. Find the profit percent.",
            "Find the percentage profit earned on an investment of {cp} that yielded a return of {sp}."
        ]
    },

    "PL_LOSS_PERCENT": {
        "topic": "Arithmetic",
        "sub_topic": "Profit & Loss",
        "concept": "Loss Percentage",
        "formula": "loss_percent",
        "unit": "%",
        "params": {
            "cp": ["cp"],
            "sp": ["sp"]
        },
        "param_rules": {
            "cp": {
                "easy": [100, 250, 400],
                "medium": [500, 750, 1200, 1600, 2500],
                "hard": [3500, 7200, 10000, 12500]
            },
            "sp": {
                "easy": [80, 200, 300],
                "medium": [425, 600, 960, 1280, 2125],
                "hard": [2800, 6400, 8500, 11000]
            }
        },
        "templates": [
            "An article is bought for {cp} and sold for {sp}. Find the loss percentage.",
            "A shopkeeper incurs a loss by selling an item for {sp} which cost him {cp}. Calculate the loss percent.",
            "If the cost price is {cp} and the selling price is {sp}, determine the loss percentage.",
            "A gadget bought for {cp} was sold for {sp} due to a defect. Calculate the percentage of loss incurred.",
            "A merchant bought a stock of perishable goods for {cp}. Since he had to sell them quickly, he sold them for {sp}. Find his loss percent.",
            "Find the loss percentage if a plot of land purchased for {cp} had to be sold for {sp}."
        ]
    },

    "PL_COST_PRICE": {
        "topic": "Arithmetic",
        "sub_topic": "Profit & Loss",
        "concept": "Cost Price from Profit %",
        "formula": "cost_price_from_sp_profit",
        "unit": "currency",
        "params": {
            "sp": ["sp"],
            "profit": ["profit"]
        },
        "param_rules": {
            "sp": {
                "easy": [110, 220, 440],
                "medium": [690, 825, 1150, 1380, 2500],
                "hard": [2400, 5600, 12800, 16500]
            },
            "profit": {
                "easy": [10, 20],
                "medium": [12, 15, 25, 30],
                "hard": [12.5, 18, 22.5, 37.5]
            }
        },
        "templates": [
            "An article is sold for {sp} at a profit of {profit}%. Find the cost price.",
            "A trader earns a profit of {profit}% by selling an item for {sp}. What was the cost price?",
            "If the selling price is {sp} and profit is {profit}%, calculate the cost price.",
            "Find the initial investment if a businessman made a {profit}% profit on a sale of {sp}.",
            "A smartphone was sold for {sp} at a gain of {profit}%. Determine the price at which the retailer bought it.",
            "By selling an object for {sp}, a person gains {profit}%. At what price did the person acquire the object?"
        ]
    },

    "PL_SELLING_PRICE": {
        "topic": "Arithmetic",
        "sub_topic": "Profit & Loss",
        "concept": "Selling Price from Profit %",
        "formula": "selling_price_from_cp_profit",
        "unit": "currency",
        "params": {
            "cp": ["cp"],
            "profit": ["profit"]
        },
        "param_rules": {
            "cp": {
                "easy": [100, 200, 400],
                "medium": [550, 800, 1250, 1600, 3200],
                "hard": [2400, 5600, 8000, 14500]
            },
            "profit": {
                "easy": [10, 20],
                "medium": [12.5, 15, 18, 25],
                "hard": [14.28, 22.5, 33.33]
            }
        },
        "templates": [
            "Find the selling price of an article costing {cp} if the profit is {profit}%.",
            "A shopkeeper gains {profit}% on an item bought for {cp}. What is the selling price?",
            "If cost price is {cp} and profit is {profit}%, calculate the selling price.",
            "A manufacturer produces a unit at a cost of {cp}. To earn a profit of {profit}%, at what price should he sell it?",
            "What should be the selling price of a product bought for {cp} to realize a gain of {profit}%?",
            "If a dealer wants to make {profit}% profit on an article that cost him {cp}, find the target selling price."
        ]
    },

    "PL_MARKED_PRICE_DISCOUNT": {
        "topic": "Arithmetic",
        "sub_topic": "Profit & Loss",
        "concept": "Marked Price & Discount",
        "formula": "selling_price_after_discount",
        "unit": "currency",
        "params": {
            "mp": ["mp"],
            "discount": ["discount"]
        },
        "param_rules": {
            "mp": {
                "easy": [200, 400, 800],
                "medium": [1250, 2400, 3500, 4800, 6000],
                "hard": [7200, 9600, 14400, 25000]
            },
            "discount": {
                "easy": [10, 20],
                "medium": [12, 15, 25, 30],
                "hard": [12.5, 17.5, 33.33, 45]
            }
        },
        "templates": [
            "An article marked at {mp} is sold at a discount of {discount}%. Find the selling price.",
            "A shopkeeper allows a discount of {discount}% on a marked price of {mp}. What is the selling price?",
            "If marked price is {mp} and discount is {discount}%, calculate the selling price.",
            "During a festive sale, an appliance with a tag price of {mp} is offered at {discount}% off. Calculate the final price to the customer.",
            "Find the amount a customer has to pay for a dress marked {mp} if the store offers a {discount}% seasonal discount.",
            "A publisher lists a book at {mp}. If a library gets a {discount}% discount on the listed price, how much does the library pay?"
        ]
    }
}
