
@app.get("/search", response_class=HTMLResponse)
async def search():
    monitor_id = 123855358
    result = search_datadog_monitor_by_id(api_key, app_key, monitor_id)
    return HTMLResponse(content=json.dumps(result, indent=4))

@app.get("/search-monitors")
async def search_monitors(query: str):
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key
    }
    response = requests.get(
        "https://api.datadoghq.com/api/v1/monitor/search",
        headers=headers,
        params={"query": query}
    )
    if response.status_code == 200:
        data = response.json()['monitors']
        return JSONResponse(content=data)
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

