from django import forms 
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_desc','item_price', 'item_image']
        widgets = {
            "item_name":forms.TextInput(attrs={"placeholder":"e.g Margherita Pizza","required":True}),
            "item_desc":forms.TextInput(attrs={"placeholder":"e.g Fresh and cheesy","required":True}),
            "item_price":forms.NumberInput(attrs={"placeholder":"100","required":True}),
            "item_image":forms.URLInput(attrs={"placeholder":"https://www.google.com","required":False}),
        }

    # method for validating the data and specify the field you want to clean 
    # this prevents a negative value being entered 
    def clean_item_price(self):
        price = self.cleaned_data["item_price"]
        if price < 0:
            raise forms.ValidationError("Price cannot be negative!")
        return price
