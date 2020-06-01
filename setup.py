from distutils.core import setup

olds_scripts = ['bin/mtlsmonitor', 'bin/mtlsbackup', 'bin/mtlslog', 'bin/mtlsanalysis',
                'bin/mtlshttp', 'bin/mtlsbigfiles', 'bin/mtlsdeleterows']

news_scripts = ['bin/mtls-big-files', 'bin/mtls-delete-rows', 'bin/mtls-file-truncate',
                'bin/mtls-http', 'bin/mtls-log', 'bin/mtls-monitor', 'bin/mtls-backup',
                'bin/mtls-perf-bench', 'bin/mtls-kill-all-conections', 'bin/mtls-sql-distribution',
                'bin/mtls-file-stat', 'bin/mtls-expired-tables', 'bin/mtls-sql-playback', 'bin/mtls-random-passwd']

scripts = olds_scripts + news_scripts

setup(name='mysqltools-python',
      version='2.20.06.01',
      scripts=scripts,
      packages=['mtls', 'mtls.kits'],
      maintainer='Neeky',
      maintainer_email='neeky@live.com',
      url='https://github.com/Neeky/mysqltools-python',
      )
