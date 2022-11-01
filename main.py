import asyncio
import e621py_wrapper as e621


async def download(ident, cat):
    print(f'Downloading post {ident} in category {cat}...')
    api.util.save(ident, f"{cat.replace('/', ' ')}/")
    print('done')


async def uncategorized_download(ident):
    print(f'Downloading post {ident}, uncategorized...')
    api.util.save(ident, "Uncategorized/")
    print('done')


async def download_pool(pool_id):
    pool = api.pools.get(pool_id)
    for ident in pool[0]['post_ids']:
        print(f'Downloading post {ident} from pool {pool[0]["name"]}...')
        api.util.save(ident, f"{pool[0]['name'].replace('/', ' ')}")
        print('done')
    print(f'Done downloading pool {pool[0]["name"]}')


async def main():
    async with asyncio.TaskGroup() as tg:
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
                tg.create_task(download_pool(pool_id))
                pool_downloaded_list.append(pool_id)
            if not pool_download:
                match = None
                for tag in all_tags:
                    for category in categories:
                        if tag == category:
                            match = category
                if match is not None:
                    tg.create_task(download(post['id'], match))
                else:
                    tg.create_task(uncategorized_download(post['id']))


try:
    api = e621.client()
    pool_downloaded_list = []
#    api.login('username', 'api key')
    posts = api.posts.search(input('What do you want to fuck today? '), '', 1000)
    categories = input('What would you like to categorize? ')
    categories = categories.split()
    downloader = set()
    rate = int(input('What will the rating threshold be? '))
    for post_rate in posts:
        if post_rate['score']['total'] < rate:
            posts.remove(post_rate)
except ValueError:
    print('You should have put in a number. Crashing!')
    exit(69)
asyncio.run(main())
print('Downloads done.')
