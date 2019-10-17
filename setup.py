from distutils.core import setup
import setup_translate


setup(name = 'enigma2-plugin-extensions-vzaphistory',
		version='1.0',
		author='Vasiliks',
		author_email='vasiliks73@gmail.com',
		package_dir = {'Extensions.vZapHistory': 'src'},
		packages=['Extensions.vZapHistory'],
		package_data={'Extensions.vZapHistory': ['buttons/*.png']},
		description = 'Quick zapping between last viewed channels',
		cmdclass = setup_translate.cmdclass,
	)

