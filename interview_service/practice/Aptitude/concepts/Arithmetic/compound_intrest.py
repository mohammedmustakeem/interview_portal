# practice/Aptitude/Arithmetic/compound_interest.py

AR_COMPOUND_INTEREST_CONCEPTS = {

    "CI_BASIC": {
        "topic": "Arithmetic",
        "sub_topic": "Compound Interest",
        "concept": "Compound Interest (Basic)",
        "formula": "compound_interest",
        "unit": "currency",
        "params": {
            "principal": ["principal"],
            "rate": ["rate"],
            "time": ["time"]
        },
        "param_rules": {
            "principal": {
                "easy": [1000, 2000, 5000],
                "medium": [12500, 16000, 25000, 31250, 40000], # Values requiring fractional logic
                "hard": [64000, 128000, 256000]
            },
            "rate": {
                "easy": [5, 10],
                "medium": [4, 8, 12, 15], # Intermediate rates
                "hard": [12.5, 16.66, 18]
            },
            "time": {
                "easy": [2],
                "medium": [3], # Cubing required
                "hard": [4, 5]
            }
        },
        "templates": [
            "Find the compound interest on {principal} at {rate}% per annum for {time} years.",
            "What is the compound interest on {principal} invested at {rate}% for {time} years?",
            "Calculate the CI for a sum of {principal} at {rate}% after {time} years.",
            "A man invests {principal} in a bank at {rate}% p.a. compound interest. How much interest will he earn in {time} years?",
            "Find the CI earned on a deposit of {principal} if the rate of interest is {rate}% and the duration is {time} years.",
            "Determine the total compound interest payable on a loan of {principal} at {rate}% per annum after {time} years."
        ]
    },

    "CI_AMOUNT": {
        "topic": "Arithmetic",
        "sub_topic": "Compound Interest",
        "concept": "Amount after Compound Interest",
        "formula": "compound_amount",
        "unit": "currency",
        "params": {
            "principal": ["principal"],
            "rate": ["rate"],
            "time": ["time"]
        },
        "param_rules": {
            "principal": {
                "easy": [1000, 3000],
                "medium": [15625, 20000, 45000, 62500],
                "hard": [75000, 150000]
            },
            "rate": {
                "easy": [5, 10],
                "medium": [5, 8, 12],
                "hard": [15, 20]
            },
            "time": {
                "easy": [2],
                "medium": [3, 4],
                "hard": [5, 6]
            }
        },
        "templates": [
            "Find the amount after {time} years if {principal} is invested at {rate}% compounded annually.",
            "What will be the final amount on {principal} at {rate}% after {time} years?",
            "Calculate the total amount after compounding {principal} for {time} years at {rate}%.",
            "What sum will {principal} amount to in {time} years at {rate}% per annum compound interest?",
            "Find the maturity value of a fixed deposit of {principal} for {time} years at {rate}% compounded yearly.",
            "A person saves {principal} in a scheme that offers {rate}% CI annually. What is the total sum accumulated after {time} years?"
        ]
    },

    "CI_SI_DIFFERENCE": {
        "topic": "Arithmetic",
        "sub_topic": "Compound Interest",
        "concept": "Difference between CI and SI",
        "formula": "ci_si_difference",
        "unit": "currency",
        "params": {
            "principal": ["principal"],
            "rate": ["rate"],
            "time": ["time"]
        },
        "param_rules": {
            "principal": {
                "easy": [1000, 2000],
                "medium": [8000, 12000, 15000, 24000],
                "hard": [25000, 50000]
            },
            "rate": {
                "easy": [5, 10],
                "medium": [6, 12, 15],
                "hard": [8.5, 14]
            },
            "time": {
                "easy": [2],
                "medium": [2, 3],
                "hard": [3]
            }
        },
        "templates": [
            "Find the difference between compound interest and simple interest on {principal} at {rate}% for {time} years.",
            "What is the difference between CI and SI on {principal} for {time} years at {rate}%?",
            "Calculate CI − SI for a sum of {principal} at {rate}% after {time} years.",
            "On a sum of {principal}, the difference between CI and SI for {time} years at {rate}% is what amount?",
            "The CI on {principal} for {time} years at {rate}% is how much more than the SI for the same period and rate?",
            "Find the gap between the interest earned through compounding and simple interest on {principal} at {rate}% p.a. for {time} years."
        ]
    },

   
    "CI_HALF_YEARLY": {
        "topic": "Arithmetic",
        "sub_topic": "Compound Interest",
        "concept": "Compound Interest (Half-Yearly)",
        "formula": "compound_interest_half_yearly",
        "unit": "currency",
        "params": {
            "principal": ["principal"],
            "rate": ["rate"],
            "time": ["time"]
        },
        "param_rules": {
            "principal": {
                "easy": [2000, 4000],
                "medium": [16000, 25000, 32000, 50000],
                "hard": [64000, 125000]
            },
            "rate": {
                "easy": [10, 20], # Becomes 5% and 10%
                "medium": [8, 12, 16], # Becomes 4%, 6%, 8%
                "hard": [15, 18]
            },
            "time": {
                "easy": [1], # 2 conversion periods
                "medium": [1.5, 2], # 3 or 4 conversion periods
                "hard": [2.5, 3]
            }
        },
        "templates": [
            "Find the compound interest on {principal} at {rate}% per annum compounded half-yearly for {time} years.",
            "Calculate CI if {principal} is invested at {rate}% half-yearly for {time} years.",
            "What is the compound interest on {principal} compounded half-yearly at {rate}% for {time} years?",
            "Find the CI on {principal} for {time} years at {rate}% p.a., interest being compounded semi-annually.",
            "How much interest will be credited to an account with {principal} at {rate}% compounded every six months for {time} years?",
            "Determine the compound interest earned on {principal} at {rate}% per annum for {time} years, if compounding is done half-yearly."
        ]
    }
}
