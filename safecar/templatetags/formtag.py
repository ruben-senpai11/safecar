# here I want create custom filter,first we create the folder templatetags in my app , add to this folder the __init__.py file
# create you custom filter and add decorator to this
# go  to your gabarit and load it 

from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    # return value.as_widget(attrs={'class': arg})
    css_c=''
    css_classes = value.field.widget.attrs.get('class', None)
    if css_classes:
        css_c= css_classes
    
    if  arg not in css_c:
        css_c = '%s %s' % (css_c, arg)
    return value.as_widget(attrs={'class': css_c})
                         

@register.filter(name='filter_type')
def filter_type(task, task_type):
        
    return task.filter(type_operation__sys_name=task_type) 