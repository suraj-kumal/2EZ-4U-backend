from django.core.files.images import get_image_dimensions
from django.contrib import admin
from django import forms
from smartad.models import Advertisement,BannerType,AdvertisementTag

from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget

# define forms here..
class AdvertisementForm(forms.ModelForm):
    # tags = TagField(required=False, widget=LabelWidget)
    class Meta:
        model = Advertisement 
        exclude = ('code',)
    
    def clean_banner_image(self):
        banner_type = BannerType.objects.get(id=self.cleaned_data['banner_type'].id)

        banner_image = self.cleaned_data['banner_image']
        if not banner_image:
            raise forms.ValidationError("No image!")
        else:
            w, h = get_image_dimensions(banner_image)
            print(banner_type.width,'===',type(banner_type.width))
            if w != banner_type.width:
                raise forms.ValidationError(f"The image is {w} pixel wide. It's supposed to be {banner_type.width}")
            if h != banner_type.height:
               raise forms.ValidationError(f"The image is {h} pixel high. It's supposed to be {banner_type.height}")
        return banner_image

class AdvertisementTagForm(forms.ModelForm):
    tags = TagField(required=False, widget=LabelWidget)
    class Meta:
        model = AdvertisementTag
        exclude = ('code',)
    
