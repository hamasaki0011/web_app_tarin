import views
from common.urls.pattern import URLPattern

# pathとview関数の対応
# URL_VIEW = {
url_patterns = {
    URLPattern("/now", views.now),
    URLPattern("/show_request", views.show_request),
    URLPattern("/parameters", views.parameters),
    URLPattern("/user/<user_id>/profile", views.user_profile),
    
    # "/now": views.now,
    # "/show_request": views.show_request,
    # "/parameters": views.parameters,
    # "/user/<user_id>/profile": views.user_profile,
    
}