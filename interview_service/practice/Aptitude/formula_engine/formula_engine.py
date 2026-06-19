import math
from collections import Counter


def solve(topic, params):
    if topic == "Time & Distance":
        speed = params["speed"]
        distance = params["distance"]
        return round(distance / speed, 2)
    
    raise ValueError("Unsupported topic")

def time_from_speed_distance(speed, distance):
    return round(distance / speed, 2)


def avg_speed_round_trip(v1, v2):
    return round((2 * v1 * v2) / (v1 + v2), 2)


def cost_price_from_sp_profit(sp, profit):
    return round(sp / (1 + profit / 100), 2)


def relative_speed_opposite(v1, v2, distance):
    return round(distance / (v1 + v2), 2)


def relative_speed_same(v1, v2, distance):
    return round(distance / (v1 - v2), 2)


def train_cross_platform(train_length, platform_length, speed):
    speed_mps = speed * (5 / 18)
    return round((train_length + platform_length) / speed_mps, 2)


def train_cross_pole(train_length, speed):
    speed_mps = speed * (5 / 18)
    return round(train_length / speed_mps, 2)


def boat_downstream_time(boat_speed, stream_speed, distance):
    return round(distance / (boat_speed + stream_speed), 2)


def calculate_si_amount(principal, rate, time):
    # SI = (P * R * T) / 100
    return round((float(principal) * float(rate) * float(time)) / 100, 2)

def work_together_time(days_a, days_b):
    # Formula: (A * B) / (A + B)
    a = float(days_a)
    b = float(days_b)
    return round((a * b) / (a + b), 2)

def original_from_final_percent(final_value, percent_change):
    # Original = (Final * 100) / (100 + Percent)
    f = float(final_value)
    p = float(percent_change)
    return round((f * 100) / (100 + p), 2)


def calculate_current_age(ratio_a, ratio_b, years_hence, future_ratio_a, future_ratio_b):
    # Logic: (ax + k) / (bx + k) = c / d
    # Solve for x: x = k(c - d) / (ad - bc)
    k = float(years_hence)
    a, b = float(ratio_a), float(ratio_b)
    c, d = float(future_ratio_a), float(future_ratio_b)
    
    x = (k * (c - d)) / (a * d - b * c)
    return round(abs(a * x), 0)

def calculate_partner_profit(inv_a, inv_b, total_profit):
    # Profit A = [Inv_A / (Inv_A + Inv_B)] * Total_Profit
    a = float(inv_a)
    b = float(inv_b)
    tp = float(total_profit)
    return round((a / (a + b)) * tp, 2)

def calculate_ci_2yr(principal, rate):
    # CI = P * [(1 + R/100)^2 - 1]
    p = float(principal)
    r = float(rate)
    amount = p * ((1 + r/100)**2)
    ci = amount - p
    return round(ci, 2)


def original_from_final_decrease(final_value, percent_change):
    """
    Reverse percentage (decrease)
    """
    return round(final_value * 100 / (100 - percent_change), 2)


def successive_percent_change(percent_1, percent_2):
    """
    Net change after two successive changes
    """
    net = percent_1 + percent_2 + (percent_1 * percent_2) / 100
    return round(net, 2)


def percentage_difference(value_a, value_b):
    """
    Percentage difference relative to value_b
    """
    return round(((value_b - value_a) / value_b) * 100, 2)


def net_percent_change(increase, decrease):
    """
    Net effect of increase followed by decrease
    """
    net = increase - decrease - (increase * decrease) / 100
    return round(net, 2)
def di_table_sum(A, B, C, D):
    return A + B + C + D

def di_table_sum(values):
    return sum(values)

def di_table_average(values):
    return round(sum(values) / len(values), 2)

def di_bar_max_min(values):
    return max(values) - min(values)

def di_percent_change(old, new):
    return round(((new - old) / old) * 100, 2)

def di_line_trend_difference(start, end):
    return end - start

def di_line_average(values):
    return round(sum(values) / len(values), 2)

