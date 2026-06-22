def evaluate_rule(rule, data):

    if rule == "LOW_STOCK":

        return data.quantity < 10

    return False
