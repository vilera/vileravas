from typing import NamedTuple, List

import requests


class Data(NamedTuple):
    name: str
    misc: List[str]


def get_vacancies(vac_name):
    data = []
    r = requests.get(f'https://api.hh.ru/vacancies/?text={vac_name}')

    result = r.json()
    vacancies = result.get('items', [])
    vacancies = vacancies if len(vacancies) < 10 else vacancies[:10]

    for vac in vacancies:
        try:
            r = requests.get(f'https://api.hh.ru/vacancies/{vac.get("id")}')
            result = dict(r.json())
        except Exception as e:
            continue
        try:
            data.append(
                Data(
                    name=result.get('name'),
                    misc=[result.get('description'), ", ".join([i.get('name') for i in result.get('key_skills')]), result.get('employer', {}).get('name'), result['salary']['from'] if result.get('salary') else '', result.get('area', {}).get('name'), result.get('published_at').split('T')[0]]
                )
            )
        except Exception as e:
            pass
    return data