def di_pie_percentage(part, total):
    return round((part / total) * 100, 2)

def di_pie_angle(part, total):
    return round((part / total) * 360, 2)

def di_avg_interest(data):
    return round(sum(data["interest"]) / len(data["interest"]), 2)


def di_bonus_percent_salary(data):
    return round((sum(data["bonus"]) / sum(data["salary"])) * 100, 2)


def di_year_ratio(data, year1, year2):
    i1 = data["years"].index(year1)
    i2 = data["years"].index(year2)

    total1 = data["salary"][i1] + data["bonus"][i1] + data["interest"][i1]
    total2 = data["salary"][i2] + data["bonus"][i2] + data["interest"][i2]

    return round((total1 / total2) * 100, 2)


def di_max_expenditure_year(data):
    totals = [
        data["salary"][i] + data["bonus"][i] + data["interest"][i]
        for i in range(len(data["years"]))
    ]
    return data["years"][totals.index(max(totals))]


# -------- BAR / PIE HELPERS --------

def di_max_sales(data):
    return max(data, key=data.get)


def di_percent_increase(data, year1, year2):
    return round(((data[year2] - data[year1]) / data[year1]) * 100, 2)


def di_max_population_sector(data):
    return max(data, key=data.get)


def di_population_percent(data, sector):
    return round((data[sector] / sum(data.values())) * 100, 2)

def di_sector_angle(dataset, sector):
    """
    Calculates the angle of a given sector in a pie chart.
    
    dataset example:
    {
        "sectors": {
            "Agriculture": 30,
            "Industry": 45,
            "Services": 75
        }
    }
    """
    sectors = dataset["sectors"]

    if sector not in sectors:
        raise ValueError(f"Sector '{sector}' not found in dataset")

    total = sum(sectors.values())
    value = sectors[sector]

    angle = (value / total) * 360
    return round(angle, 2)
def stat_mean(values=None, **kwargs):
    """
    Concept: Arithmetic Mean.
    Formula: Sum of observations / Number of observations
    """
    if not isinstance(values, list) or not values:
        return 0
    
    total_sum = sum(float(v) for v in values)
    count = len(values)
    
    result = total_sum / count
    # Return as int if whole number, otherwise round to 2 decimals
    if result.is_integer():
        return int(result)
    return round(result, 2)


def stat_median(values=None, **kwargs):
    """
    Concept: Statistical Median.
    Logic: 
    1. Sort the list.
    2. If n is odd, median is the middle element.
    3. If n is even, median is the average of the two middle elements.
    """
    if not isinstance(values, list) or not values:
        return 0
    
    # Step 1: Sort the data
    sorted_data = sorted([float(v) for v in values])
    n = len(sorted_data)
    mid = n // 2
    
    # Step 2: Check if even or odd
    if n % 2 == 0:
        # Even: Average of the two middle values
        result = (sorted_data[mid - 1] + sorted_data[mid]) / 2
    else:
        # Odd: The middle value
        result = sorted_data[mid]
    
    # Clean output formatting
    if result.is_integer():
        return int(result)
    return round(result, 2)


from collections import Counter

def stat_mode(values=None, **kwargs):
    """
    Concept: Statistical Mode.
    Logic: Find the value with the highest frequency in the list.
    """
    if not isinstance(values, list) or not values:
        return 0
    
    # Count the frequency of each element
    counts = Counter(values)
    
    # Find the maximum frequency
    max_freq = max(counts.values())
    
    # Extract values that have the maximum frequency
    modes = [val for val, freq in counts.items() if freq == max_freq]
    
    # For basic practice, we usually return the first mode found 
    # if it exists, or handle cases with no mode.
    if max_freq == 1 and len(values) > 1:
        return "No Mode"
    
    result = modes[0]
    
    # Clean output formatting
    if isinstance(result, (int, float)) and float(result).is_integer():
        return int(result)
    return result


