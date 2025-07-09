from django import forms

class UploadImageForm(forms.Form):
    image = forms.ImageField()

    OPERATION_CHOICES = [
        ('blur', 'Blur'),
        ('rotate', 'Rotate'),
        ('resize', 'Resize'),
        ('crop', 'Crop'),
        ('grayscale', 'Grayscale'),
        ('to_pdf', 'Convert to PDF'),
    ]
    operation = forms.ChoiceField(choices=OPERATION_CHOICES)

    blur_intensity = forms.IntegerField(
        required=False,
        label='Blur Intensity',
        min_value=1,
        max_value=50,
        initial=15,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': 1})
    )

    ROTATION_CHOICES = [
        (90, '90°'),
        (180, '180°'),
        (270, '270°'),
    ]
    rotation_angle = forms.ChoiceField(
        choices=ROTATION_CHOICES,
        required=False,
        label='Rotation Angle'
    )

    SCALE_CHOICES = [
        (100, '100%'),
        (200, '200%'),
        (300, '300%'),
    ]
    scale_factor = forms.ChoiceField(
        choices=SCALE_CHOICES,
        required=False,
        label='Resize Scale'
    )
    CROP_CHOICESC=[
        (25,'25% Center Crop'),
        (50,'50% Center Crop'),
        (75,'75% Center Crop'),
        (100,'100% (No Crop)'),
    ]
    crop_percentage = forms.ChoiceField(
        choices=CROP_CHOICESC,
        required= False,
        label='Crop Percentage'
    )
    crop_top = forms.IntegerField(required=False, label='Top', min_value=0)
    crop_left = forms.IntegerField(required=False, label='Left', min_value=0)
    crop_width = forms.IntegerField(required=False, label='Width', min_value=1)
    crop_height = forms.IntegerField(required=False, label='Height', min_value=1)