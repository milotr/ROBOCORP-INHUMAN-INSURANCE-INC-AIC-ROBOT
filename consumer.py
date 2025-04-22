import requests

from robocorp import workitems
from robocorp.tasks import task

@task
def consume_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System automation.
    Consumes traffic data work items.
    The consumer:

    -> loops all the work items one by one.
    -> validates the data.
    -> posts the data to the sales system API.
    -> handles successful responses.
    -> handles application exceptions.
    -> handles business exceptions.
    """
    # print("consume")
    # process_traffic_data()
    # refactoring process_traffic_data() function
    for item in workitems.inputs:
        traffic_data = item.payload["traffic_data"]
        # making sure the country code only contains 3 characters
        if len(traffic_data["country"]) == 3:
            status, return_json = post_traffic_data_to_sales_system(traffic_data)
            if status == 200:
                item.done()
            else:
                item.fail(
                    exception_type="APPLICATION",
                    code="TRAFFIC_DATA_POST_fAILED",
                    message=return_json["message"],
                )
        else:
            item.fail(exception_type="BUSINESS",
                        code="INVALID_COUNTRY_CODE",
                        message=item.payload,
                    )

def process_traffic_data():
    for item in workitems.inputs:
        traffic_data = item.payload["traffic_data"]
        # making sure the country code only contains 3 characters
        if len(traffic_data["country"]) == 3:
            status, return_json = post_traffic_data_to_sales_system(traffic_data)
            if status == 200:
                item.done()
            else:
                item.fail(
                    exception_type="APPLICATION",
                    code="TRAFFIC_DATA_POST_fAILED",
                    message=return_json["message"],
                )
        else:
            item.fail(exception_type="BUSINESS",
                      code="INVALID_COUNTRY_CODE",
                      message=item.payload,
                    )

def post_traffic_data_to_sales_system(traffic_data):
    url = "https://robocorp.com/inhuman-insurance-inc/sales-system-api"
    response = requests.post(url, json=traffic_data)
    # debug response
    # response.raise_for_status()
    return response.status_code, response.json()