def stat_range(values=None, **kwargs):
    """
    Concept: Statistical Range.
    Formula: Max(values) - Min(values)
    """
    if not isinstance(values, list) or not values:
        return 0
    
    # Identify the extreme values
    maximum = max(values)
    minimum = min(values)
    
    result = maximum - minimum
    
    # Clean output: return int if whole number, else rounded float
    if isinstance(result, (int, float)) and float(result).is_integer():
        return int(result)
    return round(result, 2)


import math

def stat_variance(values=None, **kwargs):
    """
    Concept: Population Variance (σ²).
    Logic: Average of squared differences from the Mean.
    """
    if not values: return 0
    n = len(values)
    mean = sum(values) / n
    
    # Calculate sum of squared differences
    variance = sum((x - mean) ** 2 for x in values) / n
    
    if variance.is_integer():
        return int(variance)
    return round(variance, 2)

def stat_std_dev(values=None, **kwargs):
    """
    Concept: Standard Deviation (σ).
    Logic: Square root of Variance.
    """
    variance = stat_variance(values=values, **kwargs)
    std_dev = math.sqrt(variance)
    
    if std_dev.is_integer():
        return int(std_dev)
    return round(std_dev, 2)


def stat_probability(favorable, total):
    """
    Concept: Basic Theoretical Probability.
    Formula: P(E) = n(E) / n(S)
    """
    fav = float(favorable)
    tot = float(total)
    
    if tot == 0:
        return 0
        
    if fav > tot:
        return 1.0 # Probability cannot exceed 1
        
    prob = fav / tot
    
    # Return as int if 0 or 1, else round to 3 decimals
    if prob.is_integer():
        return int(prob)
    return round(prob, 3)

def stat_correlation_type(correlation_value):
    """
    Concept: Interpretation of Pearson's r.
    Logic: 
    1. Check sign for Direction (Positive/Negative).
    2. Check magnitude for Strength (Perfect/Strong/Moderate/Weak/None).
    """
    r = float(correlation_value)
    
    # Direction
    direction = "Positive" if r > 0 else "Negative"
    if r == 0: return "No Correlation"
    
    abs_r = abs(r)
    
    # Strength
    if abs_r == 1.0:
        strength = "Perfect"
    elif abs_r >= 0.7:
        strength = "Strong"
    elif abs_r >= 0.4:
        strength = "Moderate"
    elif abs_r > 0.1:
        strength = "Weak"
    else:
        return "Negligible or No Correlation"
        
    return f"{strength} {direction} Correlation"

def stat_sampling_type(method):
    """
    Concept: Identifying Sampling Methodologies.
    Logic: Returns the key characteristic of the method.
    """
    m = method.lower()
    
    mapping = {
        "simple random": "Every individual has an equal chance of selection (e.g., drawing names from a hat).",
        "stratified": "Population is divided into groups (strata), and samples are taken from each group.",
        "cluster": "Population is divided into clusters; entire clusters are randomly selected.",
        "systematic": "Selection follows a fixed interval (e.g., every nth person on a list).",
        "convenience": "Samples are chosen based on ease of access rather than randomness.",
        "voluntary response": "Participants choose themselves to be part of the study."
    }
    
    return mapping.get(m, "Unknown sampling technique.")


def stat_cv(mean, std_dev):
    """
    Coefficient of Variation = (Std Dev / Mean) * 100
    """
    m, s = float(mean), float(std_dev)
    if m == 0: return 0
    return round((s / m) * 100, 2)

def stat_z_score(x, mean, std_dev):
    """
    Z-Score = (X - Mean) / Std Dev
    """
    val, m, s = float(x), float(mean), float(std_dev)
    if s == 0: return 0
    return round((val - m) / s, 2)

def stat_iqr(q1, q3):
    """
    Interquartile Range = Q3 - Q1
    """
    return round(float(q3) - float(q1), 2)

import math
import string

def lr_arithmetic_series_next(a, d):
    return a + 4 * d

def lr_geometric_series_next(a, r):
    return a * (r ** 4)

def lr_coding_shift(word, shift):
    result = ""
    for ch in word:
        result += chr(((ord(ch) - 65 + shift) % 26) + 65)
    return result

