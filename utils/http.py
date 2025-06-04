from flask import g

from models.translation import Translation


def make_response(payload=None, status='success', status_code=200):
    return {
        'status': status,
        'payload': payload,
    }, status_code


def orm_to_dict(orm, keys=None, additional_fields=None, translate=None):
    if keys is None:
        keys = []
    if orm is None:
        return None
    if 'id' not in keys:
        keys += ['id']
    if additional_fields is None:
        additional_fields = {}
    if translate is None:
        translate = {}
    if isinstance(orm, list):
        items = []
        for i in orm:
            if len(keys) == 1 and hasattr(i, 'to_dict_list'):
                d = i.to_dict_list()
            else:
                d = orm_to_dict(i, keys, additional_fields, translate)
            items.append(d)
        return items

    resp = {}

    for k in keys:
        if hasattr(orm, k):
            resp[k] = getattr(orm, k)
            if k in translate:
                translation = g.db.query(Translation).filter(
                    Translation.source_text == resp[k],
                    Translation.target_language == g.locale,
                ).first()
                if translation:
                    resp[k] = translation.target_text
        # elif hasattr(orm, k + '_' + DEFAULT_LANGUAGE):
        #     resp[k] = getattr(orm, k + '_' + DEFAULT_LANGUAGE)

    for j in additional_fields.keys():
        resp[j] = additional_fields[j](orm)

    return resp
