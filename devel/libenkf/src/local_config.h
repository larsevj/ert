#ifndef __LOCAL_CONFIG_H__
#define __LOCAL_CONFIG_H__

#include <local_updatestep.h>
#include <local_ministep.h>
#include <log.h>


typedef enum {
  INVALID_CMD                     = 0,  /* MArks EOF */
  CREATE_UPDATESTEP               = 1,  /* UPDATESTEP_NAME                   ->     local_config_alloc_updatestep(); */
  CREATE_MINISTEP                 = 2,  /* MINISTEP_NAME                     ->     local_config_alloc_ministep();   */
  ATTACH_MINISTEP                 = 3,  /* UPDATESTEP_NAME , MINISTEP_NAME   ->     local_updatestep_add_ministep(); */
  ADD_DATA                        = 5,  /* DATA_KEY                          ->     local_ministep_add_node();       */
  ADD_OBS                         = 4,  /* OBS_KEY                           ->     local_ministep_add_obs();        */
  ACTIVE_LIST_ADD_OBS_INDEX       = 7,  /* OBS_KEY , ACTIVE_INDEX            */
  ACTIVE_LIST_ADD_DATA_INDEX      = 8,  /* DATA_KEY , ACTIVE_INDEX           */
  ACTIVE_LIST_ADD_MANY_OBS_INDEX  = 9,  /* OBS_KEY , NUM_INDEX , INDEX1, INDEX2, INDEX3,... */
  ACTIVE_LIST_ADD_MANY_NODE_INDEX = 10, /* DATA_KEY , NUM_INDEX , INDEX1 , INDEX2 , INDEX3 ,... */  
  INSTALL_UPDATESTEP              = 11, /* UPDATESTEP_NAME , STEP1 , STEP2          local_config_set_updatestep() */
  INSTALL_DEFAULT_UPDATESTEP      = 12, /* UPDATETSTEP_NAME                         local_config_set_default_updatestep() */
  ALLOC_MINISTEP_COPY             = 13, /* SRC_NAME TARGET_NAME */ 
  DEL_DATA                        = 14, /* MINISTEP KEY*/
  DEL_OBS                         = 15  /* MINISTEP OBS_KEY */
} local_config_instruction_type; 




#define CREATE_UPDATESTEP_STRING                "CREATE_UPDATESTEP"
#define CREATE_MINISTEP_STRING                  "CREATE_MINISTEP"
#define ATTACH_MINISTEP_STRING                  "ATTACH_MINISTEP"
#define ADD_DATA_STRING                         "ADD_DATA"
#define ADD_OBS_STRING                          "ADD_OBS"      
#define ACTIVE_LIST_ADD_OBS_INDEX_STRING        "ACTIVE_LIST_ADD_OBS_INDEX"
#define ACTIVE_LIST_ADD_DATA_INDEX_STRING       "ACTIVE_LIST_ADD_DATA_INDEX"
#define ACTIVE_LIST_ADD_MANY_OBS_INDEX_STRING   "ACTIVE_LIST_ADD_MANY_OBS_INDEX"
#define ACTIVE_LIST_ADD_MANY_NODE_INDEX_STRING  "ACTIVE_LIST_ADD_MANY_NODE_INDEX"
#define INSTALL_UPDATESTEP_STRING               "INSTALL_UPDATESTEP"
#define INSTALL_DEFAULT_UPDATESTEP_STRING       "INSTALL_DEFAULT_UPDATESTEP"
#define ALLOC_MINISTEP_COPY_STRING              "COPY_MINISTEP"
#define DEL_DATA_STRING                         "DEL_DATA"
#define DEL_OBS_STRING                          "DEL_OBS"






typedef struct local_config_struct local_config_type;

local_config_type     	    * local_config_alloc( int history_length );
void                  	      local_config_free( local_config_type * local_config );

local_updatestep_type 	    * local_config_alloc_updatestep( local_config_type * local_config , const char * key );
local_ministep_type   	    * local_config_alloc_ministep( local_config_type * local_config , const char * key );
local_ministep_type         * local_config_alloc_ministep_copy( local_config_type * local_config , const char * src_key , const char * new_key);
void                  	      local_config_set_default_updatestep( local_config_type * local_config , const char * default_key);
const local_updatestep_type * local_config_iget_updatestep( const local_config_type * local_config , int index);
local_updatestep_type       * local_config_get_updatestep( const local_config_type * local_config , const char * key);
local_ministep_type         * local_config_get_ministep( const local_config_type * local_config , const char * key);
void                          local_config_set_updatestep(local_config_type * local_config, int step1 , int step2 , const char * key);
void                          local_config_load( local_config_type * local_config /*const ensemble_config_type * ensemble_config , const enkf_obs_type * enkf_obs , */ , const char * config_file , log_type * logh);
const char                  * local_config_get_cmd_string( local_config_instruction_type cmd );


#endif
