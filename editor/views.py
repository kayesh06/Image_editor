import os
from django.shortcuts import render
from django.conf import settings
from .forms import UploadImageForm
import cv2
from PIL import Image

def image_editor(request):
    result_image = None
    pdf_result = None

    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            operation = form.cleaned_data['operation']
            input_path = os.path.join(settings.MEDIA_ROOT, image_file.name)

            with open(input_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            image = cv2.imread(input_path)

            if operation == 'blur':
                intensity = form.cleaned_data.get('blur_intensity') or 15
                if intensity % 2 == 0:
                    intensity += 1
                image = cv2.GaussianBlur(image, (intensity, intensity), 0)

            elif operation == 'rotate':
                angle = int(form.cleaned_data.get('rotation_angle'))
                if angle == 90:
                    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                elif angle == 180:
                    image = cv2.rotate(image, cv2.ROTATE_180)
                elif angle == 270:
                    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

            elif operation == 'resize':
                scale_factor = int(form.cleaned_data.get('scale_factor'))
                scale_ratio = scale_factor / 100.0
                width = int(image.shape[1] * scale_ratio)
                height = int(image.shape[0] * scale_ratio)
                image = cv2.resize(image, (width, height))

            elif operation == 'crop':
                top = form.cleaned_data.get('crop_top') or 0
                left = form.cleaned_data.get('crop_left') or 0
                crop_width = form.cleaned_data.get('crop_width') or image.shape[1]
                crop_height = form.cleaned_data.get('crop_height') or image.shape[0]

                bottom = min(top + crop_height,image.shape[0])
                right = min(left + crop_width,image.shape[1])
                image =image[top:bottom,left:right]

            elif operation == 'grayscale':
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            elif operation == 'to_pdf':
                im = Image.open(input_path)
                pdf_name = os.path.splitext(image_file.name)[0] + '.pdf'
                pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_name)
                im.convert('RGB').save(pdf_path, 'PDF')
                pdf_result = pdf_name

            if operation != 'to_pdf':
                result_name = f"edited_{image_file.name}"
                result_path = os.path.join(settings.MEDIA_ROOT, result_name)
                cv2.imwrite(result_path, image)
                result_image = result_name
    else:
        form = UploadImageForm()

    return render(request, 'editor/index.html', {
        'form': form,
        'result': result_image,
        'pdf_result': pdf_result,
        'MEDIA_URL': settings.MEDIA_URL,
    })