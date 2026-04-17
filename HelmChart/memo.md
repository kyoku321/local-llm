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

hf download zai-org/GLM-4.7 --local-dir /models/GLM-4.7

hf download Qwen/Qwen3-ASR-1.7B --local-dir /models/Qwen3-ASR-1.7B

hf download Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice --local-dir /models/Qwen3-TTS-12Hz-1.7B-CustomVoice

hf download Qwen/Qwen3-Coder-Next --local-dir /models/Qwen3-Coder-Next

hf download zai-org/GLM-5 --local-dir /models/GLM-5

hf download stepfun-ai/Step-3.5-Flash --local-dir /models/Step-3.5-Flash

hf download MiniMaxAI/MiniMax-M2.7 --local-dir /models/MiniMax-M2.7


hf download Qwen/Qwen3.6-35B-A3B --local-dir /models/Qwen3.6-35B-A3B
hf download Qwen/Qwen3.6-35B-A3B-FP8 --local-dir /models/Qwen3.6-35B-A3B-FP8

hf download Qwen/Qwen3.5-27B --local-dir /models/Qwen3.5-27B


hf download google/gemma-4-E4B-it --local-dir /models/gemma-4-E4B-it

curl -X POST http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"model": "/models/gpt-oss-20b","messages": [{"role": "system","content": "帮把下面日文翻译为中文。"},{"role": "user","content": "，ベライゾンは、競争激化と顧客獲得の低迷を受け、大規模な人員削減と約200店舗のフランチャイズ化を発表しました。新CEOは、より効率的でアグレッシブな運営モデルへの転換を掲げ、顧客ロイヤリティとリテンションの向上を目指します。このリストラは、同社史上最大規模のものです。"}],"max_tokens": 2048,"temperature": 0.7}'

curl -X POST http://vllm.aggpf.gpu-k8s.cloudcore-tu.net/v1/chat/completions -H "Content-Type: application/json" -d '{"model": "/models/gpt-oss-20b","messages": [{"role": "system","content": "帮把下面日文翻译为中文。"},{"role": "user","content": "，ベライゾンは、競争激化と顧客獲得の低迷を受け、大規模な人員削減と約200店舗のフランチャイズ化を発表しました。新CEOは、より効率的でアグレッシブな運営モデルへの転換を掲げ、顧客ロイヤリティとリテンションの向上を目指します。このリストラは、同社史上最大規模のものです。"}],"max_tokens": 2048,"temperature": 0.7}'

curl -X POST https://llm.aggpf.gpu-k8s.cloudcore-tu.net/v1/chat/completions -H "Content-Type: application/json" -d '{"model": "/models/gpt-oss-20b","messages": [{"role": "system","content": "帮把下面日文翻译为中文。"},{"role": "user","content": "，ベライゾンは、競争激化と顧客獲得の低迷を受け、大規模な人員削減と約200店舗のフランチャイズ化を発表しました。新CEOは、より効率的でアグレッシブな運営モデルへの転換を掲げ、顧客ロイヤリティとリテンションの向上を目指します。このリストラは、同社史上最大規模のものです。"}],"max_tokens": 2048,"temperature": 0.7}'




curl -X GET \
  --resolve vllm.aggpf.gpu-k8s.cloudcore-tu.net:80:103.2.128.50 \
  http://vllm.aggpf.gpu-k8s.cloudcore-tu.net/health


curl -X GET \
  http://vllm.aggpf.gpu-k8s.cloudcore-tu.net/health
 



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