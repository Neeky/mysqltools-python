from distutils.core import setup

olds_scripts = ['bin/mtlsmonitor','bin/mtlsbackup','bin/mtlslog','bin/mtlsanalysis',
               'bin/mtlshttp','bin/mtlsbigfiles','bin/mtlsdeleterows']

news_scripts = ['bin/mtls-big-files','bin/mtls-delete-rows','bin/mtls-file-truncate',
                'bin/mtls-http','bin/mtls-log','bin/mtls-monitor','bin/mtls-backup']

scripts = olds_scripts + news_scripts

setup(name='mysqltools-python',
      version='2.19.07.28',
      scripts=scripts,
      packages=['mtls','mtls.kits'],
      maintainer='Neeky',
      maintainer_email='neeky@live.com',
      url='https://github.com/Neeky/mysqltools-python',
      install_requires=['mysql-connector-python>=8.0.12'],
      python_requires='>=3.1.*,'
      )


      
