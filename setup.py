from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

def requirements():
    req = []
    for line in open('requirements.txt','r'):
        req.append(line.split()[0])
    return req

setup(
    name='FacebookSearch',
    version='0.0.3',
    description='A Python library to easily iterate public information found by the Facebook Graph API',
    url='http://github.com/ckoepp/FacebookSearch',
    author='Christian Koepp, Norbert Wiedermann',
    author_email='christian.koepp@tum.de',
    license='MIT',
    packages=[ 'FacebookSearch' ],
    install_requires=requirements(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
    ],
    zip_safe=False)
