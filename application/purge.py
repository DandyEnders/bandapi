from bandapi import client
import pandas as pd
import time


def delete_all_comments(band_key, user_key):
    c = client.APIClient()
    
    for post_df, _after in c.get_posts(band_key, limit=None):
        for post in post_df.itertuples():
            post_key = post.post_key
            try:
                post.latest_comments
            except AttributeError:
                pass
            else:
                comments = c.get_comments(band_key, post_key)
                for i, comment in enumerate(comments['items']):
                    if comment['author']['user_key'] == user_key:
                        res = c.delete_comment(band_key,
                                               post_key,
                                               comment['comment_key'])
                        msg = res['message']
                        if msg == 'success':
                            print(f'Deleted comment {comment["content"]}')
                        else:
                            print(
                                f'Failed to delete comment {comment["content"]},')
                            print(f'reason: {msg}')
                        if i < (len(comments['items'])):
                            time.sleep(10.1)
    """
    Tried to make all posts / comment remover, but
    turns out that posts written on the web cannot be deleted using api.
    
    for post_df, _after in c.get_posts(band_key, limit=None):
        for post in post_df.itertuples():
            post_key = post.post_key
            if post.author['user_key'] == user_key:
                print(band_key, post_key)
                res = c.delete_post(band_key, post_key)
                msg = res['message']
                if msg == 'success':
                    print(f'Deleted post {post.content}')
                else:
                    print(
                        f'Failed to delete post {post.content},\nreason: {res}')
                time.sleep(10.1)
            else:
                try:
                    post.latest_comments
                except AttributeError:
                    pass
                else:
                    comments = c.get_comments(band_key, post_key)
                    for comment in comments['items']:
                        if comment['author']['user_key'] == user_key:
                            res = c.delete_comment(band_key,
                                                post_key,
                                                comment['comment_key'])
                            msg = res['message']
                            if msg == 'success':
                                print(f'Deleted comment {comment["content"]}')
                            else:
                                print(
                                    f'Failed to delete comment {comment["content"]},')
                                print(f'reason: {msg}')
                        time.sleep(10.1)
    """


if __name__ == "__main__":
    uk = ''
    bk = ''
    
    print('Start deleting all comments')
    delete_all_comments(bk, uk)
    print('Finished deleting all comments')