from urllib.parse import urlparse

from django import forms
from django.conf import settings
from django.contrib.sites.models import Site

from .models import Link, Tag


class LinkFormMixin(object):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(LinkFormMixin, self).__init__(*args, **kwargs)

        key_field = self.fields.get('key')
        title_field = self.fields.get('title')
        tags_field = self.fields.get('tags')

        if key_field:
            key_field.required = False
        if title_field:
            title_field.required = False
        if tags_field:
            tags_field.initial = ','.join(
                self.instance.tags.values_list('name', flat=True)
            )

    def clean_destination(self):
        '''
        Raise validation error if User enters a url that originates from this site.
        '''

        destination = self.cleaned_data.get('destination')
        url = urlparse(destination)
        site_domain = Site.objects.get_current().domain

        if url.hostname == site_domain:
            raise forms.ValidationError('Sorry, this url is not allowed!')

        return destination

    def clean_key(self):
        '''
        Raise validation error if key is given, but User is not given.
        Raise validation error if User enters an existing key.
        '''

        user_not_exists = not self.user or not self.user.is_authenticated
        key = self.cleaned_data.get('key')

        # If key is given and (User is None or
        # User not authenticated), raise exception.
        if key and user_not_exists:
            raise forms.ValidationError('Only logged in users can define key.')

        # If a key is given and an existing url has same key, raise exception.
        if key and Link.objects.filter(key=key).exists():
            raise forms.ValidationError('Custom link is already taken!')

        # Normalize key. Raise validation error if a raw key
        # was given, but a cleaned_key was not obtained.
        # This indicates that the key is invalid.
        cleaned_key = Link.normalize_key(key)
        if key and not cleaned_key:
            raise forms.ValidationError(
                'Custom key can only contain alphanumeric '
                'characters and dashes'
            )

        return cleaned_key

    def clean_title(self):
        '''
        Raise validation error if title is given, but User is not given.
        '''

        user_not_exists = not self.user or not self.user.is_authenticated
        title = self.cleaned_data.get('title')

        # If title is given and (User is None or
        # User not authenticated), raise exception.
        if title and user_not_exists:
            raise forms.ValidationError(
                'Only logged in users can define a title.'
            )
        return title

    def clean_tags(self):
        '''
        Resolve tags from an input string.
        Raise validation error if more than 8 tags.
        '''

        user_not_exists = not self.user or not self.user.is_authenticated
        tags = self.cleaned_data.get('tags')

        if tags:
            # If tags is given and (User is None or
            # User not authenticated), raise exception.
            if user_not_exists:
                raise forms.ValidationError(
                    'Only logged in users can define tags.'
                )

            # Split and normalize text from tags input.
            tags = [Tag.normalize_text(tag) for tag in tags.split(',')]

            # Filter 'None' from tags list.
            tags = list(filter(lambda x: x, tags))

            # Raise exception if tag length exceeds limit.
            if len(tags) > settings.TAG_LIMIT:
                raise forms.ValidationError(
                    'Cannot have more than {} tags.'.format(settings.TAG_LIMIT)
                )

            # Resolve Tag objects from tags list.
            tags = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]

        return tags

    def save(self, commit=True):
        '''
        Overrides form save method.
        Generates key if key does not exist.
        Sets User if user is authenticated.
        '''

        link = super(LinkFormMixin, self).save(commit=False)

        # Generate random key for Link if key does not exist.
        if not link.key:
            link.key = Link.make_key()

        # Set User if User is authenticated.
        if self.user and self.user.is_authenticated:
            link.user = self.user

        # Set default link title
        if not link.title:
            title = 'Link - {}'.format(link.key)
            link.title = title

        link.save()

        # Get tags to update link tags.
        tags = self.cleaned_data.get('tags')

        # If form had tag field
        if tags is not None:

            # Get tags before saving edit and
            # tags that were just entered.
            old_tags = set(link.tags.all())
            new_tags = set(tags)

            # Clear existing tags.
            link.tags.clear()

            # Remove cleared tags that have no m2m to links.
            for tag in old_tags.difference(new_tags):
                if not tag.links.exists():
                    tag.delete()

            if tags:
                # Add tags to link.
                link.tags.add(*tags)

        return link


class LinkForm(LinkFormMixin, forms.ModelForm):
    class Meta:
        model = Link
        fields = ['destination', 'key']


class LinkEditForm(LinkFormMixin, forms.ModelForm):
    tags = forms.CharField(required=False)

    class Meta:
        model = Link
        fields = ['destination', 'title']
