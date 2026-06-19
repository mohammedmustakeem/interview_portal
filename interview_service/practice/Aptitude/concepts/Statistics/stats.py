# statistics.py
# Math Aptitude → Statistics (Intermediate & Advanced)

STATISTICS_CONCEPTS = {
    "STAT_MEAN": {
        "topic": "Math Aptitude",
        "sub_topic": "Statistics",
        "concept": "Arithmetic Mean",
        "formula": "stat_mean",
        "unit": "number",
        "params": {
            "values": ["numbers"]
        },
        "param_rules": {
            "values": {
                "easy": [[10, 20, 30], [5, 15, 25], [12, 14, 16], [50, 100, 150]],
                "medium": [[12, 18, 24, 30, 36], [20, 25, 30, 35, 40], [105, 110, 115, 120]],
                "hard": [[8.5, 16.2, 24.3, 32.1], [1450, 2300, 1850, 3100], [0.5, 1.2, 0.8, 2.4, 1.1]]
            }
        },
        "templates": [
            "Find the arithmetic mean of the numbers {values}.",
            "What is the average of the following data set: {values}?",
            "Calculate the mean of the numbers: {values}.",
            "In a survey, the results recorded were {values}. Determine the average value.",
            "A student's scores in {len_values} subjects are {values}. Find the mean score.",
            "The daily rainfall in a city for a week was recorded as {values} mm. Calculate the mean rainfall.",
            "The weights of {len_values} boxes are {values} kg. What is the mean weight of a box?"
        ]
    },

    "STAT_WEIGHTED_MEAN": {
        "topic": "Math Aptitude",
        "sub_topic": "Statistics",
        "concept": "Weighted Average",
        "formula": "stat_weighted_mean",
        "unit": "number",
        "params": {
            "values": ["values"],
            "weights": ["weights"]
        },
        "param_rules": {
            "values": {
                "easy": [[10, 20], [30, 40], [50, 100]],
                "medium": [[15, 25, 35], [20, 30, 40], [70, 80, 90]],
                "hard": [[12.5, 14.2, 18.8], [92, 85, 88, 95], [1500, 1600, 1700, 1800]]
            },
            "weights": {
                "easy": [[1, 1], [2, 1], [1, 3]],
                "medium": [[1, 2, 3], [2, 3, 5], [1, 1, 2]],
                "hard": [[0.2, 0.5, 0.3], [1, 2, 3, 4], [10, 20, 30, 40]]
            }
        },
        "templates": [
            "Find the weighted mean of values {values} with weights {weights}.",
            "Calculate the weighted average for the scores {values} with corresponding weights {weights}.",
            "What is the weighted mean of the observations {values} if their frequencies are {weights}?",
            "A student's grades are {values} with credit hours {weights}. Find the Weighted GPA.",
            "An investor bought shares at prices {values} in quantities {weights}. Find the weighted average price.",
            "In a product mix, the costs are {values} and proportions are {weights}. Calculate the weighted cost.",
            "Determine the effective average of {values} adjusted by the significance factors {weights}."
        ]
    },


    "STAT_MEDIAN": {
        "topic": "Math Aptitude",
        "sub_topic": "Statistics",
        "concept": "Median",
        "formula": "stat_median",
        "unit": "number",
        "params": {
            "values": ["numbers"]
        },
        "param_rules": {
            "values": {
                "easy": [[3, 5, 7], [2, 4, 6, 8], [11, 15, 19]],
                "medium": [[10, 15, 20, 25, 30], [5, 10, 15, 20, 25, 30], [102, 105, 108, 111]],
                "hard": [[7, 14, 21, 28, 35, 42], [12.5, 18.2, 24.6, 30.1, 36.4], [145, 167, 189, 210]]
            }
        },
        "templates": [
            "Find the median of the data set {values}.",
            "What is the median of the following numbers: {values}?",
            "Calculate the median for the sorted data: {values}.",
            "The heights of {len_values} students are {values} cm. Find the median height.",
            "Identify the middle value (median) for the observations: {values}.",
            "In a marathon, the finishing times in minutes were {values}. Find the median time.",
            "A company recorded its daily sales as {values}. Determine the median sales amount."
        ]
    },

    "STAT_MODE": {
        "topic": "Math Aptitude",
        "sub_topic": "Statistics",
        "concept": "Mode",
        "formula": "stat_mode",
        "unit": "number",
        "params": {
            "values": ["numbers"]
        },
        "param_rules": {
            "values": {
                "easy": [[2, 3, 3, 5], [4, 4, 6, 8], [1, 1, 2, 2, 2]],
                "medium": [[10, 12, 12, 15, 18], [5, 7, 7, 7, 9, 9], [25, 25, 30, 35, 40]],
                "hard": [[20, 25, 25, 30, 30, 30], [8, 8, 12, 16, 16, 16, 20], [105, 105, 110, 115]]
            }
        },
        "templates": [
            "Find the mode of the data set {values}.",
            "Which value occurs most frequently in the following data: {values}?",
            "Determine the mode of the given numbers: {values}.",
            "In a shoe store, the sizes sold were {values}. What is the modal shoe size?",
            "A class took a quiz and scored {values}. Find the most common score (mode).",
            "Identify the mode for the following frequency distribution: {values}.",
            "The number of goals scored in {len_values} matches are {values}. Find the mode."
        ]
    },

    "STAT_VARIANCE": {
        "topic": "Math Aptitude",
        "sub_topic": "Statistics",
        "concept": "Variance",
        "formula": "stat_variance",
        "unit": "number",
        "params": {
            "values": ["numbers"]
        },
        "param_rules": {
            "values": {
                "easy": [[2, 4, 6], [3, 5, 7], [10, 20, 30]],
                "medium": [[10, 12, 14, 16], [5, 10, 15, 20], [25, 35, 45, 55]],
                "hard": [[8, 16, 24, 32], [12, 18, 24, 30], [14.2, 15.8, 16.1, 14.9]]
            }
        },
        "templates": [
            "Find the variance of the data set {values}.",
            "Calculate the variance for the given observations: {values}.",
            "Determine the variance (σ²) of the following numbers: {values}.",
            "Assess the spread of the data {values} by calculating its variance.",
            "In a scientific experiment, the recorded values were {values}. Find the variance.",
            "How much does the data set {values} vary from its mean? Find the variance.",
            "Find the average of the squared differences from the mean for {values}."
        ]
    },

    "STAT_STD_DEV": {
        "topic": "Math Aptitude",
        "sub_topic": "Statistics",
        "concept": "Standard Deviation",
        "formula": "stat_std_dev",
        "unit": "number",
        "params": {
            "values": ["numbers"]
        },
        "param_rules": {
            "values": {
                "easy": [[2, 4, 6], [3, 5, 7], [10, 20, 30]],
                "medium": [[10, 12, 14, 16], [5, 10, 15, 20], [40, 50, 60, 70]],
                "hard": [[8, 16, 24, 32], [12, 18, 24, 30], [100, 150, 200, 250]]
            }
        },
        "templates": [
            "Find the standard deviation of the data set {values}.",
            "Calculate the standard deviation for the given data: {values}.",
            "Determine the standard deviation (σ) of the following numbers: {values}.",
            "In a quality control check, the weights were {values}. Find the standard deviation.",
            "What is the standard deviation for the test scores {values}?",
            "Find the square root of the variance for the set: {values}.",
            "Analyze the volatility of the stock prices {values} by finding the standard deviation."
        ]
    },

    "STAT_PROBABILITY_BASIC": {
        "topic": "Math Aptitude",
        "sub_topic": "Statistics",
        "concept": "Basic Probability",
        "formula": "stat_probability",
        "unit": "fraction",
        "params": {
            "favorable": ["favorable"],
            "total": ["total"]
        },
        "param_rules": {
            "favorable": {
                "easy": [1, 2, 3],
                "medium": [5, 7, 10],
                "hard": [13, 17, 25]
            },
            "total": {
                "easy": [4, 6, 10],
                "medium": [20, 25, 50],
                "hard": [52, 100, 200]
            }
        },
        "templates": [
            "Find the probability of a favorable outcome when there are {favorable} favorable cases out of {total} total cases.",
            "What is the probability of success if {favorable} outcomes are favorable out of {total}?",
            "In a bag of {total} marbles, {favorable} are red. Find the probability of picking a red marble.",
            "A card is drawn from a deck of {total} cards. If {favorable} cards are Aces, find the probability of drawing an Ace.",
            "Out of {total} students, {favorable} passed. What is the probability that a randomly chosen student passed?",
            "If a die has {total} sides and {favorable} sides are marked with a star, find the probability of rolling a star.",
            "Calculate the probability of an event where the favorable outcomes are {favorable} and the sample space is {total}."
        ]
    }
}
