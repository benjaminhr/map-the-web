import json

# {
#   "https://fb.com": {
#     "children": [
#       "https://de-de.facebook.com/",
#       "https://developers.facebook.com/",
#       "https://fr-fr.facebook.com/",
#       "https://lt-lt.facebook.com/",
#       "https://messenger.com/",
#       "https://pl-pl.facebook.com/",
#       {
#         "https://www.facebook.com/": {
#           "children": [
#             "https://www.facebook.com/recover/initiate"
#           ]
#         }
#       },
#       "https://www.facebook.com/help/2687943754764396",
#       "https://zh-cn.facebook.com/"
#     ]
#   }
# }

# {
# 	url: 'google.com',
# 	children: [{
# 		url: 'Child One',
#     children: [{}, {}, {}]      
# 	}]
# }

def fix_tree(json_tree):
  json_dict = json.loads(json_tree)

  

