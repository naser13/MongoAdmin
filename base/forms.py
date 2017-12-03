from django import forms

TYPES_NOT_FILTERED = ['Object', 'ObjectId', 'Array']
NUMERIC_TYPES = ['Number', 'NumberLong']


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.keys = kwargs.pop("keys")
        super(SearchForm, self).__init__(*args, **kwargs)
        for key, key_type in self.keys:
            if key_type not in TYPES_NOT_FILTERED:
                if key_type in NUMERIC_TYPES:
                    self.fields[key] = forms.IntegerField(required=False)
                else:
                    self.fields[key] = forms.CharField(required=False)

    def get_result(self):
        result = {}
        for key, key_type in self.keys:
            if key_type not in TYPES_NOT_FILTERED and self.cleaned_data[key]:
                result[key] = self.cleaned_data[key]
        return result
