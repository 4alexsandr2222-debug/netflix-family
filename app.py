from flask import Flask, request, redirect, render_template_string
import requests
import json
import os

app = Flask(__name__)

# قاعدة بيانات الأكواد
users_database = {
    "1234": {"name": "أحمد", "used": False},
    "5678": {"name": "سارة", "used": False},
    "9999": {"name": "يوسف", "used": False}
}

# الكوكيز ديال Netflix (غادي نعوضوهوم بعدين)
NETFLIX_COOKIES = [
    {
        "name": "NetflixId",
        "value": "your_netflix_cookie_here",
        "domain": ".netflix.com",
        "path": "/"
    },
    {
        "name": "SecureNetflixId", 
        "value": "your_secure_cookie_here",
        "domain": ".netflix.com",
        "path": "/"
    }
]

# واجهة الدخول
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Netflix العائلة</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: #000; 
            color: white; 
            text-align: center; 
            padding: 50px;
            margin: 0;
        }
        .container { 
            max-width: 400px; 
            margin: 0 auto; 
            background: #141414; 
            padding: 40px; 
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(229, 9, 20, 0.3);
            border: 1px solid #333;
        }
        h1 {
            color: #E50914;
            margin-bottom: 20px;
        }
        input { 
            padding: 15px; 
            margin: 10px 0; 
            width: 80%; 
            border-radius: 8px; 
            border: 2px solid #333;
            background: #1a1a1a;
            color: white;
            font-size: 16px;
            text-align: center;
        }
        input:focus {
            outline: none;
            border-color: #E50914;
        }
        button { 
            padding: 15px; 
            margin: 20px 0; 
            width: 80%; 
            border-radius: 8px; 
            border: none; 
            background: #E50914; 
            color: white; 
            font-weight: bold; 
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        button:hover {
            background: #f40612;
            transform: translateY(-2px);
        }
        .users-list {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #333;
        }
        .user-item {
            background: rgba(255,255,255,0.1);
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 Netflix العائلة</h1>
        <p>أدخل الكود السري للدخول التلقائي</p>
        
        <form action="/login" method="POST">
            <input type="password" name="code" placeholder="أدخل الكود (4 أرقام)" required maxlength="4" pattern="[0-9]{4}">
            <br>
            <button type="submit">🚀 دخول تلقائي ل Netflix</button>
        </form>

        <div class="users-list">
            <h3>👥 أفراد العائلة:</h3>
            <div class="user-item"><strong>أحمد</strong> - 1234</div>
            <div class="user-item"><strong>سارة</strong> - 5678</div>
            <div class="user-item"><strong>يوسف</strong> - 9999</div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/login', methods=['POST'])
def login():
    code = request.form['code']
    
    if code in users_database and not users_database[code]['used']:
        # الكود صحيح - ندير الدخول التلقائي
        users_database[code]['used'] = True
        user_name = users_database[code]['name']
        
        # نوجه المستخدم ل Netflix مع الكوكيز
        return f'''
        <div style="text-align: center; padding: 50px; background: #000; color: white;">
            <h1 style="color: #E50914;">✅ تم الدخول بنجاح!</h1>
            <p>مرحبا {user_name}! جاري توجيهك إلى Netflix...</p>
            <script>
                setTimeout(function() {{
                    window.location.href = '/netflix-proxy';
                }}, 2000);
            </script>
        </div>
        '''
    else:
        return '''
        <div style="text-align: center; padding: 50px; background: #000; color: white;">
            <h1 style="color: #E50914;">❌ خطأ في الدخول</h1>
            <p>الكود غير صحيح أو مستخدم مسبقا</p>
            <a href="/" style="color: #E50914;">← العودة للصفحة الرئيسية</a>
        </div>
        '''

@app.route('/netflix-proxy')
def netflix_proxy():
    try:
        # نعمل جلسة مع الكوكيز
        session = requests.Session()
        
        # نضيف الكوكيز للجلسة
        for cookie in NETFLIX_COOKIES:
            session.cookies.set(
                cookie['name'],
                cookie['value'],
                domain=cookie['domain'],
                path=cookie['path']
            )
        
        # نجيب محتوى Netflix
        response = session.get('https://netflix.com/browse', headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # نرجع المحتوى للمستخدم
        return response.text
        
    except Exception as e:
        return f'''
        <div style="text-align: center; padding: 50px; background: #000; color: white;">
            <h1 style="color: #E50914;">❌ خطأ تقني</h1>
            <p>Error: {str(e)}</p>
            <p>⏳ جاري إصلاح المشكلة...</p>
            <a href="/" style="color: #E50914;">← العودة للصفحة الرئيسية</a>
        </div>
        '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
