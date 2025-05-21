"""Utility for generating images using OpenAI's DALL-E 3."""

import os
from datetime import datetime
from pathlib import Path
import logging
import requests

from openai import AzureOpenAI
from config import Config


logger = logging.getLogger(__name__)

def create_image(prompt: str, cfg: Config, out_dir: str = "images") -> str:
    """Generate an image from a text prompt using Azure OpenAI's DALL-E 3.
    
    Args:
        prompt: Text description to generate image from
        cfg: Application configuration with Azure details
        out_dir: Directory to save image in (relative to project root)
        
    Returns:
        Relative path to the saved image file, or None if generation failed
    """
    try:
        # Create output directory if it doesn't exist
        Path(out_dir).mkdir(exist_ok=True)
        
        # Initialize Azure client
        client = AzureOpenAI(
            api_key=cfg.api_key,
            api_version=cfg.image_api_version,
            azure_endpoint=cfg.endpoint
        )
        
        logger.info(f"Generating image with prompt: {prompt}")
        logger.info(f"Using Azure OpenAI endpoint: {cfg.endpoint}")
        logger.info(f"Using Azure OpenAI deployment: {cfg.image_deployment}")
        logger.info(f"Using Azure OpenAI API version: {cfg.image_api_version}")


        # Generate image
        response = client.images.generate(
            model=cfg.image_deployment,
            prompt=prompt,
            n=1,
            style="vivid",
            quality="standard",
        )
        
        logger.info(f"Image generation response: {response}")

        # Download image
        image_url = response.data[0].url
        image_resp = requests.get(image_url)
        image_resp.raise_for_status()
        
        # Save with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = Path(out_dir) / f"{timestamp}.png"
        
        with open(image_path, "wb") as f:
            f.write(image_resp.content)
            
        return str(image_path)
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Failed to generate/save image: {error_msg}")
        return None
