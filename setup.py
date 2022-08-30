from setuptools import setup


setup(
    name='marc2bib',
    version='0.1.7',
    url='https://github.com/xymaxim/marc2bib',
    author='Maxim Stolyarchuk',
    author_email='maxim.stolyarchuk@gmail.com',
    description='Easily convert MARC bibliographic records to BibTeX entries',
    long_description=__doc__,
    zip_safe=False,
    install_requires=[
        'pymarc',
    ],
    py_modules=['marc2bib'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: General',
    ]
)
