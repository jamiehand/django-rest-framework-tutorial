from django.forms import widgets
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User  # for representing users in API

# A serializer class is very similar to a Django Form class, and includes similar validation flags
# on the various fields, such as required, max_length and default.

# class SnippetSerializer(serializers.Serializer):  # <-- 1st implementation, without ModelSerializer class
#     pk = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#     def create(self, validated_data):
#         """
#         Create and return a new 'Snippet' instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing 'Snippet' instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance

# class SnippetSerializer(serializers.ModelSerializer):  <-- 2nd implementation; more concise w/ ModelSerializer class
class SnippetSerializer(serializers.HyperlinkedModelSerializer):  # <-- 3rd imp.; relating things w/ hyperlinks
    owner = serializers.ReadOnlyField(source='owner.username')  # associates snippet w/ user that created it.
        # After adding "owner" here, also add it to the list of fields in the inner "Meta" class.
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
        # for hyperlinked relationships.
        # Because we've included format suffixed URLs such as '.json', we also need to indicate on the highlight field
        # that any format suffixed hyperlinks it returns should use the '.html' suffix.

    class Meta:
        model = Snippet
        fields = ('url', 'highlight', 'owner', 'title', 'code', 'linenos', 'language', 'style')
            # remove 'id' for hyperlinking; add 'url' and 'highlight' for hyperlinking ('highlight' is same as 'url'
            # field, except that it points to the 'snippet-highlight' url pattern instead of the 'snippet-detail' url
            # pattern.

# New serializer to represent users in the API
class UserSerializer(serializers.HyperlinkedModelSerializer):
    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())  <-- before hyperlinking
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        # fields = ('id', 'username', 'snippets')   <-- before hyperlinking
        fields = ('url', 'username', 'snippets')  # <-- for hyperlinking
            # Because 'snippets' is a reverse relationship on the User model, it will not be included by default when
            # using the ModelSerializer class, so we needed to add an explicit field for it.