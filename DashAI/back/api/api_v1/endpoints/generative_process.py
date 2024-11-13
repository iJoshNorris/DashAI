import logging

from fastapi import APIRouter, Depends, HTTPException, status
from huggingface_hub import HfApi, hf_hub_url, model_info
from kink import di
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

from DashAI.back.api.api_v1.schemas.generative_process_params import (
    GenerativeProcessParams,
)
from DashAI.back.dependencies.database.models import GenerativeModel, GenerativeProcess

router = APIRouter()
log = logging.getLogger(__name__)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_generative_process(
    params: GenerativeProcessParams,
    session_factory: sessionmaker = Depends(lambda: di["session_factory"]),
):
    """Create a new generative process.

    Parameters
    ----------
    params : GenerativeProcessParams
        The parameters of the new generative process, which includes the model name,
        parameters, process name and description.
    session_factory : Callable[..., ContextManager[Session]]
        A factory that creates a context manager that handles a SQLAlchemy session.
        The generated session can be used to access and query the database.

    Returns
    -------
    dict
        A dictionary with the new generative process on the database

    Raises
    ------
    HTTPException
        If there's an internal database error.
    """
    hugging_face_api = HfApi()

    with session_factory() as db:
        try:
            # Guardar modelo generativo en la base de datos (params.model_name) si
            # es que no existe en la base de datos
            # tiene que existir en la API de Hugging Face

            # Attempt to fetch model information
            model_information = hugging_face_api.model_info(params.model_name)
            generative_task = model_information.pipeline_tag
            task_to_model = {
                "text-generation": "TextGenerationModel",
                "text2text-generation": "TextGenerationModel",
                "text-to-image": "ImageGenerationModel",
            }

            model = GenerativeModel(
                name=params.model_name,
                generative_model=task_to_model[generative_task],
            )
            db.add(model)
            db.commit()
            db.refresh(model)
            model_id = model.id

        except Exception:
            # Falla pq el modelo generativo no existe
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Model does not exist or is not accessible.",
            )

        try:
            process = GenerativeProcess(
                model_id=model_id,
                input_data=params.input_data,
                parameters=params.parameters,
                name=params.name,
                description=params.description,
            )
            db.add(process)
            db.commit()
            db.refresh(process)
            return process
        except exc.SQLAlchemyError as e:
            log.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal database error",
            ) from e
