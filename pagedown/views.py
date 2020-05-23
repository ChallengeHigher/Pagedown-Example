import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.contrib.auth.decorators import login_required

from pagedown.forms import ImageUploadForm


IMAGE_UPLOAD_PATH = getattr(
    settings, 'PAGEDOWN_IMAGE_UPLOAD_PATH', 'pagedown-uploads')
IMAGE_UPLOAD_ENABLED = getattr(
    settings, 'PAGEDOWN_IMAGE_UPLOAD_ENABLED', False)


@login_required
@csrf_exempt
def image_upload_view(request):
    if not request.method == 'POST':
        raise PermissionDenied()

    if not IMAGE_UPLOAD_ENABLED:
        raise ImproperlyConfigured('Image upload is disabled')

    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        image = request.FILES['image']
        path = os.path.join(IMAGE_UPLOAD_PATH, image.name)
        path = default_storage.save(path, image)
        url = default_storage.url(path)
        return JsonResponse({'success': True, 'url': url})

    return JsonResponse({'success': False, 'error': form.errors})
