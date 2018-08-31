# -*- coding: utf-8 -*-

# This plug-in was created for educational purposes. It was 
# created as part of a project for my dissertation. 
# Please feel free to download, use and edit.


"""audiomack directive for reStructuredText."""

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from nikola.plugins.compile.rest import _align_choice, _align_options_base

from nikola.plugin_categories import RestExtension


class Plugin(RestExtension):
    """Plugin for soundclound directive."""

    name = "rest_audiomack"

    def set_site(self, site):
        """Set Nikola site."""
        self.site = site
        directives.register_directive('audiomack', audiomack)
        return super(Plugin, self).set_site(site)


CODE = """\
<div class="audiomack-player{align}">
<iframe width="{width}%" height="{height}"
scrolling="no" frameborder="no"
src="https://audiomack.com/embed/{song/album}/{uploader}/{album}?background=1">
</iframe>
</div>"""


class audiomack(Directive):
    """reST extension for inserting audiomack embedded music.
    Usage:
        .. audiomack:: <album name>
		   :uploader: <Upload by who>
		   :song/album: <album / song>
           :height: 100
           :width: 600
    """

    has_content = True
    required_arguments = 1
    option_spec = {
        'uploader': directives.unchanged,
        'song/album': directives.unchanged,
        'width': directives.positive_int,
        'height': directives.positive_int,
        "align": _align_choice
    }
    
	

    def run(self):
        """Run the audiomack directive."""
        self.check_content()
        options = {
            'album': self.arguments[0],
            'uploader': self.options.get('uploader', ''),
            'song/album': self.options.get('song/album', ''),
            'width': 600,
            'height': 160,
        }
        options.update(self.options)
        if self.options.get('align') in _align_options_base:
            options['align'] = ' align-' + self.options['align']
        else:
            options['align'] = ''
        return [nodes.raw('', CODE.format(**options), format='html')]

    def check_content(self):
        """Emit a deprecation warning if there is content."""
        if self.content:  # pragma: no cover
            raise self.warning("This directive does not accept content. The "
                               "'key=value' format for options is deprecated, "
                               "use ':key: value' instead")


