from flask import Flask, render_template_string
import socket

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Load Balancer Demo</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --text-color: #f8fafc;
            --card-bg: rgba(255, 255, 255, 0.05);
            --card-border: rgba(255, 255, 255, 0.1);
        }
        body {
            margin: 0;
            padding: 0;
            font-family: 'Outfit', system-ui, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        
        .background-blobs {
            position: absolute;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            overflow: hidden;
            pointer-events: none;
        }
        
        .blob {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.5;
            animation: float 10s infinite alternate ease-in-out;
        }
        
        .blob-1 { top: -10%; left: -10%; width: 50vw; height: 50vw; background: {{ color }}; animation-delay: 0s; }
        .blob-2 { bottom: -20%; right: -10%; width: 60vw; height: 60vw; background: #3b82f6; animation-delay: -5s; }
        
        @keyframes float {
            0% { transform: scale(1) translate(0, 0); }
            100% { transform: scale(1.1) translate(5%, 5%); }
        }
        
        .container {
            position: relative;
            z-index: 1;
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 3rem;
            text-align: center;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            max-width: 600px;
            width: 90%;
            animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(40px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            background: linear-gradient(to right, #fff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        p.subtitle {
            color: #94a3b8;
            font-size: 1.1rem;
            margin-bottom: 2.5rem;
            font-weight: 300;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
            margin-bottom: 2.5rem;
        }
        
        .stat-card {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            transition: transform 0.2s, background 0.2s;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            background: rgba(0, 0, 0, 0.3);
        }
        
        .stat-label {
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94a3b8;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .stat-value {
            font-family: monospace;
            font-size: 1.5rem;
            color: #fff;
            word-break: break-all;
        }
        
        .color-indicator {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background-color: {{ color }};
            box-shadow: 0 0 30px {{ color }};
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 4px solid rgba(255,255,255,0.2);
            color: white;
        }

        .color-indicator svg {
            width: 40px;
            height: 40px;
        }

        button {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 1rem 2rem;
            font-size: 1.1rem;
            font-weight: 500;
            font-family: 'Outfit', sans-serif;
            border-radius: 9999px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0 auto;
        }
        
        button:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(255,255,255,0.1);
        }
        
        button:active {
            transform: scale(0.95);
        }
        
        button svg {
            width: 20px;
            height: 20px;
            transition: transform 0.5s;
        }
        
        button.loading svg {
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .request-count {
            margin-top: 1.5rem;
            font-size: 0.9rem;
            color: #64748b;
        }
    </style>
</head>
<body>
    <div class="background-blobs">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
    </div>
    
    <div class="container">
        <div style="display: flex; justify-content: center;">
            <div class="color-indicator">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 14.25h13.5m-13.5 0a3 3 0 0 1-3-3m3 3a3 3 0 1 0 0 6h13.5a3 3 0 1 0 0-6m-16.5-3a3 3 0 0 1 3-3h13.5a3 3 0 0 1 3 3m-19.5 0a4.5 4.5 0 0 1 .9-2.7L5.737 5.1a3.375 3.375 0 0 1 2.7-1.35h7.126c1.062 0 2.062.5 2.7 1.35l2.587 3.45a4.5 4.5 0 0 1 .9 2.7m0 0a3 3 0 0 1-3 3m0 3h.008v.008h-.008v-.008Zm0-6h.008v.008h-.008v-.008Zm-3 6h.008v.008h-.008v-.008Zm-3 6h.008v.008h-.008v-.008Z" />
                </svg>
            </div>
        </div>
        <h1>Load Balancing Demo</h1>
        <p class="subtitle">Experience dynamic traffic distribution in real-time</p>
        
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-label">Pod Hostname</span>
                <span class="stat-value" id="pod-name">{{ pod_name }}</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">Pod IP Address</span>
                <span class="stat-value" id="pod-ip">{{ pod_ip }}</span>
            </div>
        </div>
        
        <button id="refresh-btn" onclick="refreshData()">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
            Send New Request
        </button>
        
        <div class="request-count">
            Total requests in this session: <span id="counter" style="color: white; font-weight: bold;">1</span>
        </div>
    </div>

    <script>
        let counter = 1;
        
        function refreshData() {
            const btn = document.getElementById('refresh-btn');
            btn.classList.add('loading');
            
            counter = parseInt(sessionStorage.getItem('demoCount') || 1) + 1;
            sessionStorage.setItem('demoCount', counter);
            
            setTimeout(() => {
                window.location.reload(true);
            }, 300);
        }
        
        window.onload = () => {
            const stored = sessionStorage.getItem('demoCount');
            if (stored) {
                document.getElementById('counter').innerText = stored;
            } else {
                sessionStorage.setItem('demoCount', 1);
            }
        };
    </script>
</body>
</html>
"""

def get_color_from_string(s):
    # Paleta de colores vibrantes para un look premium
    colors = ['#ec4899', '#8b5cf6', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#14b8a6', '#6366f1', '#f43f5e', '#06b6d4']
    hash_val = sum(ord(c) for c in s)
    return colors[hash_val % len(colors)]

@app.route('/')
def home():
    pod_name = socket.gethostname()
    try:
        pod_ip = socket.gethostbyname(pod_name)
    except:
        pod_ip = "Unknown IP"
    color = get_color_from_string(pod_name)
    return render_template_string(HTML_TEMPLATE, pod_name=pod_name, pod_ip=pod_ip, color=color)

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
