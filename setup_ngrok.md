# 🚀 Quick Setup: Make Your Faculty Finder Public

## Step 1: Download ngrok (30 seconds)

1. Go to: **https://ngrok.com/download**
2. Click **"Download for Windows"**
3. Save the ZIP file

## Step 2: Extract (10 seconds)

1. Right-click the downloaded ZIP file
2. Click **"Extract All"**
3. Choose your Desktop or Downloads folder

## Step 3: Run ngrok (1 minute)

1. Open the folder where you extracted ngrok
2. Hold **Shift** and **right-click** in the empty space
3. Click **"Open PowerShell window here"**
4. Type this command and press Enter:
   ```
   .\ngrok http 8000
   ```

## Step 4: Get Your Public URL (10 seconds)

You'll see something like this:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8000
```

**That URL is your public Faculty Finder!** 🎉

Copy `https://abc123.ngrok.io` and share it with anyone.

---

## ✅ That's It!

Your Faculty Finder is now:
- ✅ Publicly accessible
- ✅ Working with all features
- ✅ Completely free

**Keep the PowerShell window open** - closing it will stop ngrok.

---

## 🔄 To Use Again Later

1. Make sure your local server is running: `uvicorn vector_api:app --reload --port 8000`
2. Run ngrok again: `.\ngrok http 8000`
3. Get the new URL (it changes each time)

---

**Total time: 2 minutes** ⏱️
