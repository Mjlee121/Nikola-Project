# -*- coding: utf-8 -*-

# Copyright © 2014 Ivan Teoh and others.

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from nikola.plugin_categories import RestExtension


class Plugin(RestExtension):

    name = "album_setup"

    def set_site(self, site):
        self.site = site
        directives.register_directive('album_setup', AlbumFigure)
        return super(Plugin, self).set_site(site)


CODE_IMAGE = (u"""<div class="album-figure-media">
<a class="album-figure-image" href="{url}" target="_blank">
<img src="{image_url}" alt="{title}" />
</a>
</div>""")

CODE_URL = (u"""<a class="album-figure-title" href="{url}" target="_blank">{title}</a>""")

CODE_TITLE = (u"""<p class="album-figure-title">{title}</p>""")

CODE_ARTIST = (u"""<p class="album-figure-artist">
by {artist}
</p>""")

CODE_ARTIST_WITH_URL = (u"""<p class="album-figure-artist">
by <a href="{artist_url}" target="_blank">{artist}</a>
</p>""")

CODE_ALBUM_ARTIST = (u"""<tr>
<th>Album_artist:</th>
<td>{album_artist}</td>
</tr>""")

CODE_COMPOSER = (u"""<tr>
<th>Composer:</th>
<td>{composer}</td>
</tr>""")

CODE_YEAR = (u"""<tr>
<th>Year:</th>
<td>{year}</td>
</tr>""")

CODE_ALBUM_NUMBER = (u"""<table class="album-figure-album-number"><tbody>
{album_artist}
{composer}
{year}
</tbody></table>""")

CODE_REVIEW = (u"""<div class="album-figure-review">
{review}
</div>""")

CODE_ALBUM = (u"""<div class="album-figure-content">
{url}
{artist}
{album_number}
{review}
</div>""")

CODE = (u"""<div class="{classes}">
{image_url}
{title}
</div>""")


class AlbumFigure(Directive):
    """ Restructured text extension for inserting album figure

        Usage:

        .. album_setup:: title
            :class: class name
            :url: album url
            :artist: album artist
            :artist_url: album artist url
            :album_artist: album_artist
            :composer: composer
            :year: YEAR
            :image_url: album cover image url

            Your review.
   """

    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'class': directives.unchanged,
        'url': directives.unchanged,
        'artist': directives.unchanged,
        'artist_url': directives.unchanged,
        'album_artist': directives.unchanged,
        'composer': directives.unchanged,
        'year': directives.unchanged,
        'image_url': directives.unchanged,
    }

    def run(self):
        """ Required by the Directive interface. Create docutils nodes """
        options = {
            'title': ' '.join(self.arguments),
            'classes': self.options.get('class', ''),
            'url': self.options.get('url', ''),
            'artist': self.options.get('artist', ''),
            'artist_url': self.options.get('artist_url', ''),
            'album_artist': self.options.get('album_artist', ''),
            'composer': self.options.get('composer', ''),
            'year': self.options.get('year', ''),
            'image_url': self.options.get('image_url', ''),
        }
        if options['image_url']:
            options['image_url'] = CODE_IMAGE.format(**options)
        if options['artist']:
            if options['artist_url']:
                options['artist'] = CODE_ARTIST_WITH_URL.format(**options)
            else:
                options['artist'] = CODE_ARTIST.format(**options)
        if options['album_artist']:
            options['album_artist'] = CODE_ALBUM_ARTIST.format(**options)
        if options['composer']:
            options['composer'] = CODE_COMPOSER.format(**options)
        if options['year']:
            options['year'] = CODE_YEAR.format(**options)
        options['album_number'] = ''
        if options['album_artist'] or options['composer'] or options['year']:
            options['album_number'] = CODE_ALBUM_NUMBER.format(**options)
        options['review'] = ''
        for line in self.content:
            options['review'] += u'<p>{0}</p>'.format(line)
        if options['review']:
            options['review'] = CODE_REVIEW.format(**options)
        if options['url']:
            options['url'] = CODE_URL.format(**options)
        else:
            options['url'] = CODE_TITLE.format(**options)
        options['title'] = CODE_ALBUM.format(**options)
        return [nodes.raw('', CODE.format(**options), format='html')]
