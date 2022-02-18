import pandas as pd


def awk(colConditions, table):
    """
    Grab rows based on list of lists column 
    conditions from dataframe df
    """
    df = pd.DataFrame()
    for n, cond in enumerate(colConditions):
        cond = cond.split()
        col = int(cond[0])
        if len(cond) == 1:
            df[n] = table[col]

        elif len(cond) == 3:
            if cond[1] == ">":
                df[n] = table[col] > int(cond[2])

            elif cond[1] == "==":
                df[n] = table[col] == int(cond[2])

            elif cond[1] == "<":
                df[n] = table[col] < int(cond[2])
