from settings import settings

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

credentials = UserCredential(settings['user_credentials']['username'],
                             settings['user_credentials']['password'])
ctx = ClientContext(settings['url']).with_credentials(credentials)

# connect to SP by list name
target_list = ctx.web.lists.get_by_title("Tasks")


# adding new Item
# provide a dictionary with column names as keys and values
target_list.add_item({
    "Title": "my_title",  # note, you can rename columns after they created but have to use name of initial column
    "version": "1",
    "build_date": "2020-11-17",
    "relative_url": "/test/path"})
ctx.execute_query()


# update Item property
item_to_update = target_list.get_item_by_id(54)
new_title = "Brand new title"
item_to_update.set_property('Title', new_title)
item_to_update.update()
ctx.execute_query()


# Move item to recycle bin.
# Remove when item property meets one of the conditions Title or version, version might be either 2 or 3
target_list.recycle_item_by_property({"Title": "my_title",
                                      "version": ["2", "3"]}, or_filter=True)

# Recycle when both conditions meet. Title is my_title and build_date is either "2020-11-17" or "2020-11-18"
target_list.recycle_item_by_property({"Title": "my_title",
                                      "build_date": ["2020-11-17", "2020-11-18"]}, or_filter=False)
ctx.execute_query()


# delete item by ID (will completely delete item)
target_item = target_list.get_item_by_id(54)
target_item.delete_object().execute_query()


# delete all items (will completely delete items)
result = target_list.items.get().execute_query()  # get existing items
for item in result:
    item.delete_object()
ctx.execute_batch()
