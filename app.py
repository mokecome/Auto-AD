# -*- coding: utf-8 -*-
"""
連出去
-form=>action
-超連結
"""
from flask import Flask, request, jsonify, render_template
import configparser
from flask_cors import CORS
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
import webbrowser
import  requests

app = Flask(__name__)
app.jinja_env.variable_start_string = '%%'
app.jinja_env.variable_end_string = '%%'

CORS(app)

# Load the configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

azure_endpoint = config['AzureOpenAI']['azure_endpoint']
api_key = config['AzureOpenAI']['api_key']
api_version = config['AzureOpenAI']['api_version']
print("azure_endpoint : " + azure_endpoint)

from openai import AzureOpenAI
client = AzureOpenAI(
        api_key='a34657118e1e4ca3b7e62c3ecfd1cb80',
        azure_endpoint = 'https://mokecome-openai-20240501.openai.azure.com/',
        api_version="2024-02-15-preview"
    )
    

def get_html_data(url='https://www.philips-da.com.tw/collections/%E6%B0%A3%E7%82%B8%E9%8D%8B'):
    html = requests.get(url)
    reponse = html.text     
    from html2text import HTML2Text
    import re
    converter = HTML2Text()
    converter.ignore_links = True    
    converter.ignore_images = True   
    markdown = converter.handle(reponse)  
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    return markdown

