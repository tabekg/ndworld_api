def make_response(payload=None, status='success', status_code=200):
    return {
        'status': status,
        'payload': payload,
    }, status_code


def orm_to_dict(orm, keys=None, additional_fields=None):
    if keys is None:
        keys = []
    if orm is None:
        return None
    if 'id' not in keys:
        keys += ['id']
    if additional_fields is None:
        additional_fields = {}
    if isinstance(orm, list):
        items = []
        for i in orm:
            if keys is None and hasattr(i, 'to_dict_list'):
                d = i.to_dict_list()
            else:
                d = {}
                for j in keys:
                    d[j] = getattr(i, j)
                for j in additional_fields.keys():
                    d[j] = additional_fields[j](i)
            items.append(d)
        return items

    resp = {k: getattr(orm, k) for k in keys}

    for j in additional_fields.keys():
        resp[j] = additional_fields[j](orm)

    return resp
