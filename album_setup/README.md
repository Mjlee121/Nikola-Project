Plugin to embed book link.

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

This should embed the book link.

### Examples

This reStructuredText document:

```ReST

	.. album_setup:: Get Nikola
        :class: album-figure
        :url: http://getnikola.com/
        :artist: Roberto Alsina
        :artist_url: http://ralsina.me/
        :album_artist: Roberto Alsina
        :composer: Roberto Alsina
        :year: 1993
        :image_url: http://getnikola.com/galleries/demo/tesla2_lg.jpg

        Your review.
```

will result in:

```html

    <div class="album-figure">
        <div class="album-figure-media">
        	<a class="book-figure-image" href="http://getnikola.com/" target="_blank">
        		<img src="http://getnikola.com/galleries/demo/tesla2_lg.jpg" alt="Get Nikola" />
        	</a>
        </div>
        <div class="book-figure-content">
        	<a class="album-figure-title" href="http://getnikola.com/" target="_blank">Get Nikola</a>
        	<p class="album-figure-artist">by <a href="http://ralsina.me/" target="_blank">Roberto Alsina</a></p>
        	<table class="book-figure-book-number">
        		<tbody>
			        <tr><th>Album_Artist:</th><td>Roberto Alsina</td></tr>
			        <tr><th>Composer:</th><td>Roberto Alsina</td></tr>
			        <tr><th>Year:</th><td>1993</td></tr>
        		</tbody>
        	</table>
        	<div class="album-figure-review">
        		<p>Your review.</p>
        	</div>
        </div>
    </div>
```
