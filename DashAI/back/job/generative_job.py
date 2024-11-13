import logging
from typing import Any

from kink import inject
from sqlalchemy import exc
from sqlalchemy.orm import Session

from DashAI.back.dependencies.database.models import GenerativeModel, GenerativeProcess
from DashAI.back.dependencies.registry import ComponentRegistry
from DashAI.back.job.base_job import BaseJob, JobError
from DashAI.back.models.base_generative_model import BaseGenerativeModel

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class GenerativeJob(BaseJob):
    """GenerativeJob class to infer with generative models ."""

    def set_status_as_delivered(self) -> None:
        """Set the status of the job as delivered."""
        generative_process_id: int = self.kwargs["generative_process_id"]
        db: Session = self.kwargs["db"]

        process: GenerativeProcess = db.get(GenerativeProcess, generative_process_id)
        if not process:
            raise JobError(
                f"Generative process {generative_process_id} does not exist in DB."
            )
        try:
            process.set_status_as_delivered()
            db.commit()
        except exc.SQLAlchemyError as e:
            log.exception(e)
            raise JobError(
                "Internal database error",
            ) from e

    @inject
    def run(
        self,
        component_registry: ComponentRegistry = lambda di: di["component_registry"],
        config=lambda di: di["config"],
    ) -> None:
        generative_process_id: int = self.kwargs["generative_process_id"]
        db: Session = self.kwargs["db"]

        generative_process: GenerativeProcess = db.get(
            GenerativeProcess, generative_process_id
        )

        generative_model: GenerativeModel = db.get(
            GenerativeModel, generative_process.model_id
        )
        print(generative_model.generative_model)

        model_class = component_registry[generative_model.generative_model]["class"]
        params = generative_process.parameters

        try:
            model: BaseGenerativeModel = model_class(**params)
        except TypeError as e:
            logging.error(e)

        print(model)

        input = generative_process.input_data

        # Start the generation process
        generative_process.set_status_as_started()
        db.commit()

        # Generate
        out: Any = model.generate(input)

        # Process output and store it
        output_path: str = model.process_output(
            out, generative_process.name, config["GENERATIVE_PROCESS_PATH"]
        )

        # Update the generative_process with the output path
        generative_process.output_path = str(output_path)

        # Finish the generation process
        generative_process.set_status_as_finished()
        db.commit()
