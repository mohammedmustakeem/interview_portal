from practice.Aptitude.formula_engine.formula_engine import FORMULA_REGISTRY


def get_formula(formula_name: str):
    """
    Returns the callable formula function from registry.
    """
    if formula_name not in FORMULA_REGISTRY:
        raise ValueError(f"No formula registered with name: {formula_name}")

    return FORMULA_REGISTRY[formula_name]


def compute_answer(formula_name: str, **kwargs):
    """
    Universal executor for all aptitude formulas.
    """
    formula_fn = get_formula(formula_name)
    return formula_fn(**kwargs)
