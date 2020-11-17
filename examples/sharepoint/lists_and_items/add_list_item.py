from settings import settings

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

credentials = UserCredential(settings['user_credentials']['username'],
                             settings['user_credentials']['password'])
ctx = ClientContext(settings['url']).with_credentials(credentials)

# connect to SP by list name
product_list = ctx.web.lists.get_by_title("product_list")

# provide a dictionary with column names as keys and values
product_list.add_item({
    "Title": "win2win",  # note, you can rename columns after they created but have to use name of initial column
    "version": "1",
    "build_date": "2020-11-17",
    "relative_url": "/test/path"})
ctx.execute_query()




