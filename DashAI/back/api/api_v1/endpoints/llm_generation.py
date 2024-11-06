from fastapi import APIRouter, HTTPException, Depends
from kink import di

from DashAI.back.dependencies.registry.component_registry import ComponentRegistry
from DashAI.back.api.api_v1.schemas.llm_params import LlamaRequest

router = APIRouter()


@router.post("/generate")
async def generate_text(
    request: LlamaRequest,
    component_registry: ComponentRegistry = Depends(lambda: di["component_registry"]),
):
    try:
        # Get the Llama model class from the component registry
        model_class = component_registry["LlamaModel"]["class"]

        # Instantiate the model with the required parameters
        model = model_class(
            max_tokens=request.max_tokens,  # Use the max tokens value from the request
        )

        # Generate text using the prompt from the request
        generated_text = model.generate(request.prompt)

        return {"generated_text": generated_text}

    except Exception as e:
        # Raise an HTTP exception with a 500 status code in case of errors
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")
