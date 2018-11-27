import json
from django import forms
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

from .settings import DADATA_API_URL, DADATA_API_TOKEN

class DadataWidget(forms.TextInput):
    """
    Base class for dadata jquery widgets
    
    Subclass and define widget_type. It can be 
    ('NAME', 'PARTY', 'ADDRESS', 'BANK', 'EMAIL')
    see https://dadata.ru/suggestions/usage/
    """
    # subclasses should override this props
    jscode = "console.log(suggestion);"
    widget_type = None
     
    options = {
        'url' : DADATA_API_URL,
        'token' : DADATA_API_TOKEN,
        'count' : 5,
        'input_id' : 'id_name',
        'type' : widget_type,
        'linked_fields' : {}, # should be a map like { '<dadata_field_name>' : '<input_id>' }
    }
    
    def start_jscript(self, options):
        jscode = """<script type="text/javascript">
                        $(document).ready(function() {\n
                                $("#%(input_id)s").suggestions({
                                serviceUrl: "%(url)s",
                                token: "%(token)s",
                                type: "%(type)s",
                                count: %(count)s,
                                onSelect: function(suggestion) {\n
                                    linked_fields = %(linked_fields)s;
                        """ % options 
        return jscode
    
    def close_jscript(self):
        return """                        }\n
                                });\n
                        });\n</script>"""

    def render_jscript(self, options, inner_js=None):
        return self.start_jscript(options) + inner_js + self.close_jscript()
    
    def get_options(self):
        """
        Subclass to add/modify options or drop unneccessary.
        
        :return: Dictionary of options to be passed to widget's javascript
        :rtype: :py:obj:`dict`
        """
        options = dict(self.options)
        if self.widget_type:
            options['type'] = self.widget_type
        return options
                   
    def render(self, name, value, attrs=None):
         
        jscode = self.jscode
        options = self.get_options()
        attrs = self.build_attrs(attrs)
        attrs['autocomplete'] = 'off'
        
        if self.widget_type:
            id_ = attrs.get('id', None)
            
            linked_fields_ = attrs.get('data-linked-fields', None)
            if linked_fields_:
                options['linked_fields'] = json.dumps(linked_fields_)
            options['input_id'] = id_
            if jscode:
                jscode = self.render_jscript(options, jscode) 
        
        s = unicode(super(DadataWidget, self).render(name, value, attrs))
        s += jscode
        return mark_safe(s)
    
    class Media:
        js = (#'kladr_api/js/jquery.kladr.min.js',
               'https://dadata.ru/static/js/lib/jquery.suggestions-15.8.min.js',
              )
        
        css = {
               'all': ('https://dadata.ru/static/css/lib/suggestions-15.8.css',
                       'dadata/css/common.css',
                       )
               } 

class DadataAddressWidget(DadataWidget):
    """
    Russian address select input.
    Uses dadata.ru JQuery plugin for suggestions.
    """
    widget_type = 'ADDRESS'
    jscode = """$(linked_fields['lat']).val(suggestion.data.geo_lat);
                $(linked_fields['lon']).val(suggestion.data.geo_lon);
             """
        
class DadataOrgWidget(DadataWidget):
    """
    Russian organisation select input.
    Uses dadata.ru JQuery plugin for suggestions.
    """
    widget_type = 'PARTY'
    jscode = """$(linked_fields['inn']).val(suggestion.data.inn);
                $(linked_fields['kpp']).val(suggestion.data.kpp);
            """

class DadataBankWidget(DadataWidget):
    """
    Russian bank select input.
    Uses dadata.ru JQuery plugin for suggestions.
    """
    widget_type = 'BANK'
    jscode = """$(linked_fields['bic']).val(suggestion.data.bic);
                $(linked_fields['corr']).val(suggestion.data.correspondent_account);
            """       
