from __future__ import print_function
from distutils.core import setup
import os

PLUGIN_DIR = 'Extensions.vZapHistory'

def compile_translate():
	for lang in os.listdir('po'):
		if lang.endswith('.po'):
			src = os.path.join('po', lang)
			lang = lang[:-3]
			destdir = os.path.join('src/locale', lang, 'LC_MESSAGES')
			if not os.path.exists(destdir):
				os.makedirs(destdir)
			dest = os.path.join(destdir, 'vZapHistory.mo')
			print("Language compile %s -> %s" % (src, dest))
			if os.system("msgfmt '%s' -o '%s'" % (src, dest)) != 0:
				raise RuntimeError("Failed to compile", src)

compile_translate()

setup(name = 'enigma2-plugin-extensions-vzaphistory',
		version='1.0',
		author='Vasiliks',
		author_email='vasiliks73@gmail.com',
		package_dir = {PLUGIN_DIR: 'src'},
		packages=[PLUGIN_DIR],
		package_data={PLUGIN_DIR: ['buttons/*.png']},
		description = 'Quick zapping between last viewed channels',
	)
