AR_TSD_TW_CONCEPTS = {

"TSD_SPEED": {
    "topic": "Arithmetic",
    "sub_topic": "Time Speed Distance & Work",
    "concept": "Speed from Distance and Time",
    "formula": "speed_from_dt",
    "unit": "kmph",
    "params": {"d": ["distance"], "t": ["time"]},
    "param_rules": {
        "d": {"easy": [60,120], "medium": [180,240], "hard": [360,480]},
        "t": {"easy": [1,2], "medium": [2.5,3], "hard": [4,6]}
    },
    "templates": [
        "A vehicle travels {d} km in {t} hours. Find its speed.",
        "If a car covers {d} km in {t} hours, what is its speed?",
        "How fast is a vehicle that travels {d} km in {t} hours?"
    ]
},

"TSD_DISTANCE": {
    "topic": "Arithmetic",
    "sub_topic": "Time Speed Distance & Work",
    "concept": "Distance from Speed and Time",
    "formula": "distance_from_st",
    "unit": "km",
    "params": {"s": ["speed"], "t": ["time"]},
    "param_rules": {
        "s": {"easy": [30,40], "medium": [50,60], "hard": [70,80]},
        "t": {"easy": [2,3], "medium": [4,5], "hard": [6,8]}
    },
    "templates": [
        "Find the distance travelled at a speed of {s} km/h in {t} hours.",
        "How far will a vehicle go if it moves at {s} km/h for {t} hours?"
    ]
},

"TSD_TIME": {
    "topic": "Arithmetic",
    "sub_topic": "Time Speed Distance & Work",
    "concept": "Time from Speed and Distance",
    "formula": "time_from_ds",
    "unit": "hours",
    "params": {"d": ["distance"], "s": ["speed"]},
    "param_rules": {
        "d": {"easy": [120,180], "medium": [240,300], "hard": [360,480]},
        "s": {"easy": [40,60], "medium": [60,75], "hard": [80,90]}
    },
    "templates": [
        "How much time will it take to cover {d} km at a speed of {s} km/h?",
        "Find the time required to travel {d} km at {s} km/h."
    ]
},

"TSD_AVG_SPEED": {
    "topic": "Arithmetic",
    "sub_topic": "Time Speed Distance & Work",
    "concept": "Average Speed for Equal Distances",
    "formula": "average_speed_equal",
    "unit": "kmph",
    "params": {"s1": ["speed1"], "s2": ["speed2"]},
    "param_rules": {
        "s1": {"easy": [30,40], "medium": [50,60], "hard": [70,80]},
        "s2": {"easy": [60,80], "medium": [70,90], "hard": [100,120]}
    },
    "templates": [
        "A person travels equal distances at speeds {s1} km/h and {s2} km/h. Find the average speed.",
        "Find the average speed when equal distances are covered at {s1} km/h and {s2} km/h."
    ]
},

"TSD_TRAIN": {
    "topic": "Arithmetic",
    "sub_topic": "Time Speed Distance & Work",
    "concept": "Train Crossing a Platform",
    "formula": "train_crossing_time",
    "unit": "seconds",
    "params": {"l": ["length"], "s": ["speed"]},
    "param_rules": {
        "l": {"easy": [100,150], "medium": [200,250], "hard": [300,400]},
        "s": {"easy": [36,54], "medium": [60,72], "hard": [90,108]}
    },
    "templates": [
        "A train of length {l} meters is moving at a speed of {s} km/h. How long will it take to cross a pole?",
        "Find the time taken by a train {l} meters long moving at {s} km/h to cross a stationary point."
    ]
},

"TSD_BOAT_STREAM": {
    "topic": "Arithmetic",
    "sub_topic": "Time Speed Distance & Work",
    "concept": "Boat and Stream",
    "formula": "boat_stream_speed",
    "unit": "kmph",
    "params": {"u": ["boat_speed"], "v": ["stream_speed"]},
    "param_rules": {
        "u": {"easy": [10,12], "medium": [15,18], "hard": [20,24]},
        "v": {"easy": [2,3], "medium": [4,5], "hard": [6,8]}
    },
    "templates": [
        "The speed of a boat in still water is {u} km/h and the speed of the stream is {v} km/h. Find the downstream speed.",
        "A boat moves with speed {u} km/h in still water and stream flows at {v} km/h. Find its speed downstream."
    ]
},

"TW_BASIC": {
    "topic": "Arithmetic",
    "sub_topic": "Time Speed Distance & Work",
    "concept": "Work Done Together",
    "formula": "work_together",
    "unit": "days",
    "params": {"a": ["days_a"], "b": ["days_b"]},
    "param_rules": {
        "a": {"easy": [10,12], "medium": [15,18], "hard": [20,24]},
        "b": {"easy": [15,20], "medium": [24,30], "hard": [30,36]}
    },
    "templates": [
        "A can complete a work in {a} days and B in {b} days. How long will they take together?",
        "If A alone can do a work in {a} days and B alone in {b} days, find the time taken by both together."
    ]
},

"TW_EFFICIENCY": {
    "topic": "Arithmetic",
    "sub_topic": "Time Speed Distance & Work",
    "concept": "Efficiency Based Work",
    "formula": "efficiency_work",
    "unit": "days",
    "params": {"a": ["days_a"], "b": ["days_b"]},
    "param_rules": {
        "a": {"easy": [10], "medium": [15], "hard": [20]},
        "b": {"easy": [20], "medium": [30], "hard": [40]}
    },
    "templates": [
        "A is twice as efficient as B. If B can complete a work in {b} days, how long will A take?",
        "If A takes {a} days to complete a work and B is half as efficient, find the time taken by B."
    ]
},

"TW_WAGES": {
    "topic": "Arithmetic",
    "sub_topic": "Time Speed Distance & Work",
    "concept": "Work and Wages",
    "formula": "work_wages",
    "unit": "currency",
    "params": {"a": ["days_a"], "b": ["days_b"], "w": ["wages"]},
    "param_rules": {
        "a": {"easy": [10], "medium": [12], "hard": [15]},
        "b": {"easy": [5], "medium": [6], "hard": [8]},
        "w": {"easy": [600], "medium": [960], "hard": [1200]}
    },
    "templates": [
        "A and B earn {w} together. If A works for {a} days and B for {b} days, find A's share.",
        "The total wages for a work is {w}. A works for {a} days and B for {b} days. How much does A earn?"
    ]
},

"TW_PIPES": {
    "topic": "Arithmetic",
    "sub_topic": "Time Speed Distance & Work",
    "concept": "Pipes and Cisterns",
    "formula": "pipes_fill_time",
    "unit": "hours",
    "params": {"f": ["fill"], "e": ["empty"]},
    "param_rules": {
        "f": {"easy": [10], "medium": [12], "hard": [15]},
        "e": {"easy": [20], "medium": [24], "hard": [30]}
    },
    "templates": [
        "A pipe can fill a tank in {f} hours while another pipe empties it in {e} hours. How long will it take to fill the tank?",
        "One pipe fills a tank in {f} hours and another empties it in {e} hours. Find the net time taken."
    ]
}

}
