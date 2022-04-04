def unflatten(dictionary):
    resultDict = dict()
    for key, value in dictionary.items():
        parts = key.split("__")
        d = resultDict
        for part in parts[:-1]:
            if part not in d:
                d[part] = dict()
            d = d[part]
        d[parts[-1]] = value
    return resultDict
