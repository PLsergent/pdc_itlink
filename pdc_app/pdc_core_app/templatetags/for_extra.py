import re

from django import template
from django.template.base import TemplateSyntaxError
from django.template.defaulttags import ForNode

register = template.Library()


class ZipExpression(object):
    def __init__(self, var):
        self.var = var

    def resolve(self, *args, **kwargs):
        return zip(*(
            f.resolve(*args, **kwargs) for f in self.var
        ))


@register.tag('for')
def do_for(parser, token):
    """
    For tag with ziping multiple iterables.
    """
    bits = token.contents.split()
    if len(bits) < 4:
        raise TemplateSyntaxError("'foreach' statements should have at least"
                                  " four words: %s" % token.contents)

    is_reversed = False
    try:
        in_index = bits.index('in')
        sequence = bits[in_index+1:]
        if sequence[-1] == 'reversed':
            is_reversed = True
            sequence.pop()
        if not sequence or 'in' in sequence:
            raise ValueError
        sequence = re.split(r' *, *', ' '.join(sequence))
    except ValueError:
        raise TemplateSyntaxError(
            "'foreach' statements should use the format"
            " 'foreach a,b,(...) in x,y,(...)': %s" % token.contents)

    loopvars = re.split(r' *, *', ' '.join(bits[1:in_index]))
    for var in loopvars:
        if not var or ' ' in var:
            raise TemplateSyntaxError("'foreach' tag received an invalid"
                                      " argumewnt: %s" % token.contents)

    if len(sequence) > 1:
        sequence = ZipExpression(map(parser.compile_filter, sequence))
    else:
        sequence = parser.compile_filter(sequence[0])

    nodelist_loop = parser.parse(('empty', 'endfor',))
    token = parser.next_token()
    if token.contents == 'empty':
        nodelist_empty = parser.parse(('endfor',))
        parser.delete_first_token()
    else:
        nodelist_empty = None
    return ForNode(
        loopvars, sequence, is_reversed, nodelist_loop, nodelist_empty)
