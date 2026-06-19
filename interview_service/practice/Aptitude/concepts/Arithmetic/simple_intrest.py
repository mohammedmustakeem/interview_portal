AR_SIMPLE_INTREST_CONCEPTS = {
    
    "SI_AMOUNT": {
    "topic": "Arithmetic",
    "sub_topic": "Simple Interest",
    "concept": "Amount from Principal, Rate and Time",
    "formula": "amount_simple_interest",
    "unit": "currency",
    "params": {
        "p": ["principal"],
        "r": ["rate"],
        "t": ["time"]
    },
    "param_rules": {
        "p": {
            "easy": [500, 1000, 2000],
            "medium": [3500, 4800, 7200],
            "hard": [12500, 18600, 25000]
        },
        "r": {
            "easy": [5, 10],
            "medium": [6.25, 8, 12],
            "hard": [13.5, 16.67]
        },
        "t": {
            "easy": [1, 2],
            "medium": [2.5, 3],
            "hard": [4, 5]
        }
    },
    "templates": [
        "Find the total amount after {t} years on a principal of {p} at {r}% simple interest.",
        "What will be the amount if {p} is invested for {t} years at {r}% SI?",
        "Calculate the final amount when {p} earns simple interest at {r}% per annum for {t} years.",
        "An investment of {p} grows at {r}% SI for {t} years. Find the amount.",
        "What sum will be received after {t} years if {p} is invested at {r}% simple interest?"
    ]
},
    "SI_INTEREST": {
    "topic": "Arithmetic",
    "sub_topic": "Simple Interest",
    "concept": "Simple Interest from Principal, Rate and Time",
    "formula": "simple_interest",
    "unit": "currency",
    "params": {
        "p": ["principal"],
        "r": ["rate"],
        "t": ["time"]
    },
    "param_rules": {
        "p": {
            "easy": [400, 800, 1200],
            "medium": [2500, 3600, 5400],
            "hard": [9800, 14500]
        },
        "r": {
            "easy": [5, 10],
            "medium": [7.5, 12],
            "hard": [14.4, 18]
        },
        "t": {
            "easy": [1, 2],
            "medium": [3, 4],
            "hard": [5, 6]
        }
    },
    "templates": [
        "Find the simple interest on {p} at {r}% per annum for {t} years.",
        "What interest will be earned on {p} in {t} years at {r}% SI?",
        "Calculate the interest obtained if {p} is invested at {r}% for {t} years.",
        "How much interest does {p} earn at {r}% SI in {t} years?",
        "Determine the simple interest for principal {p}, rate {r}% and time {t} years."
    ]
},
    "SI_PRINCIPAL": {
    "topic": "Arithmetic",
    "sub_topic": "Simple Interest",
    "concept": "Principal from Simple Interest",
    "formula": "principal_from_si",
    "unit": "currency",
    "params": {
        "si": ["interest"],
        "r": ["rate"],
        "t": ["time"]
    },
    "param_rules": {
        "si": {
            "easy": [100, 200],
            "medium": [450, 720],
            "hard": [1250, 1800]
        },
        "r": {
            "easy": [5, 10],
            "medium": [12, 15],
            "hard": [16.67, 20]
        },
        "t": {
            "easy": [1, 2],
            "medium": [3, 4],
            "hard": [5, 6]
        }
    },
    "templates": [
        "Find the principal if the simple interest earned is {si} at {r}% for {t} years.",
        "What was the original sum if {si} is earned at {r}% SI in {t} years?",
        "Determine the principal that yields an interest of {si} in {t} years at {r}%.",
        "If the simple interest is {si} at {r}% for {t} years, find the principal."
    ]
},
    
    "SI_RATE": {
    "topic": "Arithmetic",
    "sub_topic": "Simple Interest",
    "concept": "Rate of Interest from Simple Interest",
    "formula": "rate_from_si",
    "unit": "percentage",
    "params": {
        "p": ["principal"],
        "si": ["interest"],
        "t": ["time"]
    },
    "param_rules": {
        "p": {
            "easy": [500, 1000],
            "medium": [2400, 3600],
            "hard": [8000, 12000]
        },
        "si": {
            "easy": [50, 100],
            "medium": [360, 540],
            "hard": [1600, 2400]
        },
        "t": {
            "easy": [1, 2],
            "medium": [3, 4],
            "hard": [5, 6]
        }
    },
    "templates": [
        "Find the rate of interest if {si} is earned on {p} in {t} years.",
        "At what rate percent per annum does {p} earn {si} in {t} years?",
        "Determine the rate of simple interest for principal {p}, interest {si} and time {t}.",
        "What is the annual rate if simple interest is {si} on {p} for {t} years?"
    ]
},
    
    "SI_TIME": {
    "topic": "Arithmetic",
    "sub_topic": "Simple Interest",
    "concept": "Time from Simple Interest",
    "formula": "time_from_si",
    "unit": "years",
    "params": {
        "p": ["principal"],
        "si": ["interest"],
        "r": ["rate"]
    },
    "param_rules": {
        "p": {
            "easy": [500, 1000],
            "medium": [2400, 3600],
            "hard": [8000, 12000]
        },
        "si": {
            "easy": [100, 200],
            "medium": [600, 900],
            "hard": [2400, 3600]
        },
        "r": {
            "easy": [5, 10],
            "medium": [12, 15],
            "hard": [18, 20]
        }
    },
    "templates": [
        "Find the time for which {p} earns an interest of {si} at {r}% SI.",
        "How many years will it take for {p} to earn {si} at {r}%?",
        "Determine the time if simple interest is {si} on {p} at {r}%.",
        "For what duration was {p} invested to get interest {si} at {r}%?"
    ]
},
    
    "SI_AMOUNT_DIFF": {
    "topic": "Arithmetic",
    "sub_topic": "Simple Interest",
    "concept": "Difference between Amounts at Different Times",
    "formula": "amount_difference_si",
    "unit": "currency",
    "params": {
        "p": ["principal"],
        "r": ["rate"],
        "t1": ["time1"],
        "t2": ["time2"]
    },
    "param_rules": {
        "p": {
            "easy": [1000, 2000],
            "medium": [3600, 4800],
            "hard": [12000, 18000]
        },
        "r": {
            "easy": [5, 10],
            "medium": [12],
            "hard": [15]
        },
        "t1": {
            "easy": [1],
            "medium": [2],
            "hard": [3]
        },
        "t2": {
            "easy": [2],
            "medium": [4],
            "hard": [6]
        }
    },
    "templates": [
        "Find the difference between the amounts after {t1} years and {t2} years on {p} at {r}% SI.",
        "What is the difference in amount for an investment of {p} at {r}% SI after {t1} and {t2} years?",
        "Calculate the increase in amount from {t1} years to {t2} years at {r}% SI on {p}."
    ]
}
}
