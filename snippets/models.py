from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
# these 3 added for authentication & permissions:
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item,item) for item in get_all_styles())

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)  # switch line numbers on and off
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    # these 2 added for authentication & permissions:
    owner = models.ForeignKey('auth.User', related_name='snippets')  # user who created the code snippet
    highlighted = models.TextField()  # highlighted HTML representation of the code

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        ** After adding this we need to update our database tables (or just delete the database and start again,
        ** for the purposes of this tutorial).
        """
        lexer = get_lexer_by_name(self.language)  # lexer performs lexical analysis
            # on lexers: http://www.quora.com/What-is-the-difference-between-a-lexer-and-a-parser
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)  # calling superclass method to ensure object gets saved to database


class Meta:
    ordering = ('created',)
