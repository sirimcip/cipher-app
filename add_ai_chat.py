with open('templates/index.html', encoding='utf-8') as f:
    c = f.read()

# ── 1. Replace the placeholder AI tab with a real chat UI ──
old_ai = '''      <div id="dir-ai" style="display:none">
        <div class="ai-box">
          <div class="ai-label">⬡ CIPHER AI — PORTFOLIO INTELLIGENCE</div>
          <div class="ai-text">AI insights will appear here once connected to the Anthropic API. This will include anomaly detection, natural language report summaries, and flagged submissions requiring review.</div>
        </div>
      </div>'''

new_ai = '''      <div id="dir-ai" style="display:none">
        <div style="display:flex;flex-direction:column;height:calc(100vh - 140px);gap:0;">

          <!-- Header -->
          <div style="background:var(--navy);border-radius:12px 12px 0 0;padding:20px 24px;display:flex;align-items:center;gap:14px;">
            <svg width="28" height="32" viewBox="0 0 100 115" xmlns="http://www.w3.org/2000/svg">
              <polygon points="50,5 95,28 95,87 50,110 5,87 5,28" fill="#0A2472" stroke="#4A90D9" stroke-width="2"/>
              <polygon points="50,14 85,33 85,82 50,101 15,82 15,33" fill="none" stroke="#A8D4F5" stroke-width="0.8" opacity="0.5"/>
              <polyline points="74,42 50,29 26,42 26,73 50,86 74,73" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div>
              <div style="font-size:14px;font-weight:bold;letter-spacing:3px;color:#fff;">CIPHER AI</div>
              <div style="font-size:9px;letter-spacing:2px;color:var(--sky);font-family:'Courier New',monospace;">PORTFOLIO INTELLIGENCE ASSISTANT</div>
            </div>
            <div style="margin-left:auto;font-size:9px;color:var(--soft);font-family:'Courier New',monospace;text-align:right;line-height:1.6;">Information only · No investment advice<br/>Powered by Claude</div>
          </div>

          <!-- Chat messages -->
          <div id="ai-messages" style="flex:1;overflow-y:auto;padding:20px 24px;background:#fff;display:flex;flex-direction:column;gap:16px;">
            <!-- Welcome message -->
            <div style="display:flex;gap:12px;align-items:flex-start;">
              <div style="width:32px;height:32px;border-radius:50%;background:var(--navy);display:flex;align-items:center;justify-content:center;font-size:12px;color:#fff;flex-shrink:0;">⬡</div>
              <div style="background:#f0f4fa;border-radius:0 12px 12px 12px;padding:14px 16px;max-width:80%;">
                <div style="font-size:13px;color:#0A2472;line-height:1.7;">Hi! I'm CIPHER AI, your portfolio intelligence assistant. I can help you analyze your portfolio data, summarize performance, explain financial concepts, flag unusual patterns, and draft IC materials.<br><br>I provide <strong>information only</strong> — I won't give investment advice or recommendations. What would you like to know?</div>
                <div style="font-size:9px;color:#aab8d0;font-family:'Courier New',monospace;margin-top:8px;">CIPHER AI · Portfolio Intelligence</div>
              </div>
            </div>

            <!-- Suggested prompts -->
            <div style="display:flex;flex-wrap:wrap;gap:8px;margin-left:44px;">
              <button class="ai-prompt-btn" onclick="sendPrompt('Summarize our portfolio performance this quarter')">Summarize Q2 2026 performance</button>
              <button class="ai-prompt-btn" onclick="sendPrompt('Which manager had the highest return?')">Top performing manager</button>
              <button class="ai-prompt-btn" onclick="sendPrompt('Flag any unusual or anomalous submissions')">Flag anomalies</button>
              <button class="ai-prompt-btn" onclick="sendPrompt('Draft an executive summary for the IC meeting')">Draft IC summary</button>
              <button class="ai-prompt-btn" onclick="sendPrompt('Explain what TVPI means in private equity')">Explain TVPI</button>
            </div>
          </div>

          <!-- Input area -->
          <div style="background:#fff;border-top:1px solid #dde6f5;border-radius:0 0 12px 12px;padding:16px 24px;display:flex;gap:12px;align-items:flex-end;">
            <textarea id="ai-input" placeholder="Ask anything about your portfolio..." 
              style="flex:1;padding:12px 14px;border:1.5px solid #dde6f5;border-radius:8px;font-family:Georgia,serif;font-size:13px;color:#0A2472;resize:none;min-height:44px;max-height:120px;outline:none;transition:border 0.2s;"
              onfocus="this.style.borderColor='#4A90D9'" onblur="this.style.borderColor='#dde6f5'"
              onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();sendAIMessage()}"
              oninput="this.style.height='auto';this.style.height=Math.min(this.scrollHeight,120)+'px'"></textarea>
            <button onclick="sendAIMessage()" id="ai-send-btn"
              style="padding:12px 20px;background:var(--navy);color:#fff;border:none;border-radius:8px;font-size:10px;letter-spacing:2px;font-family:'Courier New',monospace;cursor:pointer;white-space:nowrap;transition:background 0.2s;"
              onmouseover="this.style.background='#1a3a8a'" onmouseout="this.style.background='#0A2472'">SEND</button>
          </div>
        </div>
      </div>'''

