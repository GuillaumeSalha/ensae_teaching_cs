"""
@file
@brief Shortcuts for automation
"""

from .jenkins_helper import setup_jenkins_server, default_jenkins_jobs
from .ftp_publish_helper import publish_documentation, publish_teachings_to_web
from .notebook_test_helper import execute_notebooks
from .modules_documentation import rst_table_modules
from .module_backup import ftp_list_modules
