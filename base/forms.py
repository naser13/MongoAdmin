from collections import defaultdict

from django import forms

TYPES_NOT_FILTERED = ['Object', 'ObjectId', 'Array']
NUMERIC_TYPES = ['Number', 'NumberLong']
DATE_TYPES = ['Date']


class SearchForm(forms.Form):
    page = forms.IntegerField(initial=1)
    per_page = forms.IntegerField(initial=10)

    def __init__(self, *args, **kwargs):
        self.keys = kwargs.pop("keys")
        super(SearchForm, self).__init__(*args, **kwargs)
        for key, key_type in self.keys:
            if key_type not in TYPES_NOT_FILTERED:
                if key_type in NUMERIC_TYPES:
                    self.fields[key] = forms.IntegerField(required=False)
                elif key_type in DATE_TYPES:
                    self.fields[key + "__gte"] = forms.DateTimeField(required=False)
                    self.fields[key + "__lte"] = forms.DateTimeField(required=False)
                else:
                    self.fields[key] = forms.CharField(required=False)

    def get_result(self, strict=False):
        result = defaultdict(lambda: {})
        for key, key_type in self.keys:
            if key_type not in TYPES_NOT_FILTERED:
                if key_type in DATE_TYPES:
                    if self.cleaned_data[key + "__gte"]:
                        if strict:
                            result[key]["$gte"] = {"$date": self.cleaned_data[key + "__gte"].isoformat()}
                        else:
                            result[key]["$gte"] = self.cleaned_data[key + "__gte"]
                    if self.cleaned_data[key + "__lte"]:
                        if strict:
                            result[key]["$lte"] = {"$date": self.cleaned_data[key + "__lte"].isoformat()}
                        else:
                            result[key]["$lte"] = self.cleaned_data[key + "__lte"]
                elif self.cleaned_data[key]:
                    result[key] = self.cleaned_data[key]
        return result