if 'ai-messages' not in c:
    if old_ai in c:
        c = c.replace(old_ai, new_ai, 1)
        print("Replaced AI tab with chat UI")
    else:
        # Try a looser match
        import re
        match = re.search(r'<div id="dir-ai"[^>]*>.*?<div class="ai-box">.*?</div>\s*</div>\s*</div>', c, re.DOTALL)
        if match:
            c = c.replace(match.group(0), new_ai, 1)
            print("Replaced AI tab with chat UI (loose match)")
        else:
            print("ERROR: Could not find AI tab to replace")
else:
    print("Chat UI already present")

# ── 2. Add AI chat CSS ──
old_style_end = '    /* ── CHARTS ── */'
new_style = '''    /* ── AI CHAT ── */
    .ai-prompt-btn {
      padding: 7px 14px; background: #eef5ff; color: var(--navy);
      border: 1px solid #dde6f5; border-radius: 20px; font-size: 11px;
      font-family: 'Courier New', monospace; cursor: pointer; transition: all 0.2s;
    }
    .ai-prompt-btn:hover { background: var(--navy); color: #fff; border-color: var(--navy); }

    .ai-user-msg {
      display: flex; gap: 12px; align-items: flex-start; flex-direction: row-reverse;
    }
    .ai-user-msg .ai-bubble {
      background: var(--navy); color: #fff; border-radius: 12px 0 12px 12px;
      padding: 12px 16px; max-width: 75%; font-size: 13px; line-height: 1.6;
    }
    .ai-user-avatar {
      width: 32px; height: 32px; border-radius: 50%; background: var(--sky);
      display: flex; align-items: center; justify-content: center;
      font-size: 12px; color: #fff; flex-shrink: 0;
    }
    .ai-bot-msg { display: flex; gap: 12px; align-items: flex-start; }
    .ai-bot-bubble {
      background: #f0f4fa; border-radius: 0 12px 12px 12px;
      padding: 14px 16px; max-width: 80%; font-size: 13px; color: #0A2472; line-height: 1.7;
    }
    .ai-bot-avatar {
      width: 32px; height: 32px; border-radius: 50%; background: var(--navy);
      display: flex; align-items: center; justify-content: center;
      font-size: 14px; color: #fff; flex-shrink: 0;
    }
    .ai-typing {
      display: flex; gap: 4px; align-items: center; padding: 8px 0;
    }
    .ai-typing span {
      width: 6px; height: 6px; background: #aab8d0; border-radius: 50%;
      animation: aiTyping 1.2s infinite;
    }
    .ai-typing span:nth-child(2) { animation-delay: 0.2s; }
    .ai-typing span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes aiTyping { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-6px)} }

    /* ── CHARTS ── */'''

if 'ai-prompt-btn' not in c:
    if old_style_end in c:
        c = c.replace(old_style_end, new_style, 1)
        print("Added AI chat CSS")
    else:
        print("WARNING: Could not find style anchor for AI CSS")
else:
    print("AI CSS already present")

