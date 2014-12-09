from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context
from inlinestyler.utils import inline_css
import lxml.html


class TemplateEmail(EmailMultiAlternatives):
    """
    Makes it a little easier to send HTML+plaintxt emails using templates
    """
    template = None
    context = {}
    html = None

    _rendered = False

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', self.context)
        template = kwargs.pop('template', self.template)
        super(TemplateEmail, self).__init__(*args, **kwargs)
        self.template = template

        self._default_context = {}
        self._override_context = context or {}

    def render(self):
        tpl = loader.get_template(self.template)

        context = self._default_context
        context.update(self.context)
        context.update(self._override_context)

        context_subject = dict(context, _subject=True)
        context_body = dict(context, _body=True)
        context_html = dict(context, _bodyhtml=True)

        subject = tpl.render(Context(context_subject)).strip()
        body = tpl.render(Context(context_body)).strip()
        html = tpl.render(Context(context_html)).strip()

        if subject != '':
            self.subject = subject
        if body != '':
            self.body = body
        if html != '':
            base_url = getattr(settings, "TEMPLATE_EMAIL_BASE_URL")
            if base_url:
                html_doc = lxml.html.fromstring(html)
                html_doc.make_links_absolute(base_url)
                html = lxml.html.tostring(html_doc, include_meta_content_type=True)
            if getattr(settings, "TEMPLATE_EMAIL_INLINE_CSS", True):
                html = inline_css(html)
            self.html = html

        self._rendered = True

    def send(self, *args, **kwargs):
        if not self._rendered:
            self.render()

        if self.html and self.html != '':
            self.attach_alternative(content=self.html, mimetype='text/html')

        if not isinstance(self.to, (list, tuple)):
            self.to = [self.to]

        for i, recip in enumerate(self.to):
            # Convert user objects if they're in the recipients list
            if isinstance(recip, AbstractBaseUser):
                self.to[i] = '"%s" <%s>' % (recip.get_full_name(), recip.email)

        super(TemplateEmail, self).send(*args, **kwargs)
