from bravado.client import SwaggerClient
from bravado.swagger_model import load_file
from bravado.requests_client import RequestsClient
from bravado.exception import HTTPError

from enum import Enum
import itertools    

class SwaggerClientBase:
    def __init__(self, swagger_url):
        http_client= RequestsClient()
        http_client.set_api_key('https://petstore.swagger.io/','special-key')
        self.id=next(itertools.count())
        self.pet_status_values = ['available', 'pending', 'sold']
        self.headers = {
            'api_key': 'special-key',
        }
        # config = {
        #     'validate_responses': False,  # Disable response validation
        #     'also_return_response': True,  # Return both the response and result
        #     'use_models': False
        # }
        self.client = SwaggerClient.from_url(spec_url=swagger_url,http_client=http_client)

    def get_model(self,model):
        """
            returns the model       
        """
        return self.client.get_model(model_name=model)

    def generate_pet_data(self, category_name, pet_name, tag_name, status):
        """
        Generates test data for the pet based on Swagger spec.
        """
        pet_data = {
            "id": self.id,
            "category": {"id": 0, "name": category_name},
            "name": pet_name,
            "photoUrls": ["http://example.com/photo.jpg"],
            "tags": [{"id": 0, "name": tag_name}],
            "status": status
        }
        return pet_data
    

    def add_pet(self, pet_data):
        """
        Calls the 'addPet' endpoint and returns the response.
        """
        try:
            response = self.client.pet.addPet(body=pet_data).response()
            return response
        except HTTPError as e:
            print(f"HTTPError: {e}")
            # Handle or log the error as needed
            return e.response

    def get_pet(self, pet_id):
        """
        Calls the 'getPetById' endpoint and returns the pet data.
        """
        try:
            response = self.client.pet.getPetById(petId=pet_id).response()
            return response
        except HTTPError as e:
            print(f"HTTPError: {e}")
            # Handle or log the error as needed
            return e.response

    def update_pet(self, pet_data):
        """
        Calls the 'updatePet' endpoint to update pet details.
        """
        try:
            response = self.client.pet.updatePet(body=pet_data).response()
            return response
        except HTTPError as e:
            print(f"HTTPError: {e}")
            # Handle or log the error as needed
            return e.response

    def delete_pet(self, pet_id):
        """
        Calls the 'deletePet' endpoint and returns the response.
        """
        try:
            response = self.client.pet.deletePet(petId=pet_id).response()
            return response
        except HTTPError as e:
            print(f"HTTPError: {e}")
            # Handle or log the error as needed
            return e.response    
        
    def upload_image(self, pet_id, meta_data=None, file_path=None):
        """
        Calls the 'uploadImage' endpoint and returns the response.
        
        :param pet_id: ID of the pet to associate the image with.
        :param meta_data: Additional metadata for the upload (optional).
        :param file_path: Path to the file that will be uploaded.
        """
        try:
            # Open the file in binary mode for uploading (as file upload requires binary format)
            with open(file_path, 'rb') as file:
                response = self.client.pet.uploadFile(
                    petId=pet_id,
                    additionalMetadata=meta_data,
                    file=file
                ).response()

            return response

        except Exception as e:
            print(f"Error during file upload: {e}")
            raise

    
    def find_by_status(self,statuses:list):
        """
        Fetches pets by the provided status values with validation
        Raises ValueError if any invalid stauts is passed
        """
        invalid_statuses = [status for status in statuses if status not in self.pet_status_values]
        if invalid_statuses:
            raise ValueError(f"TestData Error: invalid status value(s): {invalid_statuses}. Allowed values are: {self.pet_status_values}")
        response = self.client.pet.findPetsByStatus(status=list(statuses)).response()
        return response
    
    def update_pet_with_form_data(self,pet_id,name,status):
        """
        Updates a pet's information using form data.

        This method sends a request to update a pet's name and status based on the given `pet_id`.
        It updates the details of an existing pet in the store using form parameters as specified in
        the Swagger Pet Store API.

        Args:
            pet_id (int): The ID of the pet to be updated.
            name (str): The new name of the pet. Can be an empty string if no update is needed.
            status (str): The new status of the pet (e.g., 'available', 'pending', 'sold').
                        It must be one of the valid status values according to the API's enum.
        """
        try:
            response=self.client.pet.updatePetWithForm(
                petId=pet_id,
                name=name,
                status=status
                ).response()
            return response
        except HTTPError as e:
            print(f"HTTPError: {e}")
            # Handle or log the error as needed
            return e.response        

