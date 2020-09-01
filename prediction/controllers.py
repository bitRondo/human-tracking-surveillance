import pandas as pd
from django.utils import timezone
from datetime import date, timedelta



def makePrediction(startDate, endDate, model, data):
        nowDate = timezone.now().today().date()
        startDateDiff = (startDate-nowDate).days
        endDateDiff = (endDate-nowDate).days
        predictions = model.predict(start=len(data), end=len(data)+endDateDiff, dynamic=False)
        predictions = [round(num).astype(int) for num in predictions]
        date_list = [nowDate + timedelta(days=x) for x in range(endDateDiff+1)]
        dictionary = dict(zip(date_list, predictions))
        dictionary = dict(list(dictionary.items())[startDateDiff:])
        return dictionary

def findPeak(d):
    peakValue = max(d.items(), key=lambda x: x[1])
    dates = []
    # Iterate over all the items in dictionary to find keys with max value
    for key, value in d.items():
        if value == peakValue[1]:
            dates.append(key)
    return dates, peakValue[1]





def get_model_field_names(model, ignore_fields=['content_object']):
    
    model_fields = model._meta.get_fields()
    model_field_names = list(set([f.name for f in model_fields if f.name not in ignore_fields]))
    return model_field_names


def get_lookup_fields(model, fields=None):
    
    model_field_names = get_model_field_names(model)
    if fields is not None:
        
        lookup_fields = []
        for x in fields:
            if "__" in x:
                # the __ is for ForeignKey lookups
                lookup_fields.append(x)
            elif x in model_field_names:
                lookup_fields.append(x)
    else:
        
        lookup_fields = model_field_names
    return lookup_fields

def qs_to_dataset(qs, fields=None):
    
    
    lookup_fields = get_lookup_fields(qs.model, fields=fields)
    return list(qs.values(*lookup_fields))


    
def convert_to_dataframe(qs, fields=None, index=None):
    
    lookup_fields = get_lookup_fields(qs.model, fields=fields)
    index_col = None
    if index in lookup_fields:
        index_col = index
    elif "id" in lookup_fields:
        index_col = 'id'
    values = qs_to_dataset(qs, fields=fields)
    df = pd.DataFrame.from_records(values, columns=lookup_fields, index=index_col)
    return df
