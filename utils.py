import us
import pandas as pd

def format_currency_label(value, prefix=""):
    """
    Format a numerical value as a currency label.

    :param prefix: the prefix (e.g $ for currency)
    :param value: The numerical value to format.
    :return: Formatted currency label string.
    """
    if value >= 1e9:  # Billion
        return f'{prefix}{value / 1e9:.2f} bn'
    elif value >= 1e6:  # Million
        return f'{prefix}{value / 1e6:.2f} M'
    elif value >= 1e3:  # Thousand
        return f'{prefix}{value / 1e3:.2f} K'
    else:
        return f'{prefix}{value:.2f}'


def add_state_code(state_name):
    state = us.states.lookup(state_name)
    return state.abbr if state else None