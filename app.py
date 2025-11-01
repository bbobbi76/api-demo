import os
import google.generativeai as genai
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# Flask 앱 초기화
app = Flask(__name__)

# .env 파일에 GOOGLE_API_KEY가 있는지 확인
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_API_KEY 환경 변수를 찾을 수 없습니다.")
    print("프로젝트 루트에 .env 파일을 만들고 'GOOGLE_API_KEY=\"당신의_API_키\"' 형식으로 저장했는지 확인하세요.")
    exit()

# Gemini API 설정
genai.configure(api_key=api_key)

# ✅ Flask 라우팅
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_alert', methods=['POST'])
def generate_alert():
    try:
        # 요청이 JSON 형태인지 확인
        if not request.is_json:
            return jsonify({"error": "요청은 JSON 형식이어야 합니다."}), 415

        # 사용자 요청에서 데이터 가져오기
        data = request.get_json()
        prompt = data.get("prompt", "다음 문장을 그대로 출력해줘: '노인이 침대에서 떨어졌습니다.'") #노인이 떨어진 영상 분석했다 가정

        # ✅ Gemini 모델 선택 (flash = 빠름, pro = 정밀)
        model = genai.GenerativeModel("gemini-2.5-flash")


        # Gemini API 호출
        response = model.generate_content(prompt)

        return jsonify({"alert_message": response.text})

    except Exception as e:
        print(f"!!!!!!!!!!!!!!!!! API 호출 오류: {e} !!!!!!!!!!!!!!!!!!")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
