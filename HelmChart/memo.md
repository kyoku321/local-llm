```shell
helm install --values values.yaml local-llm ../custom-chart

helm upgrade --values values.yaml local-llm ../custom-chart
helm history news-bot
# 格式：helm rollback <RELEASE_NAME> [REVISION]
helm rollback news-bot 1
```


# temporary test
kubectl run --rm -it python-test --image=python:3.10-slim -- /bin/bash


# Storage debug
ls /var/snap/microk8s/common/default-storage/

# Manual test cron
kubectl create job --from=cronjob/embedding-ingest-cronjob embedding-ingest-manual-$(date +%s)
kubectl get jobs
kubectl get pods -l job-name=$(kubectl get job | grep embedding-ingest-manual | awk '{print $1}')
kubectl logs -l job-name=$(kubectl get job | grep embedding-ingest-manual | awk '{print $1}')
kubectl delete job -l job-name=$(kubectl get job | grep embedding-ingest-manual | awk '{print $1}')



huggingface


export HF_TOKEN="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"

kubectl logs local-llm-6f99b794fc-2h2tq -c init-download-model


# 臨時image download
hf auth login --token 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

hf download openai/gpt-oss-20b --local-dir /models/gpt-oss-20b

hf download Qwen/Qwen3-Embedding-8B --local-dir /models/Qwen3-Embedding-8B

hf download Qwen/Qwen3-Embedding-0.6B --local-dir /models/Qwen3-Embedding-0.6B


hf download Qwen/Qwen3-235B-A22B-Instruct-2507-FP8 --local-dir /models/Qwen3-235B-A22B-Instruct-2507-FP8

hf download zai-org/GLM-4.7-FP8 --local-dir /models/GLM-4.7-FP8

hf download moonshotai/Kimi-K2.5 --local-dir /models/Kimi-K2.5

hf download zai-org/GLM-4.7-Flash --local-dir /models/GLM-4.7-Flash

hf download Qwen/Qwen3-ASR-1.7B --local-dir /models/Qwen3-ASR-1.7B



curl -X POST http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"model": "/models/gpt-oss-20b","messages": [{"role": "system","content": "帮把下面日文翻译为中文。"},{"role": "user","content": "，ベライゾンは、競争激化と顧客獲得の低迷を受け、大規模な人員削減と約200店舗のフランチャイズ化を発表しました。新CEOは、より効率的でアグレッシブな運営モデルへの転換を掲げ、顧客ロイヤリティとリテンションの向上を目指します。このリストラは、同社史上最大規模のものです。"}],"max_tokens": 2048,"temperature": 0.7}'

curl -X POST http://vllm.aggpf.gpu-k8s.cloudcore-tu.net/v1/chat/completions -H "Content-Type: application/json" -d '{"model": "/models/gpt-oss-20b","messages": [{"role": "system","content": "帮把下面日文翻译为中文。"},{"role": "user","content": "，ベライゾンは、競争激化と顧客獲得の低迷を受け、大規模な人員削減と約200店舗のフランチャイズ化を発表しました。新CEOは、より効率的でアグレッシブな運営モデルへの転換を掲げ、顧客ロイヤリティとリテンションの向上を目指します。このリストラは、同社史上最大規模のものです。"}],"max_tokens": 2048,"temperature": 0.7}'

curl -X POST https://llm.aggpf.gpu-k8s.cloudcore-tu.net/v1/chat/completions -H "Content-Type: application/json" -d '{"model": "/models/gpt-oss-20b","messages": [{"role": "system","content": "帮把下面日文翻译为中文。"},{"role": "user","content": "，ベライゾンは、競争激化と顧客獲得の低迷を受け、大規模な人員削減と約200店舗のフランチャイズ化を発表しました。新CEOは、より効率的でアグレッシブな運営モデルへの転換を掲げ、顧客ロイヤリティとリテンションの向上を目指します。このリストラは、同社史上最大規模のものです。"}],"max_tokens": 2048,"temperature": 0.7}'




curl -X GET \
  --resolve vllm.aggpf.gpu-k8s.cloudcore-tu.net:80:103.2.128.50 \
  http://vllm.aggpf.gpu-k8s.cloudcore-tu.net/health


curl -X GET \
  http://vllm.aggpf.gpu-k8s.cloudcore-tu.net/health


 (APIServer pid=1) INFO 11-17 23:22:51 [launcher.py:44] Route: /openapi.json, Methods: GET, HEAD                                                                           │
│ (APIServer pid=1) INFO 11-17 23:22:51 [launcher.py:44] Route: /docs, Methods: GET, HEAD                                                                                   │
│ (APIServer pid=1) INFO 11-17 23:22:51 [launcher.py:44] Route: /docs/oauth2-redirect, Methods: GET, HEAD                                                                   │
 (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /redoc, Methods: GET                                                         │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /health, Methods: GET                                                              │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /load, Methods: GET                                                                │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /ping, Methods: POST                                                               │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /ping, Methods: GET                                                                │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /tokenize, Methods: POST                                                           │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /detokenize, Methods: POST                                                         │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /v1/models, Methods: GET                                                           │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /version, Methods: GET                                                             │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /v1/responses, Methods: POST                                                       │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /v1/responses/{response_id}, Methods: GET                                          │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /v1/responses/{response_id}/cancel, Methods: POST                                  │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /v1/chat/completions, Methods: POST                                                │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /v1/completions, Methods: POST                                                     │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /v1/embeddings, Methods: POST                                                      │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /pooling, Methods: POST                                                            │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /classify, Methods: POST                                                           │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /score, Methods: POST                                                              │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /v1/score, Methods: POST                                                           │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /v1/audio/transcriptions, Methods: POST                                            │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /v1/audio/translations, Methods: POST                                              │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /rerank, Methods: POST                                                             │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /v1/rerank, Methods: POST                                                          │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /v2/rerank, Methods: POST                                                          │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /scale_elastic_ep, Methods: POST                                                   │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /is_scaling_elastic_ep, Methods: POST                                              │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /invocations, Methods: POST                                                        │
│ (APIServer pid=1) INFO 11-16 23:20:39 [launcher.py:44] Route: /metrics, Methods: GET     




kubectl port-forward local-llm-849bd5b988-mbhfk 8000:8000


curl https://embedding.aggpf.gpu-k8s.cloudcore-tu.net/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "/models/Qwen3-Embedding-0.6B",
    "input": "Hello world"
  }'



curl https://embedding.aggpf.gpu-k8s.cloudcore-tu.net/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen3-Embedding-8B",
    "input": ["What is the capital of China?", "Explain gravity"]
  }'


curl -X GET \
  https://embedding.aggpf.gpu-k8s.cloudcore-tu.net/health




kubectl run --rm -it cuda-test --image=nvidia/cuda:13.0.2-runtime-ubuntu24.04 -- /bin/bash


curl -X POST https://embedding.aggpf.gpu-k8s.cloudcore-tu.net/v1/embeddings \
-H "Content-Type: application/json" \
-d '{"model":"/models/Qwen3-Embedding-8B","input":["Hello world"]}'

nvidia-smi 