=====================
Django Template Email
=====================

django-template-email provides a set of tools that allows you to easily build 
plain-text or HTML emails using templates.

Usage
=====
After installing django-templatee-email, add ``template_email`` to your 
``INSTALLED_APPS`` in ``settings.py``.

Templates
---------
An email template is like any other django template. To use the template as an
email, however, you must load the "email" templatetag library and use its tags
to define the different parts of the email.  The email templatetag library 
gives you three different tags to use: ``subject``, ``body``, and 
``bodyhtml``, each with their respective ``endsubject``, ``endbody``, and 
``endbodyhtml``.

For example ::
  
  {% load email %}
  {% subject %}Thank you for signing up!{% endsubject %}
  {% body %}
  Hello, {{ first_name }}.

  Thank you for signing up. To find out more information, please visit
  http://www.example.com/foo/.

  Sincerely, 
  The Team
  {% endbody %}
  {% bodyhtml %}
  Hello, <em>{{ first_name }}</em>.

  Thank you for signing up.  To find out more information, click
  <a href="http://www.example.com/foo/">here</a>.
  {% endbodyhtml %}

Each tag is entirely optional. You can set any part of the email as you 
normally would with Djanog's EmailMessage class.

Sending Email
-------------------
The TemplateEmail class is a subclass of 
django.core.mail.EmailMultiAlternatives, which itself is a subclass of
django.core.mail.EmailMessage.

To send your email template as an email, simply instantiate the TemplateEmail 
class while passing it your template and (optionally) a context dict::

  from template_email import TemplateEmail
  
  context = {'first_name': user.first_name}
  email = TemplateEmail(template='email/confirmation_message.html', context=context)
  email.send()


TemplateEmail Class
-------------------
Of course, you may also extend the TemplateEmail class to suit your needs. 
The TemplateEmail class is initialized with optional keyword arguments
of ``template`` and ``context``.  However, template and context variables may be
overridden as a property as well.  The TemplateEmail class has the following
properties:
  
* ``template``: The template used to render the email
* ``context``: The context provided to the template
* ``subject``: The subject of the email
* ``body``: The plan-text body of the email
* ``html``: The html to attach as an alternative type

The ``subject``, ``body``, and ``html`` properties are intended as defaults,
and will be overridden by whatever is given in the template.

When you call the ``send()`` method, the TemplateEmail class first renders the 
given template into the different parts of the email. The templatetags simply
dump their contents into temporary context variables for the ``render()`` method
use.  The render method then renders the contents of each tag separately into 
the class's ``subject``, ``body``, and ``bodyhtml`` properties.  

As a convienience, the ``send()`` method will automatically convert User model
instances to email recipients, formatting them as "first_name last_name 
<email>".


Inline styles
-------------
Some email clients strip out <head> and <style> tags from emails, so
TemplateEmail will automatically inline your CSS styles as long as you include
them directly within <style> tags.

You can disable this behavior by setting ``TEMPLATE_EMAIL_INLINE_CSS = False``
in ``settings.py``.


Absolute links
--------------
Set ``TEMPLATE_EMAIL_BASE_URL`` in ``settings.py`` to the base url of your site
to have TemplateEmail automatically convert relative links to absolute.
