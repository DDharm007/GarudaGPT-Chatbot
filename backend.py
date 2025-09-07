from flask import Flask, request, jsonify
from groq_client import chat_with_groq
from gemini_client import chat_with_gemini

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])
    deep_thinking = data.get("deep_thinking", False)
    
    # Check if the last message is requesting image generation
    last_message = messages[-1]["content"].lower() if messages else ""
    is_image_request = any(phrase in last_message for phrase in [
        "generate image", "create image", "make image", "draw", "generate a picture",
        "create a picture", "show me", "visualize", "generate an image", "create an image"
    ])
    
    # Use Groq with enhanced settings and image generation if requested
    groq_response = chat_with_groq(
        messages=messages,
        temperature=0.8 if deep_thinking else 0.7,
        max_tokens=2000 if deep_thinking else 1000,
        generate_image=is_image_request
    )
    
    # Check if response is structured or just a string
    if isinstance(groq_response, dict):
        response_data = {
            "response": groq_response["content"],
            "metadata": {
                "model": groq_response["model_used"],
                "usage": groq_response["usage"],
                "finish_reason": groq_response["finish_reason"]
            }
        }
        
        # Add image to response if available
        if "image" in groq_response:
            response_data["image"] = groq_response["image"]
            
        return jsonify(response_data)
    else:
        # Handle error case or simple string response
        return jsonify({"response": groq_response})
        
        # Check if response is structured or just a string
        if isinstance(groq_response, dict):
            return jsonify({
                "response": groq_response["content"],
                "metadata": {
                    "model": groq_response["model_used"],
                    "usage": groq_response["usage"],
                    "finish_reason": groq_response["finish_reason"]
                }
            })
        else:
            # Handle error case or simple string response
            return jsonify({"response": groq_response})

if __name__ == "__main__":
    app.run(port=5005, debug=True)
