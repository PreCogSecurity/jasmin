import os
import sys
import uuid

from setuptools import setup, find_packages

# After passing on travis docker-based ci, sudo is no more
# used, ROOT_PATH is a env variable set in .travis.yml to avoid
# installing things system wide.
ROOT_PATH = os.getenv('ROOT_PATH', '/')

# Base dependencies (pinned for reproducibility)
install_requires = [
    "pyasn1>=0.1.7",
    "txAMQP>=0.7.0",
    "pyOpenSSL>=0.13",
    "twisted>=20.3.0",
    "pyparsing>=2.0.0",
    "python-dateutil>=2.0",
    "service_identity>=14.0.0",
    "lockfile>=0.10.0",
]

# Extra dependencies added in 0.9rc16
extras_require = {
    "celery": ["celery>=4.0.0"],
    "redis": ["redis>=2.10"],
    "requests": ["requests>=2.13.0"],
}

# Pre-installation checklist
if "install" in sys.argv:
    # 1. Check if jasmin user and group were created
    try:
        import pwd
        import grp
        pwd.getpwnam('jasmin')
        grp.getgrnam('jasmin')
    except KeyError:
        print('WARNING: jasmin user or group not found !')

    # 2. Check if system folders are created
    sysdirs = ['%s/etc/jasmin' % ROOT_PATH,
               '%s/etc/jasmin/resource' % ROOT_PATH,
               '%s/etc/jasmin/store' % ROOT_PATH,
               '%s/var/log/jasmin' % ROOT_PATH, ]
    for sysdir in sysdirs:
        if not os.path.exists(sysdir):
            print('WARNING: %s does not exist !' % sysdir)

    # 3. Check for permission to write jasmin.cfg in /etc/jasmin/store
    if not os.access('%s/etc/jasmin/store' % ROOT_PATH, os.W_OK):
        print('WARNING: %s/etc/jasmin/store must be writeable by the current user (%s)' % (
            ROOT_PATH, os.getenv('USER', 'unknown')))

    # 4. Check if sysdirs are owned by jasmin user
    for sysdir in sysdirs[3:]:
        if os.path.exists(sysdir):
            try:
                import pwd as pwd_mod
                if pwd_mod.getpwuid(os.stat(sysdir).st_uid).pw_name != 'jasmin':
                    print('WARNING: %s is not owned by jasmin user !' % sysdir)
            except Exception:
                pass

session = uuid.uuid1()

# Dynamically calculate the version based on jasmin.RELEASE.
release = __import__('jasmin').get_release()

setup(
    name="jasmin",
    version=release,
    author="Jookies LTD",
    author_email="jasmin@jookies.net",
    url="http://www.jasminsms.com",
    license="Apache v2.0",
    description=('Jasmin is a very complete open source SMS Gateway '
                 'with many enterprise-class features.'),
    long_description=open('README.rst', 'r').read(),
    keywords=['jasmin', 'sms', 'messaging', 'smpp', 'smsc', 'smsgateway'],
    packages=find_packages(),
    scripts=['jasmin/bin/jasmind.py', 'jasmin/bin/interceptord.py', 'jasmin/bin/dlrd.py', 'jasmin/bin/dlrlookupd.py'],
    include_package_data=True,
    install_requires=install_requires,
    tests_require=[
        "pytest>=7.0",
        "testfixtures>=3.0.0",
        "coverage>=4.0.3",
    ],
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    platforms='POSIX',
    data_files=[
        ('%s/etc/jasmin' % ROOT_PATH, ['misc/config/jasmin.cfg']),
        ('%s/etc/jasmin/resource' % ROOT_PATH, [
            'misc/config/resource/amqp0-8.stripped.rabbitmq.xml',
            'misc/config/resource/amqp0-9-1.xml'
        ],),
        ('%s/etc/jasmin/store' % ROOT_PATH, []),
    ],
)
