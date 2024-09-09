import logging
from behave import step
from reusables.asserts import Assert

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@step('user creates a new pet with "{category}", "{name}", "{tag}", and "{status}"')
def step_create_pet(context, category, name, tag, status):
    logger.info(f"Creating a new pet with category: {category}, name: {name}, tag: {tag}, status: {status}")
    pet_data = context.client.generate_pet_data(category_name=category, pet_name=name, tag_name=tag, status=status)
    context.pet_data = pet_data
    context.response = context.client.add_pet(pet_data)
    logger.info(f"Pet creation response: {context.response}")

@step('user validates successful creation of pet')
def step_successful_create_pet(context):
    response = context.response
    logger.info(f"Validating pet creation. Response status code: {response.status_code}")
    assert response.status_code == 200, f"Error: {response.status_code}"
    context.pet_id = response.json()['id']
    Assert.assert_equal_ignoring_keys(context.pet_data, response.json(), "id")
    logger.info("Pet creation validation passed")

@step('user fetches the pet successfully')
def step_fetch_pet(context):
    logger.info(f"Fetching pet with ID: {context.pet_id}")
    response = context.client.get_pet(pet_id=context.pet_id)
    response_data = response.incoming_response
    logger.info(f"Fetch pet response status code: {response_data.status_code}")
    assert response_data.status_code == 200, f"Error: {response_data.status_code}"
    Assert.assert_equal_ignoring_keys(context.pet_data, response_data.json(), "id")
    logger.info("Pet fetch validation passed")

@step('user successfully updates an existing pet "{category}", "{name}", "{tag}", and "{status}"')
def step_update_pet(context, category, name, tag, status):
    logger.info(f"Updating existing pet with category: {category}, name: {name}, tag: {tag}, status: {status}")
    pet_data = context.client.generate_pet_data(category_name=category, pet_name=name, tag_name=tag, status=status)
    context.pet_data = pet_data
    response = context.client.update_pet(pet_data)
    logger.info(f"Pet update response status code: {response.status_code}")
    assert response.status_code == 200, f"Error: {response.status_code}"
    context.pet_id = response.json()['id']
    Assert.assert_equal_ignoring_keys(pet_data, response.json(), "id")
    logger.info("Pet update validation passed")

@step('user successfully updates an existing pet with form data "{name}" and "{status}"')
def step_update_pet_with_form(context, name, status):
    logger.info(f"Updating existing pet with form data. Name: {name}, Status: {status}")
    context.pet_data['name'] = name
    context.pet_data['status'] = status
    response = context.client.update_pet_with_form_data(pet_id=context.pet_id, name=name, status=status)
    logger.info(f"Pet update with form response status code: {response.status_code}")
    assert response.status_code == 200, f"Error: {response.status_code}"
    logger.info("Pet update with form data validation passed")

@step('user successfully fetches pet by status "{statuses}"')
def step_fetch_pet_by_status(context, statuses):
    logger.info(f"Fetching pets by status: {statuses}")
    list_status = statuses.split(',')
    response = context.client.find_by_status(list_status)
    response_data = response.incoming_response
    logger.info(f"Fetch pets by status response status code: {response_data.status_code}")
    assert response_data.status_code == 200, f"Error: {response_data.status_code}"

    json_data = response_data.json()
    assert len(json_data) > 0, "Response data is empty"
    Pet = context.client.get_model('Pet')

    for item in json_data:
        pet_instance = Pet._from_dict(item)
        assert isinstance(pet_instance, Pet), f"Response item is not a Pet model: {item}"

    logger.info("All pets fetched by status validation passed")

@step('user deletes the pet successfully')
def step_delete_pet(context):
    logger.info(f"Deleting pet with ID: {context.pet_id}")
    response = context.client.delete_pet(pet_id=context.pet_id)
    logger.info(f"Pet deletion response status code: {response.status_code}")
    assert response.status_code == 200, f"Error: {response.status_code}"
    logger.info("Pet deletion validation passed")

@step('user is not able to fetch the pet')
def step_fetch_pet_fail(context):
    logger.info(f"Attempting to fetch pet with ID: {context.pet_id} expecting a failure")
    response = context.client.get_pet(pet_id=context.pet_id)
    logger.info(f"Fetch pet response status code: {response.status_code}")
    assert response.status_code == 404, f"Error: expected: 404 but got: {response.status_code}"
    logger.info("Fetch pet failure validation passed")

@step('user uploads an image "{file}" to the petstore')
def step_upload_image(context, file):
    logger.info(f"Uploading image to petstore. File path: {file}")
    response = context.client.upload_image(pet_id=1, meta_data='test', file_path=file)
    context.response = response
    logger.info(f"Image upload response: {response}")

@step('image is successfully uploaded')
def step_success_200(context):
    response = context.response.incoming_response
    logger.info(f"Validating image upload. Response status code: {response.status_code}")
    assert response.status_code == 200, f"Error: {response.status_code}"
    logger.info("Image upload validation passed")

@step('user creates a new pet with invalid data')
def creates_with_invalid_data(context):
    logger.info("Creating a new pet with invalid data")
    pet_data = context.client.generate_invalid_pet_data()
    context.exception = context.client.add_pet(pet_data)
    logger.info(f"Pet creation with invalid data response: {context.exception}")

@step('user asserts request failed with message "{exp_message}"')
def step_fail_4xx(context, exp_message):
    e = context.exception
    logger.info(f"Asserting failure with expected message: {exp_message}")
    assert e.message == exp_message, f"Expected: {exp_message}, but got: {e.message}"
    logger.info("Failure assertion passed")
