import ollama
import json

def get_ai_response(task_text, mode="autonomous"):
    if mode == "autonomous":
        template = {
            "mode": "autonomous",
            "intent": "",
            "title": "",
            "deadline": "",
            "priority": "",
            "auto_execute": True
        }
        system_role = "You are a Smart Task Management Agent. You MUST return STRICT JSON only. Do NOT explain. Do NOT speak conversationally. Output must be valid JSON."
    else:
        template = {
            "mode": "human_in_loop",
            "intent": "",
            "title": "",
            "deadline": "",
            "suggestion": "",
            "message": "Do you want me to save this task?"
        }
        system_role = "You are a Smart Task Assistant. You MUST return STRICT JSON only. Do NOT explain. Do NOT speak conversationally. Output must be valid JSON."

    prompt = f"""
Analyze the user task.
Detect intent:
- create_task
- update_task
- delete_task
- list_tasks
- plan_task
Extract:
- title
- deadline
- priority if mentioned
Prioritize tasks automatically based on deadline and urgency.
Return ONLY JSON:
{json.dumps(template)}
Task:
{task_text}
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ],
        options={
            "temperature": 0.4,
            "num_predict": 60,
            "top_k": 30,
            "top_p": 0.9
        }
    )

    return response["message"]["content"]
