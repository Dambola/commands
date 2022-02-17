from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

from azure.devops.v5_1.work_item_tracking.models import Wiql

# Fill in with your personal access token and org URL
personal_access_token = 'l2fpamq4s2qhiv4lm73tdf67l5ux5demajsh3hqmldmctkogijjq'
organization_url = 'https://dev.azure.com/danielnreboucas'

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# # Get a client (the "core" client provides access to projects, teams, etc)
# core_client = connection.clients.get_core_client()

# # Get the first page of projects
# get_projects_response = core_client.get_projects()
# index = 0
# while get_projects_response is not None:
#     for project in get_projects_response.value:
#         print("[" + str(index) + "] " + project.name)
#         index += 1
#     if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
#         # Get the next page of projects
#         get_projects_response = core_client.get_projects(continuation_token=get_projects_response.continuation_token)
#     else:
#         # All projects have been retrieved
#         get_projects_response = None

def get_tasks_from_iteration_path(connection, iteration_path):
    wit_client = connection.clients.get_work_item_tracking_client()
    wiql = Wiql(
        query="""
        select [System.Id],
            [System.WorkItemType],
            [System.Title],
            [System.State],
            [System.AreaPath],
            [System.IterationPath],
            [System.Tags]
        from WorkItems
        where [System.IterationPath] == '%s'
        and [System.WorkItemType] == 'Task'
        order by [System.ChangedDate] desc""" % iteration_path
    )

    # We limit number of results to 30 on purpose
    wiql_results = wit_client.query_by_wiql(wiql, top=30).work_items
    if wiql_results:

        # WIQL query gives a WorkItemReference with ID only
        # => we get the corresponding WorkItem from id
        work_items = (
            wit_client.get_work_item(int(res.id)) for res in wiql_results
        )

        for work_item in work_items:
            print(work_item)

get_tasks_from_iteration_path(connection, 'LeWi\\Sprint 1')