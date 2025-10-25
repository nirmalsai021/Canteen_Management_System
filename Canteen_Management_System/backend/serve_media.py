from django.http import HttpResponse, Http404
from django.conf import settings
import os
import mimetypes

def serve_media(request, path):
    """Serve media files in production"""
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        
        if not os.path.exists(file_path):
            raise Http404("File not found")
        
        # Get the file's MIME type
        content_type, _ = mimetypes.guess_type(file_path)
        
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=content_type)
            return response
            
    except Exception:
        raise Http404("File not found")