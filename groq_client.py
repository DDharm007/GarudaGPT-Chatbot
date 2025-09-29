# REPLACE WITH YOUR API KEY
import requests
import os
import json
from typing import List, Dict, Optional, Union

GROQ_API_KEY = "YOUR_GROQ_API_KEY"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Available models with their context windows and capabilities
GROQ_MODELS = {
    "llama-4-scout": {
        "name": "meta-llama/llama-4-scout-17b-16e-instruct",
        "max_context": 8192,
        "description": "Latest model optimized for instruction following",
        "best_for": ["coding", "instruction following", "technical tasks"]
    },
    "mixtral-8x7b": {
        "name": "mixtral-8x7b",
        "max_context": 32768,
        "description": "Large context window model with strong performance",
        "best_for": ["long conversations", "document analysis", "complex tasks"]
    }
}

def format_prompt(message: str) -> str:
    """Format the prompt to get better responses from Groq"""
    return f"""As an AI assistant, I will help you with your request. I'll be clear, accurate, and helpful in my response.

User Request: {message}

Assistant Response:"""

def detect_task_type(messages: List[Dict[str, str]]) -> str:
    """Detect the type of task from the conversation to select the best model"""
    last_message = messages[-1]["content"].lower() if messages else ""
    
    if any(keyword in last_message for keyword in ["code", "program", "function", "debug", "error"]):
        return "llama-4-scout"
    elif len(str(messages)) > 6000:  # If conversation is long
        return "mixtral-8x7b"
    elif any(keyword in last_message for keyword in ["generate image", "create image", "draw", "picture"]):
        return "mixtral-8x7b"  # Use Mixtral for image prompt generation
    else:
        return "llama-4-scout"  # Default to a verified model

def generate_image_from_prompt(prompt: str) -> Optional[str]:
    """Generate an image using Stability AI's API"""
    try:
        stability_api_key = os.getenv("STABILITY_API_KEY")
        if not stability_api_key:
            return None

        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        headers = {
            "Authorization": f"Bearer {stability_api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 50,
        }

        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            image_data = data["artifacts"][0]["base64"]
            return image_data
        
        return None
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def chat_with_groq(
    messages: List[Dict[str, str]], 
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    top_p: float = 0.95,
    stream: bool = False,
    generate_image: bool = False
) -> Union[str, Dict]:
    """
    Enhanced chat function with Groq's API
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        model: Specific model to use, or None for automatic selection
        temperature: Controls randomness (0.0-1.0)
        max_tokens: Maximum tokens in response
        top_p: Nucleus sampling parameter
        stream: Whether to stream the response
    
    Returns:
        Response text or structured data
    """
    try:
        # Format messages correctly for Groq
        formatted_messages = []
        for msg in messages:
            # Format the user's last message for better results
            if msg["role"] == "user" and msg == messages[-1]:
                content = format_prompt(msg["content"])
            else:
                content = msg["content"]
                
            formatted_messages.append({
                "role": "assistant" if msg["role"] == "model" else msg["role"],
                "content": content
            })

        # Select the best model if none specified
        if not model:
            model = detect_task_type(messages)
        
        selected_model = GROQ_MODELS.get(model, GROQ_MODELS["llama-4-scout"])
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }
        
        data = {
            "model": selected_model["name"],
            "messages": formatted_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "stream": stream
        }
        
        if os.getenv("DEBUG"):
            print("Sending request to Groq API:", json.dumps(data, indent=2))
        
        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=data,
            timeout=30
        )
        
        if os.getenv("DEBUG"):
            print("Response status code:", response.status_code)
            
        if response.status_code == 200:
            result = response.json()
            response_text = result["choices"][0]["message"]["content"]
            
            # If image generation is requested
            if generate_image:
                # Generate an optimized prompt for image generation
                image_prompt_messages = [
                    {
                        "role": "system",
                        "content": "You are an expert at writing prompts for image generation. Convert the user's request into a detailed, descriptive prompt that will work well with image generation AI. Focus on visual details, style, mood, and lighting. Keep it under 100 words."
                    },
                    {
                        "role": "user",
                        "content": messages[-1]["content"]
                    }
                ]
                
                image_prompt_data = {
                    "model": selected_model["name"],
                    "messages": image_prompt_messages,
                    "temperature": 0.7,
                    "max_tokens": 200
                }
                
                prompt_response = requests.post(
                    GROQ_API_URL,
                    headers=headers,
                    json=image_prompt_data,
                    timeout=30
                )
                
                if prompt_response.status_code == 200:
                    image_prompt = prompt_response.json()["choices"][0]["message"]["content"]
                    image_data = generate_image_from_prompt(image_prompt)
                    
                    if image_data:
                        return {
                            "content": response_text,
                            "image": image_data,
                            "model_used": selected_model["name"],
                            "usage": result.get("usage", {}),
                            "finish_reason": result["choices"][0].get("finish_reason", "")
                        }
            
            # Return normal response if no image generation or if image generation failed
            return {
                "content": response_text,
                "model_used": selected_model["name"],
                "usage": result.get("usage", {}),
                "finish_reason": result["choices"][0].get("finish_reason", "")
            }
            print("Response content:", response.text)
        
        if response.status_code == 200:
            result = response.json()
            response_text = result["choices"][0]["message"]["content"]
            
            # Return structured response with metadata if available
            return {
                "content": response_text,
                "model_used": selected_model["name"],
                "usage": result.get("usage", {}),
                "finish_reason": result["choices"][0].get("finish_reason", None)
            }
        else:
            error_detail = response.json() if response.text else "No error details available"
            return f"Error: API returned status code {response.status_code}. Details: {error_detail}"
            
    except requests.exceptions.RequestException as e:
        return f"Network Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"
