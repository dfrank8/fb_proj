from dynamo_helper import Dynamo_Wrapper

import pdb
FB_APP_ID = '1462100957178030'

dynamo_drafts = Dynamo_Wrapper(table_name ='drafts', primary_key = 'app_id')

pdb.set_trace()

dynamo_drafts.delete_draft(FB_APP_ID,0)