def lr_blood_relation(relation):
    mapping = {
        "father": "son/daughter",
        "brother": "brother/sister",
        "uncle": "nephew/niece"
    }
    return mapping[relation]

def lr_direction_distance(x, y):
    return round(math.sqrt(x**2 + y**2), 2)

def lr_order_ranking(total, rank_from_top):
    return total - rank_from_top + 1


def lr_blood_relation_inverse(relation):
    inverse = {
        "father": "son/daughter",
        "mother": "son/daughter",
        "son": "father/mother",
        "daughter": "father/mother",
        "brother": "brother/sister",
        "sister": "brother/sister",
        "uncle": "nephew/niece",
        "aunt": "nephew/niece"
    }
    return inverse[relation]


def lr_blood_relation_two_step(r1, r2):
    table = {
        ("father", "son"): "grandfather",
        ("father", "daughter"): "grandfather",
        ("mother", "son"): "grandmother",
        ("brother", "son"): "uncle",
        ("brother", "daughter"): "uncle",
        ("sister", "son"): "aunt",
        ("sister", "daughter"): "aunt"
    }
    return table.get((r1, r2), "relative")


def lr_blood_relation_gender(relation, gender):
    table = {
        ("parent", "male"): "father",
        ("parent", "female"): "mother",
        ("sibling", "male"): "brother",
        ("sibling", "female"): "sister",
        ("child", "male"): "son",
        ("child", "female"): "daughter"
    }
    return table[(relation, gender)]


def lr_blood_relation_generation(relation):
    generations = {
        "father": "one generation",
        "mother": "one generation",
        "grandfather": "two generations",
        "grandmother": "two generations",
        "great grandfather": "three generations",
        "great grandmother": "three generations"
    }

    # 🚫 Collateral relations have no generation gap
    if relation not in generations:
        return "same generation"

    return generations[relation]

def lr_blood_relation_chain(r1, r2, r3):
    chain_map = {
        ("father", "son", "son"): "great grandfather",
        ("father", "son", "daughter"): "great grandfather",
        ("brother", "son", "son"): "grand uncle",
        ("brother", "daughter", "son"): "grand uncle",
        ("uncle", "son", "son"): "great uncle"
    }
    return chain_map.get((r1, r2, r3), "relative")
def lr_blood_relation_age(relation, age_diff):
    # Age doesn't change relation, only validates it
    valid = {
        "father": "father",
        "uncle": "uncle",
        "grandfather": "grandfather"
    }
    return valid.get(relation, "relative")

def lr_blood_relation_direction(relation, direction):
    # Direction is distraction; relation remains same
    return relation

def lr_blood_relation_gender_confusion(statement):
    mapping = {
        "A is parent of B": "father/mother",
        "A is sibling of B": "brother/sister",
        "A is elder cousin of B": "cousin"
    }
    return mapping.get(statement, "relative")


def lr_order_ranking(total: int, rank_from_top: int) -> int:
    """
    Rank from bottom = total - rank_from_top + 1
    """
    if rank_from_top > total:
        raise ValueError("Rank from top cannot exceed total students")

    return total - rank_from_top + 1


def lr_ranking_interchange(
    p1_old_left: int,
    p2_old_right: int,
    p1_new_left: int
) -> int:


    total = p1_new_left + p2_old_right - 1

    if total <= 0:
        raise ValueError("Invalid ranking configuration")

    return total


def lr_ranking_shifting(
    total: int,
    shift_count: int,
    new_pos_left: int
) -> int:

    original_left = new_pos_left + shift_count

    if original_left > total:
        raise ValueError("Invalid shift leading outside row")

    original_from_right = total - original_left + 1
    return original_from_right


def lr_ranking_total_count(pos_left: int, pos_right: int) -> int:
    """
    Total = pos_left + pos_right - 1
    """

    if pos_left <= 0 or pos_right <= 0:
        raise ValueError("Positions must be positive")

    return pos_left + pos_right - 1


