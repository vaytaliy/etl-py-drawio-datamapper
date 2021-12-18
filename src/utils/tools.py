"""
takes generic list: empty of with values
appends comma separated values or a single value
"""
def add_to_comma_separated_list(comma_separated_list, added_values):
    str_list = str(comma_separated_list)
    trimmed_added_values = str(added_values).replace(" ", "")

    if len(str_list) == 0:
        str_list += trimmed_added_values
    else:
        str_list += ',' + trimmed_added_values

    return str_list
