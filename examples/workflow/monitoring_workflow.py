import time
from examples.authentication import client
from intersight.api import compute_api
from intersight.api import workflow_api
import intersight
import sys
import argparse

api_key = "api_key"
api_key_file = "~/api_key_file_path"

api_client = client.get_api_client(api_key, api_key_file)


def monitor_workflow(workflow_monitoring_moid):
    """
    Function to monitor the workflow.
    :return: True if success , False if failure
    """

    # Creating the workflow instance api
    workflow_api_instance = workflow_api.WorkflowApi(api_client)

    flt_workflow_moid = "WorkflowCtx.InitiatorCtx.InitiatorMoid eq '{0}'\
     and Status eq 'RUNNING'".format(workflow_monitoring_moid)

    try:
        workflow_info_resp = workflow_api_instance.get_workflow_workflow_info_list(filter=flt_workflow_moid)
    except intersight.ApiException as e:
        print("Exception when calling WorkflowApi->: get_workflow_workflow_info_list %s" % e)
        sys.exit(1)

    retry = 150
    delay = 60

    if workflow_info_resp.results:
        workflow_moid = workflow_info_resp.results[0].moid
        while retry > 0:
            try:
                workflow_info_by_moid = workflow_api_instance.get_workflow_task_info_by_moid(moid=workflow_moid)
                if workflow_info_by_moid.status == "COMPLETED":
                    return True, ""
                elif workflow_info_by_moid.status == "FAILED":
                    return False, "########## FAIL : Workflow Failed ##########"
                else:
                    time.sleep(delay)
                    retry -= 1
            except intersight.ApiException as e:
                print("Exception when calling WorkflowApi->: get_workflow_task_info_by_moid %s" % e)
                sys.exit(1)
    else:
        return False, "Upgrade did not start. Please check on your compute node."


if __name__ == "__main__":
    # Users can pass moid of the initiated workflow as an argument.
    parser = argparse.ArgumentParser()
    parser.add_argument('--moid', required=True, help='Please provide the moid to monitor the workflow')
    args = parser.parse_args()

    if args.moid in [" ", "", None]:
        print("Please input a valid moid.")
        sys.exit(1)

    status, message = monitor_workflow(args.moid)
    if status:
        print(message)
    else:
        print(message)
        sys.exit(1)