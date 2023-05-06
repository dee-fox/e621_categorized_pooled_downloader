import e621py_wrapper as e621


def download(ident, cat):
    print(f'Downloading post {ident} in category {cat}...')
    better_cat = cat.replace('/', ' slash ')
    better_cat = better_cat.replace('_', ' ')
    api.util.save(ident, f"{better_cat}/")
    print('Done')


def uncategorized_download(ident):
    print(f'Downloading post {ident}, uncategorized...')
    api.util.save(ident, "uncategorized/")
    print('done')


def download_pool(pool_id):
    pool = api.pools.get(pool_id)
    for ident in pool[0]['post_ids']:
        print(f'Downloading post {ident} from pool {pool[0]["name"]}...')
        api.util.save(ident, f"{pool[0]['name'].replace('/', ' ')}")
        print('done')
    print(f'Done downloading pool {pool[0]["name"]}')


def main():
    for post in posts:
       all_tags = post['tags']['artist'] + post['tags']['general'] + post['tags']['species'] + post['tags']['character'] + post['tags']['copyright'] + post['tags']['lore'] + post['tags']['invalid'] + post['tags']['meta']
       pool_download = False
       for pool_id in post['pools']:
           pool_download = True
           new_pool = True
           for pools in pool_downloaded_list:
               if pools == pool_id:
                   new_pool = False
           if not new_pool:
               break
           download_pool(pool_id)
           pool_downloaded_list.append(pool_id)
       if not pool_download:
            match = None
            for tag in all_tags:
                for category in categories:
                    if tag == category:
                        match = category
            if match is not None:
                download(post['id'], match)
            else:
                uncategorized_download(post['id'])



api = e621.client()
pool_downloaded_list = []
# api.login('username', 'api key')
posts = api.posts.search(input('Search query: '), '', 1000)
categories = input('Categories: ')
categories = categories.split()
downloader = set()
rate_set = False
while not rate_set:
    try:
        rate = int(input('Rating threshold: '))
        rate_set = True
    except ValueError:
        rate_set = False
for post_rate in posts:
    if post_rate['score']['total'] < rate:
        posts.remove(post_rate)
main()    #leftover!
print('Downloads done.')
