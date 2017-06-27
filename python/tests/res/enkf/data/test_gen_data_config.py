from ecl.test import ExtendedTestCase
from ecl.util import BoolVector
from res.test import ErtTestContext

from res.enkf.data import EnkfNode
from res.enkf.config import GenDataConfig
from res.enkf import EnkfPrototype
from res.enkf import NodeId
from res.enkf import ForwardLoadContext


class GenDataConfigTest(ExtendedTestCase):
    _get_active_mask    = EnkfPrototype("bool_vector_ref gen_data_config_get_active_mask( gen_data_config )", bind = False)
    _update_active_mask = EnkfPrototype("void gen_data_config_update_active( gen_data_config, forward_load_context , bool_vector)", bind = False)
    _alloc_run_arg      = EnkfPrototype("run_arg_obj run_arg_alloc_ENSEMBLE_EXPERIMENT( char*, enkf_fs , int , int , char*) ", bind = False)

    def setUp(self):
        self.config_file = self.createTestPath("Statoil/config/with_GEN_DATA/config")

    def load_active_masks(self, case1, case2 ):
        with ErtTestContext("gen_data_config_test", self.config_file) as test_context:
            ert = test_context.getErt()

            fs1 =  ert.getEnkfFsManager().getFileSystem(case1)
            config_node = ert.ensembleConfig().getNode("TIMESHIFT")
            data_node = EnkfNode(config_node)
            data_node.tryLoad(fs1, NodeId(60, 0))

            active_mask = self._get_active_mask( config_node.getDataModelConfig() )
            first_active_mask_length = len(active_mask)
            self.assertEqual(first_active_mask_length, 2560)

            fs2 =  ert.getEnkfFsManager().getFileSystem(case2)
            data_node = EnkfNode(config_node)
            data_node.tryLoad(fs2, NodeId(60, 0))

            active_mask = self._get_active_mask( config_node.getDataModelConfig() )
            second_active_mask_len = len(active_mask)
            self.assertEqual(second_active_mask_len, 2560)
            self.assertEqual(first_active_mask_length, second_active_mask_len)

            # Setting one element to False, load different case, check, reload, and check.
            self.assertTrue(active_mask[10])
            active_mask_modified = active_mask.copy()
            active_mask_modified[10] = False

            self.updateMask(config_node.getDataModelConfig(),  60, fs2 , active_mask_modified)
            active_mask = self._get_active_mask( config_node.getDataModelConfig() )
            self.assertFalse(active_mask[10])

            #Load first - check element is true
            data_node = EnkfNode(config_node)
            data_node.tryLoad(fs1, NodeId(60, 0))
            active_mask = self._get_active_mask( config_node.getDataModelConfig() )
            self.assertTrue(active_mask[10])

            # Reload second again, should now be false at 10, due to the update further up
            data_node = EnkfNode(config_node)
            data_node.tryLoad(fs2, NodeId(60, 0))
            active_mask = self._get_active_mask( config_node.getDataModelConfig() )
            self.assertFalse(active_mask[10])


    def test_loading_two_cases_with_and_without_active_file(self):
        self.load_active_masks("missing-active", "default")



    def test_create(self):
        conf = GenDataConfig("KEY")

    def updateMask(self, gen_data_config , report_step , fs, active_mask):
        run_arg = self._alloc_run_arg( "run_id", fs , 0 , 0 , "Path")
        load_context = ForwardLoadContext( run_arg = run_arg , report_step = report_step )
        self._update_active_mask( gen_data_config , load_context , active_mask )
