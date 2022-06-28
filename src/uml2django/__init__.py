import sys

from uml2django.parsers.files.load_data_from_puml_or_xmi import load_data_from_puml_or_xmi

from .settings import settings
from .logger import _logger, setup_logging

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

def load_data_from(
    xmi_file_path: str = "",
    plantuml_file_path: str = ""
):
    setup_logging(settings.LOG_LEVEL)
    
    load_data_from_puml_or_xmi(
        xmi_file_path=xmi_file_path,
        plantuml_file_path=plantuml_file_path
    )