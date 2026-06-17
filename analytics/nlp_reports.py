
from poserp.analytics.reports import branch_performance


def generate_report(question):

    if "branch" in question.lower():

        return branch_performance()

    return {}
