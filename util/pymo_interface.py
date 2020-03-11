import pandas as pd


def get_data(pymo_re):
    result = []
    for i in pymo_re:
        i.pop("_id")
        result.append(i)
    return result


def get_data_df(pymo_re):
    result = []
    for i in pymo_re:
        result.append(i)
    result = pd.DataFrame(result)
    return result.drop("_id",axis=1)