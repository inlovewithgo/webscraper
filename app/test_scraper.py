import requests
import time

BASE_URL = "http://localhost:8000"

def test_scraper():
    print("🧪 Testing scraper...")
    
    response = requests.post(f"{BASE_URL}/scrape", json={"url": "https://example.com"})
    if response.status_code == 200:
        task_id = response.json()["task_id"]
        print(f"✅ Scrape started, task_id: {task_id}")
    else:
        print(f"❌ Scrape failed: {response.status_code}")
        return
    
    for i in range(10):
        time.sleep(2)
        result = requests.get(f"{BASE_URL}/result/{task_id}")
        if result.status_code == 200:
            data = result.json()
            print(f"✅ Got results: {data}")
            break
        elif result.status_code == 404:
            print(f"⏳ Waiting for results... ({i+1}/10)")
        else:
            print(f"❌ Error getting results: {result.status_code}")
            break
    
    tasks = requests.get(f"{BASE_URL}/tasks")
    if tasks.status_code == 200:
        print(f"✅ Tasks endpoint works: {len(tasks.json())} tasks")
    else:
        print(f"❌ Tasks endpoint failed: {tasks.status_code}")

if __name__ == "__main__":
    test_scraper()