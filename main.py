import e621py_wrapper as e621


def download(ident, cat, par):
    if par:
        print(f'Downloading post {ident}, the child of {cat}')
    else:
        print(f'Downloading post {ident} in category {cat}...')
        cat = cat.replace('/', ' slash ')
        cat = cat.replace('_', ' ')
    api.util.save(ident, f"{cat}/")
    post_downloaded_list.append(ident)
    print('Done')


def uncategorized_download(ident):
    print(f'Downloading post {ident}, uncategorized...')
    api.util.save(ident, "uncategorized/")
    post_downloaded_list.append(ident)
    print('Done')


def download_pool(pool_id):
    pool = api.pools.get(pool_id)
    for ident in pool[0]['post_ids']:
        print(f'Downloading post {ident} from pool {pool[0]["name"]}...')
        api.util.save(ident, f"{pool[0]['name'].replace('/', ' ')}")
        post_downloaded_list.append(ident)
        print('Done')
    pool_downloaded_list.append(pool_id)
    print(f'Done downloading pool {pool[0]["name"]}')


def main():
    for post in posts:
        new_post = True
        for dumb in post_downloaded_list:
            if dumb == post['id']:
                new_post = False
        if not new_post:
            break
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
        if post['relationships']['parent_id'] is not None or not post['relationships']['has_children']:
            if not pool_download:
                match = None
                for tag in all_tags:
                    for category in categories:
                        if tag == category:
                            match = category
                if match is not None:
                    download(post['id'], match, False)
                else:
                    uncategorized_download(post['id'])
        elif post['relationships']['has_children'] or post['relationships']['parent_id'] is not None:
            match = post['id']
            if post['relationships']['parent_id'] is not None:
                posts.append(api.posts.get(post['relationships']['parent_id']))
                match = post['relationships']['parent_id']
            for child in api.posts.get(post['relationships']['children']):
                posts.append(child)
            download(post['id'], match, True)


api = e621.client()
pool_downloaded_list = []
post_downloaded_list = []
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
main()    # leftover!
print('Downloads done.')