def llm(system_prompt,combined_message):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": combined_message}
    ] 

    response = client.chat.completions.create(
        model='gpt4o-mokecome-0522',  
        messages=messages,
        temperature=0.7,
        max_tokens=1500,
        top_p=0.90,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    reply = response.choices[0].message.content.strip()
    return reply


product='飛利浦海星氣炸鍋'
aisas_dict={'attention':f'''你的角色是產品行銷專家和品牌行銷專家,擅長分析市場消費者需求，找出購買關鍵因素，並注重產品體驗的情境設定，主要販售給注重生活的單身貴族，喜歡展示品味追求精緻品牌的家電愛好者，你擁有豐富的產品開發和通路策劃以及行銷規劃經驗。
                 以提升廣告曝光量或網站訪問量為指標，結合年輕人喜愛的"熱門新聞議題"文字，例如最近很紅的音樂：FridayNight，目的是利用吸睛的標題及內文，增加市場吸引力和消費者關注,以專業且正向的描述{product}。             
                 以150字內說明。''',
             'interest':f'''你是市場分析師,我是產品行銷經理,我想要開發{product},確定目標市場群體,目的是精確定位產品行銷策略,吸引目標族群的注意力，擬定再行銷策略。
             分析並列出可能的目標市場群體,包括每個群體的年紀、性別、生活方式、特點、主要需求和市場規模。包含落魄貴族的這個目標族群。
             
             主要鎖定目標族群約20歲到40歲的落魄貴族族群，女性居多，教育程度大學以上，收入約3萬到5萬，喜歡展示品味追求精緻品牌，生活方式注重飲食健康和身材管理。有興趣的內容：健康飲食、烹飪技巧、食品衛生、疾病資訊，舉例來說會受到「價格促銷、新品推出、節慶優惠、會員集點」吸引。，讓進一步產生興趣。
             以頁面停留時間或產品諮詢量為指標,將產品廣告文案優化再行銷。
             會用專業且正向的描述,以300字內說明。 ''',
             'search': f'''你的角色是SEO廣告行銷專家,擅長分析市場關鍵字排名，及規劃合適的關鍵字廣告，擁有豐富的產品關鍵字廣告規劃經驗。
                   你販賣的商品是{product}，以關鍵詞搜索量或社交媒體話題熱度為指標設計。
                   請幫我找出最適合的關鍵字，不需要其他內容''',
             'action':'''你是網頁設計及SEO的專家，會對現有的網頁文案及圖片做優化，以購買轉化率和銷售量為指標。請針對飛利浦HD9257/80氣炸鍋及網頁：https://www.philips-da.com.tw/products/hd925780 提出專業且具體的修改建議。請包括以下幾點：
                1.首頁設計：
                改善頁面布局，使關鍵信息更加突出。
                提供更吸引人的視覺元素，增加高質量產品圖片和使用場景圖片。
                2.文案優化：
                強調產品的核心賣點和獨特功能，使用簡潔有力的語言。
                增加客戶見證和評價，增強信任感和購買欲望。
                3.SEO優化：
                使用適當的關鍵詞以提升搜尋引擎排名，例如“氣炸鍋最佳選擇”、“健康烹飪”等。
                優化元標題和描述，吸引更多點擊。
                4.使用者體驗：
                提供清晰的購買流程，減少購物車放棄率。
                增加產品比較功能，幫助消費者更好地做出購買決策。
                5.行動裝置優化：
                確保網頁在各種行動裝置上顯示良好，提升行動購物體驗。
                減少頁面載入時間，提高用戶留存率。
                請詳細描述每項建議的具體措施及其預期效果，確保能有效提升購買轉化率和銷售量。
             '''   ,
             'share':f'''你的角色是真實買家,擅長用樸實無華的文字評價某個產品使用後的感受。
                               你是一個熱愛發表意見，並且每天煮飯的人，喜歡用烹調設備做出各種美食。
                               以社交媒體分享次數或客戶推薦率為指標,
                               請對{product}列點描述以FABE文案的不同角度列舉,做出口語化真實的描述。
                               請將回答的問題自動進行列點並換行，並以150字內說明。''',
             'qa':'''# Role: 你的角色是專業電商客服問答助手

             ## Profile
             - author: LangGPT 
             - version: 1.0
             - language: 中文
             - description: 電商客服問答助手，透過AI技術提供即時、準確的客戶服務，解答常見問題並協助處理 訂單、退換貨、支付等相關事宜。還能提供商品使用方式的詳細說明。

             ## Skills
             1. 能夠回答常見的客戶問題，如產品資訊、訂單狀態、物流追蹤等。
             2. 協助客戶處理訂單問題，如退換貨、退款、訂單修改等。
             3. 提供支付幫助和解決支付相關問題。
             4. 能夠理解並回應客戶的特定需求，提供個性化服務。
             5. 使用tool提供商品使用方式的詳細說明。

             ## Background(可選項):
             電商客服問答助手旨在提升客戶服務效率，減少客服工作量，提高客戶滿意度。透過即時回應和準確回答，幫助客戶快速解決問題，提升購物體驗。

             ## Goals(可選項):
             1. 提供高效、準確的客戶服務。
             2. 減少客戶等待時間，提高回應速度。
             3. 增強客戶體驗和滿意度。
             4. 提供詳細的商品使用方式說明，提升客戶使用體驗。
             5. 只返回台灣繁體中文，不允許有換行符等其他內容，否則會受到懲罰。

             ## OutputFormat(可選項):
             - 工具: 'tools'

             ## Rules
             1. 使用簡潔明瞭的語言回答客戶問題。
             2. 遇到無法解答的問題時，引導客戶聯絡人工客服。
             3. 在回答中盡可能提供詳細的資訊和解決方案。
             4. 遵循平台的服務政策和標準。
             5. 使用tool提供商品使用方式的詳細說明。

             ## Workflows
             1. 收集客戶問題，進行分類和分析。
             2. 根據常見問題和平台政策，設計初步的回答模板。
             3. 評估回答的準確性和覆蓋度，必要時進行調整和優化。
             4. 透過AI提供即時回答，並根據客戶反饋不斷改進服務。
             5. 使用tool提供商品使用方式的詳細說明，確保回應的準確性和實用性。

             ## Init
             歡迎使用客服問答小助手，請問我可以幫您解決什麼問題？''',
             'image':'''這是一台氣炸鍋，請生成視覺產品圖，去背，真實，居家，廚房'''}



def edit_image(input_url,bg_prompt='a cozy marble kitchen with wine glasses' ):
    import io
    import requests
    from PIL import Image
    image_file_object= Image.open(input_url)
    # 將圖像轉換為 bytes
    img_byte_arr = io.BytesIO()
    image_file_object.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    r = requests.post('https://clipdrop-api.co/replace-background/v1',
         files = {'image_file': (input_url,img_byte_arr,'image/png'),},
         data = { 'prompt': bg_prompt},
      headers = { 'x-api-key': 'e6530e6a1ece851131cad3875f02cc9cb0b25639530f5b09376b3fe10f084d3c7902e464b22429c33889e08918292e33'}
    )
    if r.ok:
        # r.content 包含返回圖像的 bytes
        print(r.content)
        with open('img/out_image.png', 'wb') as f:
            f.write(r.content)
    else:
      r.raise_for_status()
     


def qdrant_search(query: str):
    """當用戶詢問商品相關問題時,使用這個工具來搜索相關律文件。"""
    embedding_model = AzureOpenAIEmbeddings(
        api_key='',
        azure_deployment='',
        openai_api_version='',
        azure_endpoint='',
    )
    client = Qdrant(
        QdrantClient(path="./productInformation"),
        "local_documents",
        embedding_model,
    )
    retriever = client.as_retriever(search_kwargs={"k": 3})
    result = retriever.invoke(query)
    return result

@app.route('/')
def index():
    # 定義 message 變量
    message = "一個消息"
    # 將 message 變量傳遞給模板
    return render_template('index.html', message=message)

@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_message = data.get('userMessage')
    button_message = data.get('buttonMessage')
    print(f"User message: {user_message}")
    # Combine messages for GPT-4
    html_response=get_html_data(url='https://www.philips-da.com.tw/collections/%E6%B0%A3%E7%82%B8%E9%8D%8B')
    combined_message = f'''{user_message}\n{button_message}\n,會參考{html_response}的內容'''
    
    #button_message->
    system_prompt = ''
    if button_message=='創意文字':
        system_prompt=aisas_dict['attention']
        html_response=get_html_data(url='https://www.philips-da.com.tw/collections/%E6%B0%A3%E7%82%B8%E9%8D%8B')
        combined_message = f'''{user_message}\n{button_message}\n,會參考{html_response}的內容'''
    elif button_message=='再行銷策略':
        system_prompt=aisas_dict['interest']
    elif button_message=='優化關鍵字':
        system_prompt=aisas_dict['search']
    elif button_message=='優化網頁':
        system_prompt=aisas_dict['action']
    elif button_message=='買家評論':
        system_prompt=aisas_dict['share']
        
    if 'QA' in button_message:
        system_prompt=aisas_dict['qa']
        webbrowser.open('http://127.0.0.1:8001/')
    
    if button_message=='我需要廣告圖片':
        edit_image('img/00-1.png',bg_prompt='a camping scene and blue sky')
        webbrowser.open('http://127.0.0.1:8000/img')
        return jsonify({'reply': '已經生成圖片'})
            
    try:
        reply=llm(system_prompt,combined_message)
        return jsonify({'reply': reply})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'reply': 'An error occurred while processing your request.'}), 500


if __name__ == "__main__":
    app.run(port=5001)
    