# ── 3. Add AI chat JavaScript ──
ai_js = '''
  // ══ CIPHER AI CHAT ══
  const CIPHER_AI_SYSTEM = `You are CIPHER AI, an intelligent portfolio intelligence assistant embedded inside the CIPHER Platform — an institutional portfolio management tool used by investment teams at hospitals, nonprofits, and institutional investors.

Your role is to help the investment team with:
- Analyzing and summarizing portfolio performance data
- Explaining financial concepts and metrics (IRR, TVPI, PME, J-curve, attribution, etc.)
- Identifying patterns or anomalies in submission data
- Drafting executive summaries and IC meeting materials
- Answering questions about the portfolio, managers, asset classes, and market data shown in CIPHER

IMPORTANT RULES:
- You provide INFORMATION ONLY. Never give investment advice, recommendations to buy/sell, or suggest portfolio changes.
- If asked for investment advice, politely decline and explain you can only provide information.
- Always add a disclaimer when discussing performance data: "This is for informational purposes only and does not constitute investment advice."
- Be concise, professional, and use institutional investment terminology appropriately.
- When you don't have specific data, say so clearly rather than making it up.

Current platform context: CIPHER Platform — institutional portfolio reporting tool.`;

  let aiChatHistory = [];

  function addMessage(role, content, isTyping = false) {
    const container = document.getElementById('ai-messages');
    const div = document.createElement('div');

    if (isTyping) {
      div.id = 'ai-typing-indicator';
      div.className = 'ai-bot-msg';
      div.innerHTML = `
        <div class="ai-bot-avatar">⬡</div>
        <div class="ai-bot-bubble">
          <div class="ai-typing"><span></span><span></span><span></span></div>
        </div>`;
    } else if (role === 'user') {
      div.className = 'ai-user-msg';
      div.innerHTML = `
        <div class="ai-user-avatar">👤</div>
        <div class="ai-bubble">${content}</div>`;
    } else {
      div.className = 'ai-bot-msg';
      div.innerHTML = `
        <div class="ai-bot-avatar">⬡</div>
        <div class="ai-bot-bubble">
          <div>${content}</div>
          <div style="font-size:9px;color:#aab8d0;font-family:'Courier New',monospace;margin-top:8px;">CIPHER AI · Information only — not investment advice</div>
        </div>`;
    }

    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    return div;
  }

  function removeTypingIndicator() {
    const el = document.getElementById('ai-typing-indicator');
    if (el) el.remove();
  }

  function getPortfolioContext() {
    // Build context from current page data
    let ctx = "Current portfolio data visible in CIPHER:\\n";
    const invested = document.getElementById('dir-total-invested')?.textContent;
    const gained   = document.getElementById('dir-total-gained')?.textContent;
    const submitted = document.getElementById('dir-submitted-count')?.textContent;
    const missing  = document.getElementById('dir-missing-count')?.textContent;
    if (invested) ctx += `- Total Invested: ${invested}\\n`;
    if (gained)   ctx += `- Total Gained: ${gained}\\n`;
    if (submitted) ctx += `- Managers Submitted: ${submitted}\\n`;
    if (missing)  ctx += `- Missing Submissions: ${missing}\\n`;
    ctx += "\\nSample analytics data (from platform):\\n";
    ctx += "- Portfolio YTD Return: +8.4% vs S&P 500 +6.2% (alpha: +2.2%)\\n";
    ctx += "- Asset classes: Public Equity 33.8%, Private Equity 25.3%, Fixed Income 19.9%, Real Assets 14.6%, Operations 6.4%\\n";
    ctx += "- Total portfolio value: $124.6M\\n";
    ctx += "- Liquidity: $18.4M immediately available, $74.8M illiquid\\n";
    ctx += "- Top PE fund: Apex Growth III (IRR: 18.4%, TVPI: 1.42x)\\n";
    return ctx;
  }

  async function sendAIMessage() {
    const input = document.getElementById('ai-input');
    const msg = input.value.trim();
    if (!msg) return;

    input.value = '';
    input.style.height = '44px';

    // Add user message
    addMessage('user', msg);
    aiChatHistory.push({ role: 'user', content: msg });

    // Show typing indicator
    addMessage('ai', '', true);

    // Disable send button
    const btn = document.getElementById('ai-send-btn');
    btn.disabled = true;
    btn.textContent = '...';

    try {
      const portfolioCtx = getPortfolioContext();
      const systemPrompt = CIPHER_AI_SYSTEM + "\\n\\n" + portfolioCtx;

      const res = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: 'claude-sonnet-4-6',
          max_tokens: 1000,
          system: systemPrompt,
          messages: aiChatHistory
        })
      });

      const data = await res.json();
      const reply = data.content?.[0]?.text || "I'm sorry, I couldn't generate a response. Please try again.";

      removeTypingIndicator();
      addMessage('ai', reply.replace(/\\n/g, '<br>'));
      aiChatHistory.push({ role: 'assistant', content: reply });

      // Keep history to last 20 messages to avoid token limits
      if (aiChatHistory.length > 20) aiChatHistory = aiChatHistory.slice(-20);

    } catch (e) {
      removeTypingIndicator();
      addMessage('ai', "I'm having trouble connecting right now. Please check your connection and try again.");
      console.error('CIPHER AI error:', e);
    }

    btn.disabled = false;
    btn.textContent = 'SEND';
  }

  function sendPrompt(text) {
    document.getElementById('ai-input').value = text;
    sendAIMessage();
  }'''

if 'CIPHER_AI_SYSTEM' not in c:
    last = c.rfind('</script>')
    c = c[:last] + ai_js + '\n' + c[last:]
    print("Added AI chat JavaScript")
else:
    print("AI JS already present")

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("\nDone!")
print("  1. Restart: uvicorn main:app --reload")
print("  2. Log in as director")
print("  3. Click AI Insights in the sidebar")
print("  4. Chat with CIPHER AI about your portfolio")
