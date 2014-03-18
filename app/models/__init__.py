import pprint
from prettytable import PrettyTable

def extract_value_by_text(extracted_hash, key):
    result = None
    if extracted_hash.get(key) and extracted_hash[key].get('values'):
        result = extracted_hash[key]['values'][0]['text']
    return result

def extract_values_by_text(extracted_hash, key):
    results = []
    if extracted_hash.get(key) and extracted_hash[key].get('values'):
        for value in extracted_hash[key]['values']:
            if value['text'] not in results:
              results += [value['text']]
    return results

def extract_values_by_property(extracted_hash, key, sub_key):
    results = []
    if extracted_hash.get(key) and extracted_hash[key].get('values'):
        for value in extracted_hash[key]['values']:
            if value['property'].get(sub_key):
                results += [value['property'][sub_key]['values'][0]['text']]
    return results

def extract_nested_values_by_property(extracted_hash, key, sub_keys_list):
    results = []
    if extracted_hash.get(key) and extracted_hash[key].get('values'):
        for value in extracted_hash[key]['values']:
            result = {}
            for property_key, property_value in value['property'].iteritems():
                for sub_key in sub_keys_list:
                    if (sub_key in property_key.split("/")[-1]) and property_value.get('values'):
                        result[sub_key] = property_value['values'][0]['text']
            results.append(result)
    return results
