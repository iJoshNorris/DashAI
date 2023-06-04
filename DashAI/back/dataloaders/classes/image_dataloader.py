from datasets import DatasetDict, Image, load_dataset
from fastapi import UploadFile

from DashAI.back.dataloaders.classes.dataloader import BaseDataLoader


class ImageDataLoader(BaseDataLoader):
    """Data loader for data from image files."""

    def load_data(
        self, dataset_path: str, file: UploadFile = None, url: str = None
    ) -> DatasetDict:
        """
        Load image data uploaded in a zip file in a DatasetDict.

        Args:
            dataset_path (str): Path of the folder with the dataset files.
            file (UploadFile, optional): File uploaded.
                It's optional because is not necessary if dataset is uploaded in a URL.

            url (str, optional): For load the dataset from an URL.
                It's optional because is not necessary if dataset is uploaded in files.

        Returns
        -------
            DatasetDict: Dataset loaded in Hugging Face format.
        -------------------------------------------------------------------------------
        - NOTE: For image data, the original files are saved in "/files" folder and
                the DatasetDict should have only the path to the images in "/files"
                If decode is True, data is duplicated in DatasetDict as a PIL object.

                More information: https://huggingface.co/docs/datasets/image_load
        -------------------------------------------------------------------------------
        """
        if not isinstance(dataset_path, str):
            raise TypeError(
                f"dataset_path should be a string, got {type(dataset_path)}"
            )
        if not isinstance(file, UploadFile):
            raise TypeError(
                f"file should be an uploaded file from user, got {type(file)}"
            )
        if not isinstance(url, str):
            raise TypeError(
                f"url should be a string with a web site adress, got {type(url)}"
            )

        if url:
            dataset = load_dataset("imagefolder", data_files=url).cast_column(
                "image",
                Image(decode=False),
            )
        elif file:
            if file.content_type == "application/zip":
                files_path = self.extract_files(dataset_path, file)
                dataset = load_dataset("imagefolder", data_dir=files_path).cast_column(
                    "image",
                    Image(decode=False),
                )
            else:
                raise Exception("For image data is necessary a zip file.")
        return dataset
