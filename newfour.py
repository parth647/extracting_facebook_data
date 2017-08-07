import os
import json
import facebook
import requests
from argparse import ArgumentParser

def get_parser():
     parser = ArgumentParser()
     parser.add_argument('--page')
     parser.add_argument('--n',default=100,type=int)
     return parser

if __name__ == '__main__':
     parser = get_parser()
     args = parser.parse_args()

     token = os.environ.get('FACEBOOK_TEMP_TOKEN')
     graph = facebook.GraphAPI(token)

     all_fields = ['id','message','created_time','shares','likes.summary(true)','comments.summary(true)']
     all_fields = ',' .join(all_fields)
     posts = graph.get_connections('dardanaak','posts',fields=all_fields)
     downloaded = 0
     while True:

         if downloaded >= args.n:
             break
         try:
             fname = 'posts_{}.json1'.format(args.page)
             with open(fname,'a') as f:

                 for post in posts['data']:
                     downloaded += 1
                     f.write(json.dumps(post)+"\n")

                 posts = requests.get(posts['paging']['next']).json()
         except KeyError:
              break
