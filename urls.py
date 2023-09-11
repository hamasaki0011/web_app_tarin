import views
from common.urls.pattern import URLPattern

# pathとview関数の対応
# URL_VIEW = {
url_patterns = {
    URLPattern("/now", views.now),
    URLPattern("/show_request", views.show_request),
    URLPattern("/parameters", views.parameters),
    URLPattern("/user/<user_id>/profile", views.user_profile),
    # 2023.8.28 In order to check cookies'
    URLPattern("/set_cookie", views.set_cookie),
    # 2023.8.29 For confirming function of log-in using cookie
    URLPattern("/login", views.login),
    URLPattern("/welcome", views.welcome),
    URLPattern('/upload', views.upload),
    # URLPattern("/upload_complete", views.upload_complete),
    
    # "/now": views.now,
    # "/show_request": views.show_request,
    # "/parameters": views.parameters,
    # "/user/<user_id>/profile": views.user_profile,
    
}