from django.core.cache import cache


def site_logo(request):
    # Retrieve the logo from the cache
    return {"site_logo": cache.get("site_logo")}
