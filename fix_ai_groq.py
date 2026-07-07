with open('routes.py', encoding='utf-8') as f:
    c = f.read()

ai_route = '''

# ── CIPHER AI CHAT ENDPOINT (Groq) ──
import httpx as _httpx
from fastapi import Request as _Request
from pydantic import BaseModel as _BaseModel
from typing import List as _List

class AIMessage(_BaseModel):
    messages: _List[dict]
    system: str

@router.post("/ai/chat")
async def ai_chat(data: AIMessage):
    try:
        # Prepend system message for Groq (uses messages format)
        msgs = [{"role": "system", "content": data.system}] + data.messages
        async with _httpx.AsyncClient() as client:
            res = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": "Bearer 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",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "max_tokens": 1000,
                    "messages": msgs
                },
                timeout=30
            )
        data_resp = res.json()
        # Return in Anthropic-style format so frontend works unchanged
        text = data_resp.get("choices", [{}])[0].get("message", {}).get("content", "")
        return {"content": [{"type": "text", "text": text}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error: {str(e)}"}]}
'''

if '/ai/chat' not in c:
    c += ai_route
    print("Added Groq AI chat route")
else:
    # Update existing route with Groq
    import re
    c = re.sub(
        r'@router\.post\("/ai/chat"\).*?(?=@router|\Z)',
        ai_route.strip() + '\n\n',
        c,
        flags=re.DOTALL
    )
    print("Updated existing AI chat route to use Groq")

with open('routes.py', 'w', encoding='utf-8') as f:
    f.write(c)

# Make sure httpx is importable
import subprocess, sys
subprocess.run([sys.executable, '-m', 'pip', 'install', 'httpx', '--quiet', '--break-system-packages'], capture_output=True)
print("httpx installed")

# Update frontend to call backend
with open('templates/index.html', encoding='utf-8') as f:
    h = f.read()

old_fetch = "      const res = await fetch('https://api.anthropic.com/v1/messages', {"
new_fetch = "      const res = await fetch(`${API}/ai/chat`, {"

old_body = """        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: 'claude-sonnet-4-6',
          max_tokens: 1000,
          system: systemPrompt,
          messages: aiChatHistory
        })"""

new_body = """        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          system: systemPrompt,
          messages: aiChatHistory
        })"""

if old_fetch in h:
    h = h.replace(old_fetch, new_fetch, 1)
    h = h.replace(old_body, new_body, 1)
    print("Updated frontend to use backend AI proxy")
elif f'{API}/ai/chat' in h or '${API}/ai/chat' in h:
    print("Frontend already using backend proxy")
else:
    print("WARNING: Could not find fetch call to update")

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("\nDone!")
print("  1. Restart: uvicorn main:app --reload")
print("  2. Log in as director, click AI Insights")
print("  3. Ask anything about your portfolio!")
