# percentage.py
# Arithmetic → Percentages (Intermediate & Expanded Concepts)

AR_PERCENTAGE_CONCEPTS = {

    "PERCENTAGE_REVERSE_INCREASE": {
        "topic": "Arithmetic",
        "sub_topic": "Percentages",
        "concept": "Reverse Percentage (Increase)",
        "formula": "original_from_final_percent",
        "params": {
            "final_value": ["final_value"],
            "percent_change": ["percent_change"]
        },
        "param_rules": {
            "final_value": {
                "easy": [120, 240, 360],
                "medium": [575, 840, 1125, 1440, 2250], # Values requiring more mental division
                "hard": [4560, 8424, 15600, 28800]
            },
            "percent_change": {
                "easy": [10, 20, 50],
                "medium": [12, 15, 25, 35, 45], # Intermediate percentages
                "hard": [12.5, 17.5, 22.5, 37.5]
            }
        },
        "templates": [
            "After an increase of {percent_change}%, a number becomes {final_value}. Find the original number.",
            "A monthly salary becomes {final_value} after a {percent_change}% hike. What was the salary before the increment?",
            "The price of a luxury watch inclusive of {percent_change}% sales tax is {final_value}. Calculate its price before tax.",
            "A town's population rose by {percent_change}% over a year and is now {final_value}. What was the population at the start of the year?",
            "After adding {percent_change}% interest, a bank balance reaches {final_value}. Determine the initial principal amount.",
            "If a company's revenue reaches {final_value} after growing by {percent_change}% from the previous quarter, what was the earlier revenue?"
        ]
    },

    "PERCENTAGE_REVERSE_DECREASE": {
        "topic": "Arithmetic",
        "sub_topic": "Percentages",
        "concept": "Reverse Percentage (Decrease)",
        "formula": "original_from_final_decrease",
        "params": {
            "final_value": ["final_value"],
            "percent_change": ["percent_change"]
        },
        "param_rules": {
            "final_value": {
                "easy": [80, 160, 240],
                "medium": [425, 630, 850, 1080, 1575],
                "hard": [3150, 6240, 9750, 14200]
            },
            "percent_change": {
                "easy": [10, 20, 50],
                "medium": [15, 25, 30, 40],
                "hard": [12.5, 18.75, 37.5, 62.5]
            }
        },
        "templates": [
            "After a decrease of {percent_change}%, a number becomes {final_value}. Find the original number.",
            "A pair of shoes is sold for {final_value} after a discount of {percent_change}%. What was the marked price?",
            "If a car's value depreciates by {percent_change}% and becomes {final_value}, find its value at the time of purchase.",
            "The weight of a metal ore reduces by {percent_change}% during processing to {final_value} kg. Find the initial weight.",
            "A student's marks decreased by {percent_change}% in the second term to {final_value}. How many marks did the student score in the first term?",
            "After losing {percent_change}% of its water due to evaporation, a tank contains {final_value} liters. What was the original volume?"
        ]
    },

    "PERCENTAGE_SUCCESSIVE_CHANGE": {
        "topic": "Arithmetic",
        "sub_topic": "Percentages",
        "concept": "Successive Percentage Change",
        "formula": "successive_percent_change",
        "params": {
            "percent_1": ["percent_1"],
            "percent_2": ["percent_2"]
        },
        "param_rules": {
            "percent_1": {
                "easy": [10, 20],
                "medium": [12, 15, 25, 30],
                "hard": [12.5, 33.33, 40]
            },
            "percent_2": {
                "easy": [10, 20],
                "medium": [10, 20, 25, 40],
                "hard": [11.11, 25, 37.5]
            }
        },
        "templates": [
            "A value is increased by {percent_1}% and then increased again by {percent_2}%. Find the net percentage change.",
            "An item's price is increased by {percent_1}% and then a further increase of {percent_2}% is applied. What is the total effective increase?",
            "A company's production grows by {percent_1}% in the first year and by {percent_2}% in the second year. Calculate the overall growth percentage.",
            "If the price of fuel rises by {percent_1}% in January and {percent_2}% in February, what is the net percentage rise at the end of February?",
            "A trader marks up his goods by {percent_1}% and then gives another {percent_2}% hike. Find the cumulative percentage increase.",
            "Find the equivalent single percentage change for two successive increases of {percent_1}% and {percent_2}%."
        ]
    },

    "PERCENTAGE_COMPARISON": {
        "topic": "Arithmetic",
        "sub_topic": "Percentages",
        "concept": "Percentage Comparison",
        "formula": "percentage_difference",
        "params": {
            "value_a": ["value_a"],
            "value_b": ["value_b"]
        },
        "param_rules": {
            "value_a": {
                "easy": [40, 60, 80],
                "medium": [135, 175, 225, 315, 450],
                "hard": [560, 840, 1260, 2100]
            },
            "value_b": {
                "easy": [50, 75, 100],
                "medium": [150, 250, 300, 450, 600],
                "hard": [700, 1050, 1400, 2800]
            }
        },
        "templates": [
            "By what percentage is {value_a} less than {value_b}?",
            "Calculate the percentage increase required to go from {value_a} to {value_b}.",
            "If A's salary is {value_a} and B's salary is {value_b}, by what percentage is A's salary lower than B's?",
            "A shopkeeper bought an item for {value_a} and sold it for {value_b}. Find his profit percentage.",
            "In a test, Alice scored {value_a} marks while Bob scored {value_b} marks. By what percent are Alice's marks less than Bob's?",
            "The price of a commodity changed from {value_b} to {value_a}. Find the percentage decrease in price."
        ]
    },

    "PERCENTAGE_NET_CHANGE": {
        "topic": "Arithmetic",
        "sub_topic": "Percentages",
        "concept": "Net Percentage Change",
        "formula": "net_percent_change",
        "params": {
            "increase": ["increase"],
            "decrease": ["decrease"]
        },
        "param_rules": {
            "increase": {
                "easy": [10, 20],
                "medium": [15, 25, 30, 40],
                "hard": [12.5, 37.5, 50, 60]
            },
            "decrease": {
                "easy": [10, 20],
                "medium": [10, 15, 20, 25],
                "hard": [12.5, 16.66, 33.33, 40]
            }
        },
        "templates": [
            "A value increases by {increase}% and then decreases by {decrease}%. Find the net percentage change.",
            "The price of an item is increased by {increase}% and later reduced by {decrease}%. What is the net percentage effect on the price?",
            "If a worker's wages are increased by {increase}% and then decreased by {decrease}%, what is the net change in his income?",
            "In a retail store, the price is hiked by {increase}% but then a discount of {decrease}% is offered during a sale. Find the overall percentage change.",
            "The length of a rectangle is increased by {increase}% and its breadth is decreased by {decrease}%. Find the percentage change in its area.",
            "A population increases by {increase}% due to migration but then decreases by {decrease}% due to a local epidemic. Calculate the net percentage change in population."
        ]
    }
}
