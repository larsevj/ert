import os
from argparse import Namespace

import pytest

from ert.cli.workflow import execute_workflow
from ert.config import ErtConfig
from ert.enkf_main import EnKFMain
from ert.shared.plugins.plugin_manager import ErtPluginContext


@pytest.mark.usefixtures("copy_poly_case")
def test_executing_workflow(storage):
    with ErtPluginContext():
        with open("test_wf", "w", encoding="utf-8") as wf_file:
            wf_file.write("EXPORT_RUNPATH")

        config_file = "poly.ert"
        with open(config_file, "a", encoding="utf-8") as file_handle:
            file_handle.write("LOAD_WORKFLOW test_wf")

        rc = ErtConfig.from_file(config_file)
        ert = EnKFMain(rc)
        args = Namespace(name="test_wf")
        # pylint: disable=no-member
        # (pylint not able to verify contents of Namespace)
        execute_workflow(ert, storage, args.name)
        assert os.path.isfile(".ert_runpath_list")
