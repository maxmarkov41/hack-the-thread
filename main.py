import os
import asyncio
from quart import Quart, jsonify, request
from quart_cors import cors
from backend.Telegram.links import main
from backend.Database.store_retrieve import MNG
from telegram import Update
from dotenv import load_dotenv


load_dotenv()
token = os.getenv("telegram_bot_token")
URI = os.getenv('connection_string')
DB_NAME = os.getenv('db_name')
COLLECTION_NAME = os.getenv('collection_name')

app = Quart(__name__)
app = cors(app, allow_origin="*")

mango = MNG(URI,DB_NAME,COLLECTION_NAME)

@app.route('/')
async def index():
    return jsonify({"message": "API is running!"})

@app.route('/api/data', methods=['GET'])
async def api_get_all():
    try:
        data = await asyncio.to_thread(mango.get)
        return jsonify({"status": "success", "count": len(data), "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/api/data/tag/<string:tag_name>', methods=['GET'])
async def api_get_by_tag(tag_name):
    print(tag_name)
    try:
        data = await asyncio.to_thread(mango.get_by_tag, tag_name)
        return jsonify({"status": "success", "count": len(data), "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/data/time', methods=['GET'])
async def api_get_by_time():
    try:
        start_str = request.args.get('start')
        end_str = request.args.get('end')

        if not start_str:
            return jsonify({"status": "error", "message": "Missing required 'start' parameter"}), 400

        start = int(start_str)
        end = int(end_str) if end_str else None

        data = await asyncio.to_thread(mango.get_by_time, start, end)
        return jsonify({"status": "success", "count": len(data), "data": data}), 200
        
    except ValueError:
        return jsonify({"status": "error", "message": "Timestamps must be valid integers"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
async def actual_main():
    print('Starting Telegram Server')
    bot = await main()
    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling(allowed_updates=Update.ALL_TYPES) # run until ctrl / cmd + c is detected
    print("Starting Quart API Server on port 5000")
    await app.run_task(host='0.0.0.0', port=5000)

if __name__ == "__main__":
   asyncio.run(actual_main())