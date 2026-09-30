"""Brand embedded presentation assets; leave upstream protocol and attribution intact."""
from pathlib import Path
import shutil

root = Path('/src/www')
for path in root.glob('*.html'):
    text = path.read_text()
    text = text.replace('<title>DATUM', '<title>Paperclip DATUM')
    text = text.replace(' DATUM <span>GATEWAY</span>', ' PAPERCLIP <span>DATUM</span>')
    text = text.replace('(DATUM Logo)', 'Paperclip Pool')
    text = text.replace('type="image/x-icon" href="/assets/icons/favicon.ico"',
                        'type="image/svg+xml" href="/assets/icons/datum_logo.svg"')
    if path.name == 'foot.html':
        text = text.replace('</body>', '<p class="note">Paperclip DATUM · Based on CONVOY DATUM Gateway. <a href="https://pool.paperclippool.xyz/">Paperclip Pool</a></p>\n</body>')
    path.write_text(text)
shutil.copyfile('/branding/icon.svg', root / 'assets/icons/datum_logo.svg')
with (root / 'assets/style.css').open('a') as style:
    style.write('\n/* Paperclip presentation */\nbody{background:#111c2e;color:#eef2fa}a{color:#f56835}h1 span{color:#f56835}\n')
