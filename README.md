# josa-model

Josa selection model packaged as:
- FastAPI inference service (`/predict`, `/health`)
- RunPod serverless handler
- Docker images for both pod and serverless deployment

## Local run

```bash
pip install -r requirements.txt
uvicorn api:app --host 0.0.0.0 --port 8000
```

Test:

```bash
python -m unittest discover -v
```

## API

### `GET /health`

Response:

```json
{"status": "ok"}
```

### `POST /predict`

Request:

```json
{
  "word": "집",
  "pair": ["은", "는"]
}
```

Response:

```json
{
  "word": "집",
  "selected_josa": "은",
  "pair": ["은", "는"],
  "combined_text": "집은",
  "has_batchim": true
}
```

## Containerization

### Build pod image (FastAPI)

```bash
docker build -f Dockerfile -t <registry>/josa-model:latest .
docker push <registry>/josa-model:latest
```

### Build RunPod serverless image

```bash
docker build -f Dockerfile.serverless -t <registry>/josa-model:serverless .
docker push <registry>/josa-model:serverless
```

## RunPod deployment

### Option A: Serverless
1. Create a Serverless Template in RunPod using `<registry>/josa-model:serverless`.
2. Set any required env vars in the template.
3. Create a Serverless Endpoint from the template.
4. Invoke endpoint with:

```json
{
  "input": {
    "word": "집",
    "pair": ["은", "는"]
  }
}
```

### Option B: GPU/CPU Pod
1. Create a Pod using `<registry>/josa-model:latest`.
2. Expose container port `8000`.
3. Use proxy/public endpoint and call `/predict`.

## Azure API Management (APIM) integration

1. Create backend in APIM pointing to your RunPod URL.
2. Import/create API with `/health` and `/predict`.
3. Add inbound policy to pass RunPod authorization token if needed.
4. Add throttling/rate limits and optional response cache.
5. Publish API and issue subscription keys.

Example inbound policy:

```xml
<policies>
  <inbound>
    <base />
    <set-header name="Authorization" exists-action="override">
      <value>TOKEN_PLACEHOLDER</value>
    </set-header>
    <rate-limit-by-key calls="60" renewal-period="60" counter-key="@(context.Subscription.Key)" />
  </inbound>
  <backend>
    <base />
  </backend>
  <outbound>
    <base />
  </outbound>
  <on-error>
    <base />
  </on-error>
</policies>
```