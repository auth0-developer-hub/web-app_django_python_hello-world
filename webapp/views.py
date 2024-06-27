from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import auth
from authlib.integrations.django_client import OAuth
from urllib.parse import quote_plus, urlencode
from django.contrib.auth.decorators import login_required

from .models import Profile
from .services.message_service import MessageService

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def login(request):
    return oauth.auth0.authorize_redirect(
        request,
        request.build_absolute_uri(reverse("callback")),
    )


def signup(request):
    return oauth.auth0.authorize_redirect(
        request,
        request.build_absolute_uri(reverse("callback")),
        screen_hint="signup"
    )


def callback(request):
    token = oauth.auth0.authorize_access_token(request)

    user = auth.authenticate(request, token=token)

    if user:
        auth.login(request, user)
        return redirect(request.build_absolute_uri(reverse("profile")))

    return HttpResponse(status=400)


def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


def index(request):
    template = loader.get_template('home/index.html')

    context = {
        "features": [{
            "title": "Identity Providers",
            "description":
                "Auth0 supports social providers such as Google, Facebook, and Twitter, along with Enterprise providers "
                "such as Microsoft Office 365, Google Apps, and Azure. You can also use any OAuth 2.0 Authorization "
                "Server.",
            "resourceUrl": "https://auth0.com/docs/connections",
            "icon": "https://cdn.auth0.com/blog/hello-auth0/identity-providers-logo.svg",
        }, {
            "title": "Multi-Factor Authentication",
            "description":
                "You can require your users to provide more than one piece of identifying information when logging in. "
                "MFA delivers one-time codes to your users via SMS, voice, email, WebAuthn, and push notifications.",
            "resourceUrl": "https://auth0.com/docs/multifactor-authentication",
            "icon": "https://cdn.auth0.com/blog/hello-auth0/mfa-logo.svg",
        }, {
            "title": "Attack Protection",
            "description":
                "Auth0 can detect attacks and stop malicious attempts to access your application such as blocking traffic "
                "from certain IPs and displaying CAPTCHA. Auth0 supports the principle of layered protection in security "
                "that uses a variety of signals to detect and mitigate attacks.",
            "resourceUrl": "https://auth0.com/docs/attack-protection",
            "icon": "https://cdn.auth0.com/blog/hello-auth0/advanced-protection-logo.svg",
        }, {
            "title": "Serverless Extensibility",
            "description":
                "Actions are functions that allow you to customize the behavior of Auth0. Each action is bound to a "
                "specific triggering event on the Auth0 platform. Auth0 invokes the custom code of these Actions when the "
                "corresponding triggering event is produced at runtime.",
            "resourceUrl": "https://auth0.com/docs/actions",
            "icon": "https://cdn.auth0.com/blog/hello-auth0/private-cloud-logo.svg",
        }]
    }

    return HttpResponse(template.render(context, request))


@login_required
def profile(request):
    template = loader.get_template('profile/index.html')
    user = request.session.get('user').get('userinfo')

    user_profile = Profile(
        nickname=user.get('nickname'),
        name=user.get('name'),
        picture=user.get('picture'),
        updated_at=user.get('updated_at'),
        email=user.get('email'),
        email_verified=user.get('email_verified'),
        sub=user.get('sub')
    )

    context = {
        'user_profile': user_profile
    }

    return HttpResponse(template.render(context, request))


def public(request):
    template = loader.get_template('public/index.html')
    context = {
        "message": MessageService().public_message()
    }
    return HttpResponse(template.render(context, request))


@login_required
def protected(request):
    template = loader.get_template('protected/index.html')
    context = {
        "message": MessageService().protected_message()
    }
    return HttpResponse(template.render(context, request))


@login_required
def admin(request):
    template = loader.get_template('admin/index.html')
    context = {
        "message": MessageService().admin_message()
    }
    return HttpResponse(template.render(context, request))


def page_not_found_view(request, *args, **kwargs):
    template = loader.get_template('404.html')
    return HttpResponse(template.render(None, request))
