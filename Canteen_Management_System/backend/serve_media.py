from django.http import HttpResponse, Http404
from django.conf import settings
import os
import mimetypes

def serve_media(request, path):
    """Serve media files in production with fallback"""
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        
        if os.path.exists(file_path):
            # File exists, serve it
            content_type, _ = mimetypes.guess_type(file_path)
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type=content_type)
                return response
        else:
            # File doesn't exist, return placeholder image URL
            from django.http import HttpResponseRedirect
            placeholder_url = "https://via.placeholder.com/300x200/cccccc/666666?text=No+Image"
            return HttpResponseRedirect(placeholder_url)
            
    except Exception:
        # Error occurred, redirect to placeholder
        from django.http import HttpResponseRedirect
        placeholder_url = "https://via.placeholder.com/300x200/cccccc/666666?text=Error"
        return HttpResponseRedirect(placeholder_url)