def lr_ranking_min_total(pos_left, pos_right, between):
    """
    Formula for Minimum Total (Overlapping):
    Min Total = (Sum of positions from ends) - (Persons in middle) - 2
    """
    return (pos_left + pos_right) - between - 2


def lr_ranking_middle_count(total, pos_left, pos_right):
    # Case 1: Simple (Non-overlapping)
    # If (pos_left + pos_right) < total
    if (pos_left + pos_right) < total:
        return total - (pos_left + pos_right)
    
    # Case 2: Overlapping (The "Hard" case)
    # If (pos_left + pos_right) > total
    else:
        return (pos_left + pos_right) - total - 2
    

def lr_order_ranking_reverse(total: int, rank_from_bottom: int) -> int:
    """
    Rank from top = total - rank_from_bottom + 1
    """
    if rank_from_bottom > total:
        raise ValueError("Invalid rank from bottom")

    return total - rank_from_bottom + 1



def lr_ranking_same_side_diff(pos1: int, pos2: int) -> int:
    """
    Difference between two ranks from same side
    Students between = |pos2 - pos1| - 1
    """
    return abs(pos2 - pos1) - 1



def lr_ranking_opposite_side_diff(
    total: int,
    pos_left: int,
    pos_right: int
) -> int:
    """
    Students between when positions are from opposite sides:
    between = total - (pos_left + pos_right)
    """
    between = total - (pos_left + pos_right)
    return max(between, 0)


def lr_ranking_consecutive(rank1: int, rank2: int) -> str:
    """
    Checks if two ranks are consecutive
    """
    return "Yes" if abs(rank1 - rank2) == 1 else "No"


def lr_ranking_change(old_rank: int, new_rank: int) -> int:
    """
    Number of positions changed
    """
    return abs(old_rank - new_rank)



def lr_ranking_removal(rank: int, removed: int) -> int:
    """
    New rank after removing students above
    """
    new_rank = rank - removed
    return max(new_rank, 1)


def lr_ranking_addition(rank: int, added: int) -> int:
    """
    New rank after adding students above
    """
    return rank + added


