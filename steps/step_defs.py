from behave import step
from reusables.asserts import Assert

@step('user creates a new pet with "{category}", "{name}", "{tag}", and "{status}"')
def step_create_pet(context, category, name, tag, status):
    pet_data=context.client.generate_pet_data(category_name=category,pet_name=name,tag_name=tag,status=status)
    context.pet_data=pet_data
    context.response = context.client.add_pet(pet_data)

@step('user validates successful creation of pet')
def step_succesful_create_pet(context):
    response = context.response
    assert response.status_code == 200, f"Error: {response.status_code}"
    context.pet_id = response.json()['id']
    Assert.assert_equal_ignoring_keys(context.pet_data,response.json(),"id")

@step('user fetches the pet successfully')
def step_fetch_pet(context):
    response = context.client.get_pet(pet_id=context.pet_id)
    response_data = response.incoming_response
    assert response_data.status_code == 200, f"Error: {response_data.status_code}"
    Assert.assert_equal_ignoring_keys(context.pet_data,response_data.json(),"id")

# Step Definitions for Scenario: Update an existing pet
@step('user successfully updates an existing pet "{category}", "{name}", "{tag}", and "{status}"')
def step_update_pet(context, category, name, tag, status):
    pet_data=context.client.generate_pet_data(category_name=category,pet_name=name,tag_name=tag,status=status)
    context.pet_data=pet_data
    response = context.client.update_pet(pet_data)
    assert response.status_code == 200, f"Error: {response.status_code}"
    context.pet_id = response.json()['id']
    Assert.assert_equal_ignoring_keys(pet_data,response.json(),"id")

# Step Definitions for Scenario: Update an existing pet with form data
@step('user successfully updates an existing pet with form data "{name}" and "{status}"')
def step_update_pet_with_form(context, name, status):
    context.pet_data['name']=name
    context.pet_data['status']=status
    response = context.client.update_pet_with_form_data(pet_id=context.pet_id,name=name,status=status)
    assert response.status_code == 200, f"Error: {response.status_code}"


# Step Definitions for Scenario: Get pet by status
@step('user successfully fetches pet by status "{statuses}"')
def step_fetch_pet_by_status(context, statuses):
    list_status=statuses.split(',')
    response = context.client.find_by_status(list_status)
    response_data = response.incoming_response
    assert response_data.status_code == 200, f"Error: {response_data.status_code}"

    json_data=response_data.json()
    # Check that the response data size is greater than zero
    assert len(json_data) > 0, "Response data is empty"

    # Assert that the response data matches the expected model
    Pet = context.client.get_model('Pet')

    # Validate that each item in the response data is of type Pet
    for item in json_data:
        pet_instance = Pet._from_dict(item)
        assert isinstance(pet_instance, Pet), f"Response item is not a Pet model: {item}"

    print("All checks passed.")

@step('user deletes the pet successfully')
def step_delete_pet(context):
    response = context.client.delete_pet(pet_id=context.pet_id)
    assert response.status_code == 200, f"Error: {response.status_code}"

@step('user is not able to fetch the pet')
def step_fetch_pet_fail(context):
    response = context.client.get_pet(pet_id=context.pet_id)
    assert response.status_code == 404, f"Error: expected: 404 but got, {response.status_code}"

@step('user uploads an image "{file}" to the petstore')
def step_upload_image(context,file):
    response = context.client.upload_image(pet_id=1,meta_data='test',file_path=file)
    context.response=response

@step('image is successfully uploaded')
def step_success_200(context):
    response=context.response.incoming_response
    assert response.status_code == 200, f"Error: {response.status_code}"

@step('assert request failed {code}')
def step_fail_4xx(context,code):
    response=context.response.incoming_response
    assert response.status_code == code, f"Error: {response.status_code}"


  