def lr_ranking_middle_position(total: int) -> int:
    """
    Rank of middle student (total assumed odd)
    """
    if total % 2 == 0:
        raise ValueError("Total must be odd to have a single middle position")

    return (total // 2) + 1


def lr_ranking_max_total(pos_left: int, pos_right: int, between: int) -> int:
    """
    Finds the maximum possible total number of people in a row.

    Logic:
    Maximum total = pos_left + pos_right + between
    """

    if pos_left <= 0 or pos_right <= 0 or between < 0:
        raise ValueError("Invalid ranking values")

    return pos_left + pos_right + between
# practice/Aptitude/formula_engine/AR_formula_engine.py

def compound_interest(principal, rate, time, **kwargs):
    amount = principal * ((1 + rate / 100) ** time)
    return round(amount - principal, 2)


def compound_amount(principal, rate, time, **kwargs):
    return round(principal * ((1 + rate / 100) ** time), 2)


def ci_si_difference(principal, rate, time, **kwargs):
    si = (principal * rate * time) / 100
    ci = compound_interest(principal, rate, time)
    return round(ci - si, 2)


def compound_interest_half_yearly(principal, rate, time, **kwargs):
    r = rate / 200
    n = time * 2
    amount = principal * ((1 + r) ** n)
    return round(amount - principal, 2)

def simple_interest(p: float, r: float, t: float) -> float:
    """
    SI = (P * R * T) / 100
    """
    return (p * r * t) / 100

def amount_simple_interest(p: float, r: float, t: float) -> float:
    """
    Amount = P + SI
    """
    si = simple_interest(p, r, t)
    return p + si
def principal_from_si(si: float, r: float, t: float) -> float:
    """
    P = (SI * 100) / (R * T)
    """
    return (si * 100) / (r * t)


def rate_from_si(p: float, si: float, t: float) -> float:
    """
    R = (SI * 100) / (P * T)
    """
    return (si * 100) / (p * t)


def time_from_si(p: float, si: float, r: float) -> float:
    """
    T = (SI * 100) / (P * R)
    """
    return (si * 100) / (p * r)

def amount_difference_si(p: float, r: float, t1: float, t2: float) -> float:
    """
    Difference in amount between t1 and t2 years
    ΔA = P * R * (t2 - t1) / 100
    """
    return (p * r * (t2 - t1)) / 100
# =====================================================
# TIME, SPEED & DISTANCE (TSD)
# =====================================================

def speed_from_dt(d: float, t: float) -> float:
    """
    Speed = Distance / Time
    """
    return d / t


def distance_from_st(s: float, t: float) -> float:
    """
    Distance = Speed × Time
    """
    return s * t


def time_from_ds(d: float, s: float) -> float:
    """
    Time = Distance / Speed
    """
    return d / s


def average_speed_equal(s1: float, s2: float) -> float:
    """
    Average speed when equal distances are covered
    = 2*s1*s2 / (s1 + s2)
    """
    return (2 * s1 * s2) / (s1 + s2)


def relative_speed(s1: float, s2: float, direction: str = "opposite") -> float:
    """
    Relative speed:
    - opposite direction: s1 + s2
    - same direction: |s1 - s2|
    """
    if direction == "same":
        return abs(s1 - s2)
    return s1 + s2


def train_crossing_time(l: float, s: float) -> float:
    """
    Time = Length / Speed
    Speed converted from km/h to m/s
    """
    speed_mps = (s * 1000) / 3600
    return l / speed_mps


def boat_stream_speed(u: float, v: float, direction: str = "downstream") -> float:
    """
    Boat & stream:
    downstream = u + v
    upstream = u - v
    """
    if direction == "upstream":
        return u - v
    return u + v


# =====================================================
# TIME & WORK (TW)
# =====================================================

def work_together(a: float, b: float) -> float:
    """
    Work done together:
    1/T = 1/a + 1/b
    """
    return 1 / ((1 / a) + (1 / b))


def efficiency_work(a: float, b: float = None) -> float:
    """
    Efficiency-based:
    If A is twice as efficient as B
    and B takes b days, A takes b/2 days
    """
    if b is not None:
        return b / 2
    return a


def work_wages(a: float, b: float, w: float) -> float:
    """
    Work & Wages:
    Wages proportional to days worked
    """
    total_days = a + b
    return (a / total_days) * w


def pipes_fill_time(f: float, e: float) -> float:
    """
    Pipes & cisterns:
    Net work rate = (1/f - 1/e)
    """
    rate = (1 / f) - (1 / e)
    if rate <= 0:
        raise ValueError("Tank will never fill")
    return 1 / rate


def stat_weighted_mean(values, weights):
    """
    Weighted Mean
    """
    if len(values) != len(weights):
        raise ValueError("Values and weights must be of same length")
    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("Total weight cannot be zero")
    return sum(v * w for v, w in zip(values, weights)) / total_weight

def stat_median(values):
    """
    Median
    """
    if not values:
        raise ValueError("Values list cannot be empty")
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2

    if n % 2 == 0:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
    return sorted_vals[mid]


def stat_mode(values):
    """
    Mode (single mode guaranteed by param_rules)
    """
    if not values:
        raise ValueError("Values list cannot be empty")
    freq = Counter(values)
    return freq.most_common(1)[0][0]

def stat_variance(values):
    """
    Variance (population variance)
    """
    if not values:
        raise ValueError("Values list cannot be empty")
    mean = stat_mean(values)
    return sum((x - mean) ** 2 for x in values) / len(values)


def stat_std_dev(values):
    """
    Standard Deviation
    """
    return math.sqrt(stat_variance(values))

def stat_probability(favorable, total):
    """
    Basic Probability = favorable / total
    """
    if total <= 0:
        raise ValueError("Total outcomes must be positive")
    if favorable < 0 or favorable > total:
        raise ValueError("Invalid favorable outcomes")
    return favorable / total

FORMULA_REGISTRY = {  
    "stat_mean": stat_mean,
    "stat_weighted_mean": stat_weighted_mean,
    "stat_median": stat_median,
    "stat_mode": stat_mode,
    "stat_variance": stat_variance,
    "stat_std_dev": stat_std_dev,
    "stat_probability": stat_probability,
    "speed_from_dt": speed_from_dt,
    "distance_from_st": distance_from_st,
    "time_from_ds": time_from_ds,
    "average_speed_equal": average_speed_equal,
    "relative_speed": relative_speed,
    "train_crossing_time": train_crossing_time,
    "boat_stream_speed": boat_stream_speed,
    "work_together": work_together,
    "efficiency_work": efficiency_work,
    "work_wages": work_wages,
    "pipes_fill_time": pipes_fill_time,
    "simple_interest":simple_interest,
    "amount_simple_interest":amount_simple_interest,
    "principal_from_si":principal_from_si,
    "rate_from_si":rate_from_si,
    "time_from_si": time_from_si,
    "amount_difference_si":amount_difference_si,
    "compound_interest":compound_interest,
    "compound_amount":compound_amount,
    "ci_si_difference":ci_si_difference,
    "compound_interest_half_yearly":compound_interest_half_yearly,
    "original_from_final_percent": original_from_final_percent,
    "successive_percentage_change": successive_percent_change,
    "avg_speed_round_trip": avg_speed_round_trip,
    "time_from_speed_distance": time_from_speed_distance,
    "cost_price_from_sp_profit": cost_price_from_sp_profit,
    "relative_speed_opposite": relative_speed_opposite,
    "relative_speed_same": relative_speed_same,
    "train_cross_platform": train_cross_platform,
    "train_cross_pole": train_cross_pole,
    "boat_downstream_time": boat_downstream_time,
    "calculate_si_amount": calculate_si_amount,
    "work_together_time": work_together_time,
    "original_from_final_decrease": original_from_final_decrease,
    "successive_percent_change": successive_percent_change,
    "percentage_difference": percentage_difference,
    "net_percent_change": net_percent_change,
    "lr_ranking_min_total": lr_ranking_min_total,
    "lr_order_ranking": lr_order_ranking,
    "lr_ranking_interchange": lr_ranking_interchange,
    "lr_ranking_shifting": lr_ranking_shifting,
    "lr_ranking_total_count": lr_ranking_total_count,
    "lr_ranking_middle_count": lr_ranking_middle_count,
    "lr_order_ranking_reverse": lr_order_ranking_reverse,
    "lr_ranking_same_side_diff": lr_ranking_same_side_diff,
    "lr_ranking_opposite_side_diff": lr_ranking_opposite_side_diff,
    "lr_blood_relation_inverse": lr_blood_relation_inverse,
    "lr_blood_relation_two_step": lr_blood_relation_two_step,
    "lr_ranking_consecutive": lr_ranking_consecutive,
    "lr_ranking_change": lr_ranking_change,
    "lr_ranking_removal": lr_ranking_removal,
    "lr_ranking_addition": lr_ranking_addition,
    "lr_ranking_middle_position": lr_ranking_middle_position,
    "lr_ranking_max_total": lr_ranking_max_total,   
    "calculate_current_age":calculate_current_age,
    "calculate_partner_profit":calculate_partner_profit,
    "calculate_ci_2yr":calculate_ci_2yr,
    "di_table_sum":di_table_sum,
    "di_table_average":di_table_average,
    "di_avg_interest": di_avg_interest,
    "di_bar_max_min":di_bar_max_min,
    "stat_median": stat_median,
    "stat_mode": stat_mode,
    "stat_range": stat_range,
    "stat_variance": stat_variance,
    "stat_std_dev": stat_std_dev,
    "stat_probability": stat_probability,
    "stat_correlation_type": stat_correlation_type,
    "stat_sampling_type": stat_sampling_type,
    "stat_cv": stat_cv,
    "stat_z_score": stat_z_score,
    "stat_iqr": stat_iqr,
}
